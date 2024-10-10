

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.handlers.admin_handler import create_record, send_admin
from tgbot.keyboards.inline import *

from Web.AdminPanel.models import TgUser, User
from tgbot.misc.states import SchoolerCounter

router = Router()


async def choose_start(user_id: int, bot: Bot, state: FSMContext = None):

    if state:
        current_state = await state.get_state()

        if current_state is not None:
            print(f"Current state before sending new message: {current_state}")

        await state.set_state(SchoolerCounter.frame)
        print(f"State set to: {SchoolerCounter.frame} for user {user_id}")

    await bot.send_message(
        user_id,
        "Пожалуйста выберите корпус учащихся",
        reply_markup=choose_frame_kb(),
    )


@router.callback_query(F.data.startswith("frame"))
async def choose_frame(call: CallbackQuery, user: TgUser, state: FSMContext):

    frame = call.data.split(":")[1]

    await state.update_data(frame=frame)
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

    class_num = call.data.split(":")[1]
    if class_num == "back":
        await state.set_state(SchoolerCounter.frame)
        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся", reply_markup=choose_frame_kb()
        )
        return
    data = await state.get_data()
    frame = data.get("frame")

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
    await call.message.edit_text("Введите количество учеников", reply_markup=None)

    await state.set_state(SchoolerCounter.count)


@router.message(SchoolerCounter.count)
async def choose_count(message: Message, state: FSMContext, user: TgUser):
    try:
        count = int(message.text)
        await state.update_data(count=count)
        user1 = User.objects.filter(tg_user__telegram_id=user.telegram_id).get()

        data = await state.get_data()
        frame = data.get("frame")
        class_num = data.get("class_num")
        letter = data.get("letter")
        count = data.get("count")
        msg = (
            f"{user1.name} {user1.patronymic}, проверьте запись: в {frame} корпусе "
            f"{class_num}{letter} - {count} человек"
        )
        await message.answer(msg, reply_markup=accept_record_kb())

    except ValueError as e:

        await message.answer("Введите количество учеников числом", reply_markup=None)
        await state.set_state(SchoolerCounter.count)
        print(e)


@router.callback_query(F.data.startswith("check"))
async def check(call: CallbackQuery, state: FSMContext, user: TgUser):
    check_record = call.data.split(":")[1]
    if check_record == "accept":
        user1 = User.objects.filter(tg_user__telegram_id=user.telegram_id).get()
        data = await state.get_data()
        frame = data.get("frame")
        class_num = data.get("class_num")
        letter = data.get("letter")
        count = data.get("count")
        await create_record(frame, class_num, letter, count)
        await send_admin(call.message.bot)
        await call.message.edit_text(
            f"{user1.name} {user1.patronymic}, сделана запись: в {frame} корпусе "
            f"{class_num}{letter} - {count} человек"
        )
    elif check_record == "restart":
        await state.clear()
        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся", reply_markup=choose_frame_kb()
        )
        await state.set_state(SchoolerCounter.frame)
