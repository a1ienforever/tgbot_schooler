import logging

from aiogram import Router, Bot, F
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
    second_frame_class_kb,
    first_frame_class_kb,
)
from tgbot.keyboards.reply import menu_kb
from tgbot.misc.states import SchoolerCounter

router = Router()


@router.message(Command("report"))
@role_required(["director", "deputy"])
async def start_report(message: Message, user: TgUser):
    await message.answer(
        "Выберите нужный вид отчета в клавиатуре снизу", reply_markup=menu_kb()
    )


@router.message(F.text.upper().in_({"ОПОЗДАВШИЙ", "БЕЗ ФОРМЫ"}))
@role_required(["director", "deputy"])
async def choose_start_incident(
    message: Message,
    user: TgUser,
    lesson_number: int = 1,
    state: FSMContext = None,
):
    try:
        if state:
            await state.set_state(SchoolerCounter.frame)
            if message.text.upper() == "ОПОЗДАВШИЙ":
                await state.update_data(message_type="later")
            else:
                await state.update_data(message_type="without_uniform")
        await message.answer(
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(lesson_num=lesson_number),
        )
    except AiogramError as e:
        logging.info(f"{e}")


@router.callback_query(F.data.startswith("person"))
async def late_record(call: CallbackQuery, state: FSMContext, user: TgUser):
    person_id = call.data.split(":")[1]
    data = await state.get_data()
    if person_id == "back":
        await state.set_state(SchoolerCounter.class_num)
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
    if data["message_type"] == "later":
        await IncidentRecord.objects.acreate(
            person_id=person, status=IncidentRecord.LATE
        )
        await call.message.edit_text(
            f"Запись создана: \n" f"Опоздавший(-ая) {text}",
        )
    else:
        await IncidentRecord.objects.acreate(
            person_id=person, status=IncidentRecord.WITHOUT_UNIFORM
        )
        await call.message.edit_text(
            f"Запись создана: \n" f"Без формы {text}",
        )
