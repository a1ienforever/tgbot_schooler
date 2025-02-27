import logging

from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.filters import Command
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
from tgbot.keyboards.reply import menu_kb
from tgbot.misc.callback import (
    FrameCallback,
    ClassCallback,
    LetterCallback,
    PersonCallback,
)
from tgbot.misc.states import IncidentForm
from tgbot.services.choose import (
    choose_frame_state,
    choose_class_state,
    choose_letter_state,
)

router = Router()
persons = set()


@router.message(Command("report"))
@role_required(["director", "deputy"])
async def start_report(message: Message, user: TgUser):
    await message.answer(
        "Выберите нужный вид отчета в клавиатуре снизу", reply_markup=menu_kb()
    )


# @router.message(F.text.upper().in_("БЕЗ ФОРМЫ"))
# @role_required(["director", "deputy"])
# async def choose_start_incident(
#     message: Message,
#     user: TgUser,
#     lesson_number: int = 1,
#     state: FSMContext = None,
# ):
#     try:
#         if state:
#             await state.set_state(IncidentForm.frame)
#         text = "Пожалуйста выберите корпус для отметки ученика без формы"
#         await choose_frame_state(message, type_report="form", lesson_num=lesson_number, text=text)
#     except AiogramError as e:
#         logging.info(f"{e}")
#
#
# # сделал
# @router.callback_query(FrameCallback.filter(F.type_report == "form"))
# async def choose_frame(
#     call: CallbackQuery, callback_data: FrameCallback, user: TgUser, state: FSMContext
# ):
#     frame = callback_data.frame
#     persons.clear()
#     await state.update_data(frame=frame)
#     await choose_class_state(
#         type_report="form",
#         lesson_num=callback_data.lesson_num,
#         frame=frame,
#         call=call,
#     )
#     await state.set_state(IncidentForm.class_num)
#
#
# # сделал
# @router.callback_query(
#     ClassCallback.filter(F.type_report == "form"),
# )
# async def choose_class(
#     call: CallbackQuery, callback_data: ClassCallback, user: TgUser, state: FSMContext
# ):
#     data = await state.get_data()
#     frame = data.get("frame")
#     class_num = callback_data.class_num
#     ic()
#     ic(callback_data)
#     if class_num == 100:
#         await state.set_state(IncidentForm.frame)
#         await call.message.edit_text(
#             "Пожалуйста выберите корпус учащихся",
#             reply_markup=choose_frame_kb(
#                 type_report="form", lesson_num=callback_data.lesson_num
#             ),
#         )
#         return
#     await state.update_data(class_num=class_num)
#     await choose_letter_state(
#         frame,
#         class_num,
#         lesson_num=callback_data.lesson_num,
#         type_report="form",
#         call=call,
#     )
#
#     await state.set_state(IncidentForm.letter)
#
#
# @router.callback_query(
#     LetterCallback.filter(F.type_report == "form"),
# )
# async def choose_letter(
#         call: CallbackQuery, callback_data: LetterCallback, state: FSMContext, user: TgUser
# ):
#     class_letter = callback_data.letter
#     await state.update_data(letter=class_letter)
#     data = await state.get_data()
#     frame = data.get("frame")
#
#     if class_letter == "back":
#         await choose_class_state(
#             type_report="form",
#             lesson_num=callback_data.lesson_num,
#             frame=frame,
#             call=call,
#         )
#         await state.set_state(IncidentForm.class_num)
#         return
#
#     await call.message.edit_text(
#         "Выберите учеников (нажимайте несколько раз для выбора, затем 'Готово')",
#         reply_markup=generate_inline_keyboard(
#             type_report="form", state=data, persons=persons
#         ).as_markup(),
#     )
#     await state.set_state(IncidentForm.person)


@router.callback_query(
    PersonCallback.filter(F.type_report == "form"),
)
async def select_person(
        call: CallbackQuery, callback_data: PersonCallback, state: FSMContext, user: TgUser
):
    person_id = callback_data.person_id

    if person_id == -1:  # Если нажали кнопку "Готово"
        await process_selected_persons(persons, call)
        return

    if person_id == -2:
        await state.set_state(IncidentForm.frame)
        await call.message.edit_text(
            "Пожалуйста выберите корпус учащихся",
            reply_markup=choose_frame_kb(type_report="form", lesson_num=1),
        )
        return

    if person_id in persons:
        persons.remove(person_id)
    else:
        persons.add(person_id)

    await call.message.edit_reply_markup(reply_markup=generate_inline_keyboard(persons=persons, state=await state.get_data(), type_report='form').as_markup())


async def process_selected_persons(selected_persons, call):
    text = "\n".join([await create_person(person_id) for person_id in selected_persons])
    await call.message.edit_text(f"Запись создана:\n{text}")


async def create_person(person_id):
    person = await Person.objects.aget(id=person_id)
    text = f"{person.last_name} {person.first_name} {person.class_assigned.grade}{person.class_assigned.letter}"

    await IncidentRecord.objects.acreate(
        person_id=person, status=IncidentRecord.WITHOUT_UNIFORM
    )

    return text
