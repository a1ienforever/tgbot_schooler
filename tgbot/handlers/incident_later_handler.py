import logging

from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from icecream import ic

from Web.AdminPanel.models import TgUser
from Web.Record.models import IncidentRecord
from Web.Schooler.models import Person
from tgbot.decorators.access_rights import role_required
from tgbot.keyboards.inline import (
    choose_frame_kb,
    generate_inline_keyboard,
)
from tgbot.misc.callback import (
    FrameCallback,
    ClassCallback,
    LetterCallback,
    PersonCallback,
)
from tgbot.misc.states import IncidentLater
from tgbot.services.choose import (
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

        await state.set_state(IncidentLater.frame)

        await message.answer(
            "Пожалуйста выберите корпус учащихся для отметки опоздавшего",
            reply_markup=choose_frame_kb(
                type_report="later",
                lesson_num=lesson_number,
            ),
        )
    except AiogramError as e:
        logging.info(f"{e}")


@router.callback_query(FrameCallback.filter(F.type_report == "later"))
async def choose_frame(
    call: CallbackQuery, callback_data: FrameCallback, user: TgUser, state: FSMContext
):
    frame = callback_data.frame

    await state.update_data(frame=frame)
    await choose_class_state(type_report="later", frame=frame, call=call, lesson_num=1)
    await state.set_state(IncidentLater.class_num)


@router.callback_query(
    ClassCallback.filter(F.type_report == "later"), IncidentLater.class_num
)
async def choose_class(
    call: CallbackQuery, callback_data: ClassCallback, user: TgUser, state: FSMContext
):
    data = await state.get_data()
    frame = data.get("frame")
    class_num = callback_data.class_num
    ic()
    ic(call.data)
    if class_num == 100:
        await state.set_state(IncidentLater.frame)
        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся для отметки опоздавшего",
            reply_markup=choose_frame_kb(
                type_report="later", lesson_num=callback_data.lesson_num
            ),
        )
        return
    await state.update_data(class_num=class_num)
    await choose_letter_state(
        frame,
        class_num,
        lesson_num=callback_data.lesson_num,
        type_report="later",
        call=call,
    )

    await state.set_state(IncidentLater.letter)


@router.callback_query(LetterCallback.filter(F.type_report == "later"))
async def choose_letter(
    call: CallbackQuery, callback_data: LetterCallback, state: FSMContext, user: TgUser
):
    class_letter = callback_data.letter
    await state.update_data(letter=class_letter)
    data = await state.get_data()
    frame = data.get("frame")

    if class_letter == "back":
        await choose_class_state(
            type_report="later",
            lesson_num=callback_data.lesson_num,
            frame=frame,
            call=call,
        )
        await state.set_state(IncidentLater.class_num)
        return

    await state.update_data(letter=class_letter)
    await call.message.edit_text(
        "Выберите имя ученика",
        reply_markup=generate_inline_keyboard(
            type_report="later", state=data, persons=set()
        ).as_markup(),
    )
    await state.set_state(IncidentLater.person)


@router.callback_query(
    PersonCallback.filter(F.type_report == "later"),
)
async def late_record(
    call: CallbackQuery, callback_data: PersonCallback, state: FSMContext, user: TgUser
):
    person_id = callback_data.person_id
    data = await state.get_data()

    if person_id == -2:
        await state.set_state(IncidentLater.frame)
        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(type_report="later", lesson_num=1),
        )
        return

    person = Person.objects.filter(id=person_id).get()
    text = f"{person.last_name} {person.first_name} {person.class_assigned.grade}{person.class_assigned.letter}"

    await IncidentRecord.objects.acreate(person_id=person, status=IncidentRecord.LATE)
    await state.clear()
    await call.message.edit_text(
        f"Запись создана: \n" f"Опоздавший(-ая) {text}",
    )
