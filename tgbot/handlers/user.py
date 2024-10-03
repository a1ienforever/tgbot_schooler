from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from tgbot.keyboards.inline import choose_frame_kb, choose_class_kb, choose_letter_kb
from Web.AdminPanel.models import TgUser, User
from tgbot.misc.states import SchoolerCounter

user_router = Router()


@user_router.message(Command('report'))
async def choose_start(message: Message, user: TgUser, state: FSMContext):
    await state.clear()
    await message.answer("Пожалуйста выберите корпус учащихся", reply_markup=choose_frame_kb())

    await state.set_state(SchoolerCounter.frame)


@user_router.callback_query(F.data.startswith('frame'), SchoolerCounter.frame)
async def choose_frame(call: CallbackQuery, user: TgUser, state: FSMContext):
    frame = call.data.split(':')[1]
    await state.update_data(frame=frame)
    # await call.message.answer("Пожалуйста выберите класс учащихся", reply_markup=choose_class_kb())
    # await call.message.edit_reply_markup(reply_markup=choose_class_kb())
    await call.message.edit_text("Пожалуйста выберите класс учащихся", reply_markup=choose_class_kb())
    await state.set_state(SchoolerCounter.class_num)


@user_router.callback_query(F.data.startswith('class'), SchoolerCounter.class_num)
async def choose_class(call: CallbackQuery, user: TgUser, state: FSMContext):
    class_num = call.data.split(':')[1]
    await state.update_data(class_num=class_num)
    # await call.message.answer("Выберите букву класса.", reply_markup=choose_letter_kb())
    # await call.message.edit_reply_markup(reply_markup=choose_letter_kb())
    await call.message.edit_text("Выберите букву класса", reply_markup=choose_letter_kb())

    await state.set_state(SchoolerCounter.letter)


@user_router.callback_query(F.data.startswith('letter'), SchoolerCounter.letter)
async def choose_letter(call: CallbackQuery, state: FSMContext, user: TgUser):
    class_letter = call.data.split(':')[1]
    await state.update_data(letter=class_letter)
    # await call.message.answer("Введите количество учеников")
    await call.message.edit_text("Введите количество учеников", reply_markup=None)

    await state.set_state(SchoolerCounter.count)


@user_router.message(SchoolerCounter.count)
async def choose_count(message: Message, state: FSMContext, user: TgUser):
    count = message.text
    await state.update_data(count=count)
    user1 = User.objects.filter(tg_user__telegram_id=user.telegram_id).get()
    print(user1)
    data = await state.get_data()
    msg = (f"{user1.name} {user1.patronymic}, в {data.get('frame')} корпусе "
           f"{data.get('class_num')}{data.get('letter')} - {data.get('count')} человек")
    await message.answer(msg)
