import logging

from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Web.AdminPanel.models import TgUser
from Web.Record.models import IncidentRecord
from Web.Schooler.models import Person
from tgbot.decorators.access_rights import role_required
from tgbot.keyboards.inline import (
    choose_frame_kb,
    second_frame_class_kb,
    first_frame_class_kb,
    generate_inline_keyboard,
)
from tgbot.misc.states import Incident, IncidentLater
from tgbot.services.choose import (
    choose_frame_state,
    choose_class_state,
    choose_letter_state,
)

router = Router()


@router.message(F.text.upper().in_("ОПОЗДАВШИЙ"))
@role_required(["director", "deputy"])
async def choose_start_incident(
    message: Message,
    user: TgUser,
    lesson_number: int = 1,
    state: FSMContext = None,
):
    try:
        if state:
            if message.text.upper() == "ОПОЗДАВШИЙ":
                await state.set_state(IncidentLater.frame)
                await state.update_data(message_type="later")

        await choose_frame_state(message, 1)
    except AiogramError as e:
        logging.info(f"{e}")


@router.callback_query(F.data.startswith("frame"), IncidentLater.frame)
async def choose_frame(call: CallbackQuery, user: TgUser, state: FSMContext):
    data = call.data.split(":")
    frame = data[1]

    await state.update_data(frame=frame)
    await choose_class_state(frame, call)
    await state.set_state(IncidentLater.class_num)


@router.callback_query(F.data.startswith("class"), IncidentLater.class_num)
async def choose_class(call: CallbackQuery, user: TgUser, state: FSMContext):
    data = await state.get_data()
    frame = data.get("frame")
    class_num = call.data.split(":")[1]

    if class_num == "back":
        await state.set_state(IncidentLater.frame)
        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(data.get("lesson_num")),
        )
        return
    await state.update_data(class_num=class_num)
    await choose_letter_state(frame, class_num, call)
    await state.set_state(IncidentLater.letter)


@router.callback_query(F.data.startswith("letter"), Incident.letter)
async def choose_letter(call: CallbackQuery, state: FSMContext, user: TgUser):
    class_letter = call.data.split(":")[1]
    data = await state.get_data()
    frame = data.get("frame")

    if class_letter == "back":
        await state.set_state(IncidentLater.class_num)
        await choose_class_state(frame, call)
        return

    await state.update_data(letter=class_letter)
    data = await state.get_data()
    await call.message.edit_text(
        "Выберите имя ученика",
        reply_markup=generate_inline_keyboard(data).as_markup(),
    )
    await state.set_state(IncidentLater.person)


@router.callback_query(F.data.startswith("person"), IncidentLater.person)
async def late_record(call: CallbackQuery, state: FSMContext, user: TgUser):
    person_id = call.data.split(":")[1]
    data = await state.get_data()

    if person_id == "back":
        await state.set_state(IncidentLater.frame)
        if data["frame"] == "4":
            await call.message.edit_text(
                "Выберите класс учащихся", reply_markup=second_frame_class_kb()
            )
        if data["frame"] == "1":
            await call.message.edit_text(
                "Выберите класс учащихся", reply_markup=first_frame_class_kb()
            )
        return

    person = Person.objects.filter(id=person_id).get()
    text = f"{person.last_name} {person.first_name} {person.class_assigned.grade}{person.class_assigned.letter}"

    await IncidentRecord.objects.acreate(person_id=person, status=IncidentRecord.LATE)
    await call.message.edit_text(
        f"Запись создана: \n" f"Опоздавший(-ая) {text}",
    )
    await state.clear()
