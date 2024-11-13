import datetime

from asgiref.sync import sync_to_async
from django.db import transaction
from django.utils import timezone

from Web.AdminPanel.models import AdminNotification, TgUser
from Web.Record.models import RecordDate, Record, IncidentRecord
from Web.Schooler.models import ClassNum, Person, Building


async def add_person(
    first_name, last_name, class_num, letter, building, middle_name=None
):
    # Получаем или создаем корпус
    building_obj, _ = await Building.objects.aget_or_create(number=building)

    # Получаем или создаем класс
    class_assigned_obj, _ = await ClassNum.objects.aget_or_create(
        grade=class_num, letter=letter, building=building_obj
    )

    # Создаем или получаем пользователя
    await Person.objects.aget_or_create(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        class_assigned=class_assigned_obj,
    )


def clear_database_schooler():
    # Удаление данных всех моделей
    Person.objects.all().delete()
    ClassNum.objects.all().delete()
    Building.objects.all().delete()


async def create_record(
    frame,
    class_num,
    letter,
    count,
    lesson_num,
    record_date=None,
):

    if record_date is None:
        record_date = datetime.date.today()

    record_date_obj, created = await RecordDate.objects.aget_or_create(date=record_date)

    new_record = Record.objects.create(
        frame=frame,
        class_num=class_num,
        letter=letter,
        count=count,
        date=record_date_obj,
        lesson_num=lesson_num,
    )

    return new_record


@sync_to_async
def create_notification(today, admin, sent_message, lesson_num):
    with transaction.atomic():
        return AdminNotification.objects.create(
            date=today,
            admin_id=admin.telegram_id,
            message_id=sent_message.message_id,
            lesson_num=lesson_num,
        )


@sync_to_async
def get_notification(today, admin, lesson_num):
    return AdminNotification.objects.filter(
        date=today, admin_id=admin.telegram_id, lesson_num=lesson_num
    ).first()


@sync_to_async
def get_records(today, lesson_num):
    return Record.objects.filter(date__date=today, lesson_num=lesson_num).order_by(
        "frame", "class_num"
    )


@sync_to_async
def get_incidents():
    now = timezone.now()
    start_of_week = now - datetime.timedelta(days=now.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=7)

    recent_records_late = IncidentRecord.objects.filter(
        date__gte=start_of_week, date__lt=end_of_week, status=IncidentRecord.LATE
    ).order_by(
        "date",
        "person_id__last_name",
        "person_id__class_assigned__building",
        "person_id__class_assigned",
    )

    recent_records_uniform = IncidentRecord.objects.filter(
        date__gte=start_of_week,
        date__lt=end_of_week,
        status=IncidentRecord.WITHOUT_UNIFORM,
    ).order_by(
        "date", "person_id__class_assigned__building", "person_id__class_assigned"
    )

    return recent_records_late, recent_records_uniform


@sync_to_async
def get_admins():
    return TgUser.objects.filter(is_admin=True)
