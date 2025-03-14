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
    LetterCallback, PersonCallback,
)
from tgbot.misc.states import IncidentLater, IncidentForm, IncidentSignal
from tgbot.services.choose import (
    choose_class_state,
    choose_letter_state, choose_frame_state,
)

router = Router()
persons = set()


@router.message(Command('report'))
@role_required(['director', 'deputy'])
async def start_report(message: Message, user: TgUser):
    await message.answer(
        'Выберите нужный вид отчета в клавиатуре снизу', reply_markup=menu_kb()
    )


@router.message(F.text.upper().in_(['БЕЗ ФОРМЫ', 'ОПОЗДАВШИЙ', 'СИГНАЛ']))
@role_required(['director', 'deputy'])
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
            text = 'Пожалуйста выберите корпус учащихся для отметки опоздавшего'
        elif message_type == 'БЕЗ ФОРМЫ':
            await state.set_state(IncidentForm.frame)
            text = 'Пожалуйста выберите корпус для отметки ученика без формы'
            type_report = 'form'
        elif message_type == 'СИГНАЛ':
            await state.set_state(IncidentSignal.frame)
            text = 'Пожалуйста выберите корпус для создания сигнала'
            type_report = 'signal'
        await choose_frame_state(message=message, type_report=type_report, lesson_num=lesson_number, text=text)
    except AiogramError as e:
        logging.info(f'{e}')


@router.callback_query(FrameCallback.filter(F.type_report.in_(['form', 'later', 'signal'])))
async def choose_frame(
        call: CallbackQuery, callback_data: FrameCallback, user: TgUser, state: FSMContext
):
    frame = callback_data.frame
    if callback_data.type_report == 'form':
        persons.clear()
        await state.set_state(IncidentForm.class_num)
    elif callback_data.type_report == 'later':
        await state.set_state(IncidentLater.class_num)
    elif callback_data.type_report == 'signal':
        await state.set_state(IncidentSignal.class_num)
    else:
        return

    await state.update_data(frame=frame)
    await choose_class_state(type_report=callback_data.type_report, frame=frame, call=call, lesson_num=1)


@router.callback_query(ClassCallback.filter(F.type_report.in_(['form', 'later', 'signal'])))
async def choose_class(
        call: CallbackQuery, callback_data: ClassCallback, user: TgUser, state: FSMContext
):
    data = await state.get_data()
    frame = data.get('frame')
    class_num = callback_data.class_num

    if class_num == 100:
        text = str
        if callback_data.type_report == 'form':
            await state.set_state(IncidentForm.frame)
            text = 'Пожалуйста выберите корпус для отметки ученика без формы'
        elif callback_data.type_report == 'later':
            await state.set_state(IncidentLater.frame)
            text = 'Пожалуйста выберите корпус учащихся для отметки опоздавшего'
        elif callback_data.type_report == 'signal':
            await state.set_state(IncidentSignal.frame)
            text = 'Пожалуйста выберите корпус для создания сигнала'

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
    elif callback_data.type_report == 'signal':
        await state.set_state(IncidentSignal.letter)


@router.callback_query(LetterCallback.filter(F.type_report.in_(['form', 'later', 'signal'])))
async def choose_letter(
        call: CallbackQuery, callback_data: LetterCallback, state: FSMContext, user: TgUser
):
    class_letter = callback_data.letter
    await state.update_data(letter=class_letter)
    data = await state.get_data()
    frame = data.get('frame')

    if class_letter == 'back':
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
        elif callback_data.type_report == 'signal':
            await state.set_state(IncidentSignal.frame)
        return

    if callback_data.type_report == 'form':
        await call.message.edit_text(
            'Выберите учеников (нажимайте несколько раз для выбора, затем "Готово")',
            reply_markup=generate_inline_keyboard(
                type_report=callback_data.type_report, state=data, persons=persons
            ).as_markup(),
        )
        await state.set_state(IncidentForm.person)
    elif callback_data.type_report == 'signal':

        await call.message.edit_text('Выберите учеников (нажимайте несколько раз для выбора, затем "Готово")',
                                     reply_markup=generate_inline_keyboard(
                                         type_report=callback_data.type_report, state=data, persons=persons
                                     ).as_markup())
        await state.set_state(IncidentSignal.person)

    elif callback_data.type_report == 'later':
        await call.message.edit_text(
            'Выберите имя ученика',
            reply_markup=generate_inline_keyboard(
                type_report=callback_data.type_report, state=data, persons=set()
            ).as_markup(),
        )
        await state.set_state(IncidentLater.person)


@router.callback_query(
    PersonCallback.filter(F.type_report.in_(['later'])),
)
async def late_record(
        call: CallbackQuery, callback_data: PersonCallback, state: FSMContext, user: TgUser
):
    person_id = callback_data.person_id

    if person_id == -2:
        await state.set_state(IncidentLater.frame)
        await call.message.edit_text(
            'Пожалуйста выберите корпус учащихся',
            reply_markup=choose_frame_kb(type_report=callback_data.type_report, lesson_num=1),
        )
        return

    await create_person(person_id, callback_data.type_report)

    await state.clear()
    await process_selected_persons([person_id], call, callback_data.type_report)

@router.callback_query(
    PersonCallback.filter(F.type_report.in_(['form'])),
)
async def without_form_record(
        call: CallbackQuery, callback_data: PersonCallback, state: FSMContext, user: TgUser
):
    person_id = callback_data.person_id
    if person_id == -1:  # Если нажали кнопку 'Готово'
        await process_selected_persons(persons, call, callback_data.type_report)
        persons.clear()
        await state.clear()
        return
    if person_id == -2:
        await state.set_state(IncidentForm.frame)
        await call.message.edit_text(
            'Пожалуйста выберите корпус учащихся',
            reply_markup=choose_frame_kb(type_report='form', lesson_num=1),
        )
        return

    if person_id in persons:
        persons.remove(person_id)
    else:
        persons.add(person_id)
    await call.message.edit_reply_markup(
        reply_markup=generate_inline_keyboard(persons=persons, state=await state.get_data(),
                                              type_report='form').as_markup())



async def process_selected_persons(selected_persons, call, type_report):
    text = '\n'.join([await create_person(person_id, type_report) for person_id in selected_persons])
    await call.message.edit_text(f'Запись создана:\n{text}')


async def create_person(person_id, type_report):
    person = await Person.objects.aget(id=person_id)
    text = f'{person.last_name} {person.first_name} {person.class_assigned.grade}{person.class_assigned.letter}'
    if type_report == 'form':
        await IncidentRecord.objects.acreate(
            person_id=person, status=IncidentRecord.WITHOUT_UNIFORM
        )
    elif type_report == 'later':
        await IncidentRecord.objects.acreate(
            person_id=person, status=IncidentRecord.LATE
        )
    elif type_report == 'signal':
        pass

    return text


