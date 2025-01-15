import logging
from curses.ascii import isdigit

from aiogram import Router, Bot, F
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from icecream import ic

from Web.AdminPanel.models import TgUser

from tgbot.handlers.admin_handler import send_admin
from tgbot.keyboards.inline import *
from tgbot.misc.callback import FrameCallback
from tgbot.misc.states import SchoolerCounter
from tgbot.services.choose import choose_class_state, choose_letter_state
from tgbot.services.db import create_record
from tgbot.utils import get_user_data, get_state_data, format_message

router = Router()


async def choose_start(
        user_id: int, bot: Bot, lesson_number: int, state: FSMContext = None
):
    try:
        await state.clear()
        await state.set_state(SchoolerCounter.frame)

        await bot.send_message(
            user_id,
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(type_report="count", lesson_num=lesson_number),
        )
    except ValueError as ve:
        logging.error(f"Ошибка состояния: {ve}")
    except AiogramError as e:
        logging.info(f"User: {user_id} - {e}")


@router.callback_query(
    FrameCallback.filter(F.type_report == "count"),
)
async def choose_frame(
        call: CallbackQuery, callback_data: FrameCallback, user: TgUser, state: FSMContext
):
    ic(callback_data)
    frame = callback_data.frame
    lesson_num = callback_data.lesson_num

    await state.update_data(frame=frame, lesson_num=lesson_num)
    await state.set_state(SchoolerCounter.class_num)
    await choose_class_state(
        type_report="count", lesson_num=lesson_num, frame=frame, call=call
    )


@router.callback_query(
    ClassCallback.filter(F.type_report == "count"),
)
async def choose_class(
        call: CallbackQuery, callback_data: ClassCallback, user: TgUser, state: FSMContext
):
    data = await state.get_data()
    frame = data.get("frame")
    class_num = callback_data.class_num
    ic()
    if class_num == 100:
        await state.set_state(SchoolerCounter.frame)
        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(
                type_report="count", lesson_num=data.get("lesson_num")
            ),
        )
        return
    ic()
    await state.update_data(class_num=class_num)
    await state.set_state(SchoolerCounter.letter)
    await choose_letter_state(
        frame=frame,
        class_num=class_num,
        lesson_num=data.get("lesson_num"),
        type_report="count",
        call=call,
    )


@router.callback_query(
    LetterCallback.filter(F.type_report == "count"),
)
async def choose_letter(
        call: CallbackQuery, callback_data: LetterCallback, state: FSMContext, user: TgUser
):
    class_letter = callback_data.letter
    data = await state.get_data()
    frame = data.get("frame")
    ic()
    if class_letter == "back":
        await state.set_state(SchoolerCounter.class_num)
        if frame == "4":
            await call.message.edit_text(
                "Выберите класс учащихся",
                reply_markup=second_frame_class_kb(callback_data.type_report, callback_data.lesson_num)
            )
        if frame == "1":
            await call.message.edit_text(
                "Выберите класс учащихся",
                reply_markup=first_frame_class_kb(callback_data.type_report, callback_data.lesson_num)
            )
        return

    await state.update_data(letter=class_letter)
    await state.set_state(SchoolerCounter.count)
    await call.message.edit_text("Введите количество учеников", reply_markup=None)


@router.message(SchoolerCounter.count)
async def choose_count(message: Message, state: FSMContext, user: TgUser):
    def is_valid_count(value: str) -> bool:
        """Проверяет, является ли значение числом и находится ли оно в пределах допустимого диапазона."""
        try:
            count = int(value)
            return 0 <= count < 35
        except ValueError:
            return False

    if is_valid_count(message.text):
        count = int(message.text)
        await state.update_data(count=count)

        # Получение данных пользователя и состояния
        user_data = await get_user_data(user)
        state_data = await get_state_data(state)
        lesson_num = (await state.get_data()).get("lesson_num")

        # Форматирование сообщения
        msg = await format_message(
            user_data,
            state_data["frame"],
            state_data["class_num"],
            state_data["letter"],
            state_data["count"],
            lesson_num,
        )

        # Отправка сообщения
        await message.answer(msg, reply_markup=accept_record_kb())
    else:
        # Обработка неверных данных
        await state.set_state(SchoolerCounter.count)
        await message.answer(
            "Проверьте корректность вводимых данных. "
            "Сообщение должно быть числом и не превышать количество учеников в классе.",
            reply_markup=None,
        )


@router.callback_query(F.data.startswith("check"))
async def check(call: CallbackQuery, state: FSMContext, user: TgUser):
    check_record = call.data.split(":")[1]
    state_info = await state.get_data()
    if check_record == "accept":
        user1 = await get_user_data(user)
        state_data = await get_state_data(state)
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
        await state.clear()
    elif check_record == "restart":
        await state.clear()
        await state.set_state(SchoolerCounter.frame)

        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb("count", state_info["lesson_num"]),
        )
