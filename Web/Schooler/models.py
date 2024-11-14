from django.db import models


class Building(models.Model):
    number = models.IntegerField(verbose_name="Корпус")

    class Meta:
        verbose_name = "Корпус"
        verbose_name_plural = "Корпусы"

    def __str__(self):
        return f"{self.number}к"


class ClassNum(models.Model):
    grade = models.IntegerField(verbose_name="Класс")
    letter = models.CharField(max_length=1, verbose_name="Буква")
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, verbose_name="Корпус"
    )

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def __str__(self):
        return f"{self.grade}{self.letter} {self.building}"


class Person(models.Model):
    name = "Ученики"
    verbose_name = "Ученики"
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Отчество"
    )
    class_assigned = models.ForeignKey(
        ClassNum, on_delete=models.CASCADE, verbose_name="Класс учащегося"
    )

    class Meta:
        verbose_name = "Ученика"
        verbose_name_plural = "Ученики"

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name or ""}'
