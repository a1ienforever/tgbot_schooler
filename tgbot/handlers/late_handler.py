from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from Web.AdminPanel.models import TgUser
from tgbot.keyboards.reply import menu_kb

router = Router()


@router.message(Command('report'))
async def start_report(message: Message, user: TgUser):
    await message.answer("Выберите нужный вид отчета в клавиатуре снизу", reply_markup=menu_kb())

