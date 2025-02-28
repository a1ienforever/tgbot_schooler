import logging

from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from icecream import ic

from Web.AdminPanel.models import TgUser

from tgbot.decorators.access_rights import role_required
from tgbot.keyboards.inline import (
    choose_frame_kb,
    generate_inline_keyboard,
)
from tgbot.keyboards.reply import menu_kb
from tgbot.misc.callback import (
    FrameCallback,
    ClassCallback,
    LetterCallback,
)
from tgbot.misc.states import IncidentLater, IncidentForm
from tgbot.services.choose import (
    choose_class_state,
    choose_letter_state, choose_frame_state,
)

router = Router()
persons = set()

@router.message(Command("report"))
@role_required(["director", "deputy"])
async def start_report(message: Message, user: TgUser):
    await message.answer(
        "Выберите нужный вид отчета в клавиатуре снизу", reply_markup= menu_kb()
    )

@router.message(F.text.upper().in_(['БЕЗ ФОРМЫ', 'ОПОЗДАВШИЙ']))
@role_required(["director", "deputy"])
async def choose_start_incident(
    message: Message,
    user: TgUser,
    lesson_number: int = 1,
    state: FSMContext = None,
):
    try:
        message_type = message.text.upper()
        text = None
        if message_type == 'ОПОЗДАВШИЙ':
            await state.set_state(IncidentLater.frame)
            type_report = 'later'
            text = "Пожалуйста выберите корпус учащихся для отметки опоздавшего"
        elif message_type == 'БЕЗ ФОРМЫ':
            await state.set_state(IncidentForm.frame)
            text = "Пожалуйста выберите корпус для отметки ученика без формы"
            type_report = 'form'
        else:
            return

        await choose_frame_state(message=message, type_report=type_report, lesson_num=lesson_number, text=text)

    except AiogramError as e:
        logging.info(f"{e}")

@router.callback_query(FrameCallback)
async def choose_frame(
    call: CallbackQuery, callback_data: FrameCallback, user: TgUser, state: FSMContext
):
    frame = callback_data.frame
    if callback_data.type_report == 'form':
        persons.clear()
        await state.set_state(IncidentForm.class_num)
    elif callback_data.type_report == 'later':
        await state.set_state(IncidentLater.class_num)
    else:
        return

    await state.update_data(frame=frame)
    await choose_class_state(type_report=callback_data.type_report, frame=frame, call=call, lesson_num=1)


@router.callback_query(ClassCallback)
async def choose_class(
    call: CallbackQuery, callback_data: ClassCallback, user: TgUser, state: FSMContext
):
    data = await state.get_data()
    frame = data.get("frame")
    class_num = callback_data.class_num
    ic()
    ic(call.data)
    if class_num == 100:
        text = str
        if callback_data.type_report == 'form':
            await state.set_state(IncidentForm.frame)
            text = "Пожалуйста выберите корпус для отметки ученика без формы"
        elif callback_data.type_report == 'later':
            await state.set_state(IncidentLater.frame)
            text = "Пожалуйста выберите корпус учащихся для отметки опоздавшего"


        await call.message.edit_text(
            text=text,
            reply_markup=choose_frame_kb(
                type_report=callback_data.type_report, lesson_num=callback_data.lesson_num
            ),
        )
        return
    await state.update_data(class_num=class_num)

    await choose_letter_state(
        frame,
        class_num,
        lesson_num=callback_data.lesson_num,
        type_report=callback_data.type_report,
        call=call,
    )
    if callback_data.type_report == 'form':
        await state.set_state(IncidentForm.letter)
    elif callback_data.type_report == 'later':
        await state.set_state(IncidentLater.letter)

@router.callback_query(LetterCallback)
async def choose_letter(
        call: CallbackQuery, callback_data: LetterCallback, state: FSMContext, user: TgUser
):
    class_letter = callback_data.letter
    await state.update_data(letter=class_letter)
    data = await state.get_data()
    frame = data.get("frame")

    if class_letter == "back":
        await choose_class_state(
            type_report=callback_data.type_report,
            lesson_num=callback_data.lesson_num,
            frame=frame,
            call=call,
        )
        if callback_data.type_report == 'form':
            await state.set_state(IncidentForm.frame)

        elif callback_data.type_report == 'later':
            await state.set_state(IncidentLater.frame)
        return

    if callback_data.type_report == 'form':
        await call.message.edit_text(
            "Выберите учеников (нажимайте несколько раз для выбора, затем 'Готово')",
            reply_markup=generate_inline_keyboard(
                type_report="form", state=data, persons=persons
            ).as_markup(),
        )
        await state.set_state(IncidentForm.person)
    elif callback_data.type_report == 'later':
        await call.message.edit_text(
            "Выберите имя ученика",
            reply_markup=generate_inline_keyboard(
                type_report="later", state=data, persons=set()
            ).as_markup(),
        )
        await state.set_state(IncidentLater.person)
