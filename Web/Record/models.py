from django.db import models

from Web.Schooler.models import Person


# Create your models here.
class Record(models.Model):
    frame = models.IntegerField(verbose_name="корпус")
    class_num = models.IntegerField(verbose_name="Класс")
    letter = models.CharField(max_length=10, verbose_name="Буква")
    count = models.IntegerField(verbose_name="Количество")
    date = models.ForeignKey("RecordDate", on_delete=models.CASCADE)
    lesson_num = models.IntegerField(verbose_name="Номер урока")


class RecordDate(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="Дата создания")


class IncidentRecord(models.Model):
    WITHOUT_UNIFORM = "Без формы"
    LATE = "Опоздал"

    STATUS_CHOICES = [
        (WITHOUT_UNIFORM, "Без формы"),
        (LATE, "Опоздал"),
    ]

    date = models.DateField(
        auto_now_add=True,
    )
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
