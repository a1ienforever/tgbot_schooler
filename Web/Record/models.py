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

    def __str__(self):
        return f'{self.class_num}{self.letter} - {self.count}'

    class Meta:
        verbose_name = 'Запись количества отсутствующих'
        verbose_name_plural = 'Записи количества отсутствующих'

class RecordDate(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')


class Signal(models.Model):
    msg = models.CharField(max_length=500)

    def __str__(self):
        return self.msg

class IncidentRecord(models.Model):
    WITHOUT_UNIFORM = 'Без формы'
    LATE = 'Опоздал'
    SIGNAL = 'Сигнал'

    STATUS_CHOICES = [
        (WITHOUT_UNIFORM, 'Без формы'),
        (LATE, 'Опоздал'),
        (SIGNAL, 'Сигнал')
    ]

    date = models.DateField(
        auto_now_add=True,
    )
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Учащийся')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус')
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Сигнал')


    def __str__(self):
        return f'{self.person_id.last_name} {self.person_id.first_name} - {self.status}'

    class Meta:
        verbose_name = 'Запись о нарушение правил'
        verbose_name_plural = 'Записи о нарушение правил'


