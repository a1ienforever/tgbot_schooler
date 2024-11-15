import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Web.AdminPanel.models import TgUser
from tgbot.handlers.admin_handler import send_admin
from tgbot.keyboards.inline import *
from tgbot.misc.states import SchoolerCounter
from tgbot.services.db import create_record
from tgbot.utils import get_user_data, get_state_data, format_message

router = Router()


async def choose_start(
    user_id: int, bot: Bot, lesson_number: int, state: FSMContext = None
):
    try:
        if state:
            current_state = await state.get_state()
            await state.update_data(message_type="counter")
            if current_state is not None:
                print(f"Current state before sending new message: {current_state}")

            await state.set_state(SchoolerCounter.frame)
            print(f"State set to: {SchoolerCounter.frame} for user {user_id}")
        await bot.send_message(
            user_id,
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(lesson_num=lesson_number),
        )
    except AiogramError as e:
        logging.info(f"User: {user_id} - {e}")


@router.callback_query(F.data.startswith("frame"))
async def choose_frame(call: CallbackQuery, user: TgUser, state: FSMContext):
    data = call.data.split(":")
    frame = data[1]
    lesson_num = data[2]

    await state.update_data(frame=frame, lesson_num=lesson_num)
    if frame == "1":
        await call.message.edit_text(
            "Выберите класс учащихся", reply_markup=first_frame_class_kb()
        )
    if frame == "4":
        await call.message.edit_text(
            "Выберите класс учащихся", reply_markup=second_frame_class_kb()
        )
    await state.set_state(SchoolerCounter.class_num)


@router.callback_query(F.data.startswith("class"), SchoolerCounter.class_num)
async def choose_class(call: CallbackQuery, user: TgUser, state: FSMContext):
    data = await state.get_data()
    frame = data.get("frame")
    class_num = call.data.split(":")[1]

    if class_num == "back":
        await state.set_state(SchoolerCounter.frame)
        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(data.get("lesson_num")),
        )
        return

    await state.update_data(class_num=class_num)
    if frame == "1":
        await call.message.edit_text(
            "Выберите букву класса", reply_markup=first_frame_letter_kb()
        )
    elif frame == "4":
        if int(class_num) in [1]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_eab_kb()
            )
        if int(class_num) in [2, 6, 7, 11]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_a_kb()
            )
        if int(class_num) in [3]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_ea_kb()
            )
        if int(class_num) in [4, 5]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_ab_kb()
            )
        if int(class_num) in [8]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_gnste_kb()
            )
        if int(class_num) in [9]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_gnte_kb()
            )
        if int(class_num) in [10]:
            await call.message.edit_text(
                "Выберите букву класса", reply_markup=generate_npt_kb()
            )

    await state.set_state(SchoolerCounter.letter)


@router.callback_query(F.data.startswith("letter"), SchoolerCounter.letter)
async def choose_letter(call: CallbackQuery, state: FSMContext, user: TgUser):
    class_letter = call.data.split(":")[1]
    data = await state.get_data()
    frame = data.get("frame")

    if class_letter == "back":
        await state.set_state(SchoolerCounter.class_num)
        if frame == "4":
            await call.message.edit_text(
                "Выберите класс учащихся", reply_markup=second_frame_class_kb()
            )
        if frame == "1":
            await call.message.edit_text(
                "Выберите класс учащихся", reply_markup=first_frame_class_kb()
            )
        return

    await state.update_data(letter=class_letter)
    data = await state.get_data()
    if data.get("message_type") == "counter":
        await call.message.edit_text("Введите количество учеников", reply_markup=None)
        await state.set_state(SchoolerCounter.count)
    else:
        await call.message.edit_text(
            "Выберите имя ученика",
            reply_markup=generate_inline_keyboard(data).as_markup(),
        )
        await state.set_state(SchoolerCounter.name)


@router.message(F.text.len() == 2, SchoolerCounter.count)
async def choose_count(message: Message, state: FSMContext, user: TgUser):
    try:
        count = int(message.text)
        await state.update_data(count=count)
        user1 = await get_user_data(user)
        state_data = await get_state_data(state)
        state_info = await state.get_data()
        msg = await format_message(
            user1,
            state_data["frame"],
            state_data["class_num"],
            state_data["letter"],
            state_data["count"],
            state_info.get("lesson_num"),
        )
        print(state_data["message_type"])
        await message.answer(msg, reply_markup=accept_record_kb())

    except ValueError as e:

        await message.answer("Введите количество учеников числом", reply_markup=None)
        await state.set_state(SchoolerCounter.count)
        print(e)


@router.callback_query(F.data.startswith("check"))
async def check(call: CallbackQuery, state: FSMContext, user: TgUser):
    check_record = call.data.split(":")[1]
    state_info = await state.get_data()
    if check_record == "accept":
        user1 = await get_user_data(user)
        state_data = await get_state_data(state)
        await state.clear()
        await create_record(
            frame=state_data["frame"],
            class_num=state_data["class_num"],
            letter=state_data["letter"],
            count=state_data["count"],
            lesson_num=state_info.get("lesson_num"),
        )
        await send_admin(call.message.bot, lesson_num=int(state_info.get("lesson_num")))
        await call.message.edit_text(
            f"{user1.name} {user1.patronymic}, сделана запись: на {state_info.get('lesson_num')} уроке в {state_data['frame']} корпусе "
            f"{state_data['class_num']}{state_data['letter']} - {state_data['count']} человек"
        )
    elif check_record == "restart":
        await state.clear()
        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(state_info["lesson_num"]),
        )
        await state.set_state(SchoolerCounter.frame)
