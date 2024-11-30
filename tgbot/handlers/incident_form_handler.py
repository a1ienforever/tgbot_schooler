import logging

from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Web.AdminPanel.models import TgUser
from Web.Record.models import IncidentRecord
from Web.Schooler.models import Person
from tgbot.decorators.access_rights import role_required
from tgbot.keyboards.inline import (
    choose_frame_kb,
    generate_inline_keyboard,
)
from tgbot.keyboards.reply import menu_kb
from tgbot.misc.states import IncidentForm
from tgbot.services.choose import (
    choose_frame_state,
    choose_class_state,
    choose_back,
    choose_letter_state,
)

router = Router()


@router.message(Command("report"))
@role_required(["director", "deputy"])
async def start_report(message: Message, user: TgUser):
    await message.answer(
        "Выберите нужный вид отчета в клавиатуре снизу", reply_markup=menu_kb()
    )


@router.message(F.text.upper().in_("БЕЗ ФОРМЫ"))
@role_required(["director", "deputy"])
async def choose_start_incident(
    message: Message,
    user: TgUser,
    lesson_number: int = 1,
    state: FSMContext = None,
):
    try:
        if state:
            await state.set_state(IncidentForm.frame)

        await message.answer(
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(lesson_num=lesson_number),
        )
    except AiogramError as e:
        logging.info(f"{e}")


@router.callback_query(F.data.startswith("frame"), IncidentForm.frame)
async def choose_frame(call: CallbackQuery, user: TgUser, state: FSMContext):
    data = call.data.split(":")
    frame = data[1]

    await state.update_data(frame=frame)
    await choose_class_state(frame, call)
    await state.set_state(IncidentForm.class_num)


@router.callback_query(F.data.startswith("class"), IncidentForm.class_num)
async def choose_class(call: CallbackQuery, user: TgUser, state: FSMContext):
    data = await state.get_data()
    frame = data.get("frame")
    class_num = call.data.split(":")[1]

    if class_num == "back":
        await state.set_state(IncidentForm.frame)
        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(data.get("lesson_num")),
        )
        return

    await state.update_data(class_num=class_num)
    await choose_letter_state(frame, class_num, call)

    await state.set_state(IncidentForm.letter)


@router.callback_query(F.data.startswith("letter"), IncidentForm.letter)
async def choose_letter(call: CallbackQuery, state: FSMContext, user: TgUser):
    class_letter = call.data.split(":")[1]
    data = await state.get_data()
    frame = data.get("frame")

    if class_letter == "back":
        await state.set_state(IncidentForm.frame)
        await choose_back(frame, call)

    await state.update_data(letter=class_letter)
    data = await state.get_data()
    await call.message.edit_text(
        "Выберите имя ученика",
        reply_markup=generate_inline_keyboard(data).as_markup(),
    )
    await state.set_state(IncidentForm.person)


@router.callback_query(F.data.startswith("person"), IncidentForm.person)
async def late_record(call: CallbackQuery, state: FSMContext, user: TgUser):
    person_id = call.data.split(":")[1]
    data = await state.get_data()
    if person_id == "back":
        await state.set_state(IncidentForm.frame)
        await choose_frame_state(call.message, 1)

    person = Person.objects.filter(id=person_id).get()
    text = f"{person.last_name} {person.first_name} {person.class_assigned.grade}{person.class_assigned.letter}"

    await IncidentRecord.objects.acreate(
        person_id=person, status=IncidentRecord.WITHOUT_UNIFORM
    )
    await call.message.edit_text(
        f"Запись создана: \n" f"Без формы {text}",
    )
    await state.clear()
