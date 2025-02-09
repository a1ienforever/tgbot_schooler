from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Web.AdminPanel.models import TgUser, User
from tgbot.keyboards.inline import start_cb, accept_cb
from tgbot.misc.states import Register


router = Router()


@router.message(CommandStart())
async def user_start(message: Message, user: TgUser):
    await message.answer("Пройдите этап регистрации", reply_markup=start_cb())


@router.callback_query(F.data == "register")
async def register(call: CallbackQuery, user: TgUser, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    if User.objects.filter(tg_user__telegram_id=user.telegram_id):
        await call.message.answer("Вы уже зарегестрированы.")
        await state.clear()
        return
    await state.clear()
    await call.message.answer("Введите фамилию: ")
    await state.set_state(Register.surname)


@router.message(F.text, Register.surname)
async def save_full_name(message: Message, state: FSMContext):
    if len(message.text.split()) != 1:
        await message.answer("Фамилия введена некорректно\n" "Попробуйте еще раз")
        await state.set_state(Register.surname)
    else:
        await state.update_data(surname=message.text)
        await message.answer("Введите имя: ")
        await state.set_state(Register.name)


@router.message(F.text, Register.name)
async def save_full_name(message: Message, state: FSMContext):
    if len(message.text.split()) != 1:
        await message.answer("Имя введено некорректно\n" "Попробуйте еще раз")
        await state.set_state(Register.name)
    else:
        await state.update_data(name=message.text)
        await message.answer("Введите отчество: ")
        await state.set_state(Register.patronymic)


@router.message(F.text, Register.patronymic)
async def save_full_name(message: Message, state: FSMContext, user: TgUser):
    if len(message.text.split()) != 1:
        await message.answer("Отчество введено некорректно" "Попробуйте еще раз")
        await state.set_state(Register.patronymic)
    else:
        await state.update_data(patronymic=message.text)

        data = await state.get_data()
        surname = data.get("surname")
        name = data.get("name")
        patronymic = data.get("patronymic")
        msg = f"Фамилия: {surname}\n" f"Имя: {name}\n" f"Отчество: {patronymic}"
        await User.objects.aget_or_create(
            name=name, surname=surname, patronymic=patronymic, tg_user=user
        )
        await message.answer("Заявка обрабатывается модератором. Пожалуйста подождите.")
        for admin in TgUser.objects.filter(is_admin=True):
            await message.bot.send_message(
                chat_id=admin.telegram_id,
                text=msg,
                reply_markup=accept_cb(user.telegram_id),
            )
        await state.clear()
