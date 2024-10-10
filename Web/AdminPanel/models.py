from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения")

    class Meta:
        abstract = True


class TgUser(CreatedModel):
    telegram_id = models.BigIntegerField()
    username = models.CharField(max_length=100, verbose_name="Username в тг")
    tg_fullname = models.CharField(max_length=100, verbose_name="Имя в тг")
    is_access = models.BooleanField(default=True, verbose_name="Доступ к боту")
    is_admin = models.BooleanField(default=False, verbose_name="Админ?")

    def __str__(self) -> str:
        return f'{self.telegram_id} - {self.username} - {self.tg_fullname}'

    class Meta:
        verbose_name = "Пользователи телеграмм бота"
        verbose_name_plural = 'Пользователи телеграмм бота'
        db_table = 'TgUsers'


class User(models.Model):
    tg_user = models.OneToOneField(to='TgUser', on_delete=models.CASCADE)
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    is_accept = models.BooleanField(default=False, verbose_name='Запись принята')


class Record(models.Model):
    frame = models.IntegerField(verbose_name='корпус')
    class_num = models.IntegerField(verbose_name='Класс')
    letter = models.CharField(max_length=10, verbose_name='Буква')
    count = models.IntegerField(verbose_name='Количество')
    date = models.ForeignKey('RecordDate', on_delete=models.CASCADE)
    lesson_num = models.IntegerField(verbose_name='Номер урока')


class RecordDate(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="Дата создания")


class AdminNotification(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Дата отправки')
    admin_id = models.IntegerField(verbose_name='ID администратора')
    message_id = models.IntegerField(verbose_name='ID сообщения в Telegram')
    lesson_num = models.IntegerField(verbose_name="Номер урока")


