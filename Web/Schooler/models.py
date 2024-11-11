from django.db import models


class Building(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f"{self.number}к"


class ClassNum(models.Model):
    grade = models.IntegerField()
    letter = models.CharField(max_length=1)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.grade}{self.letter} {self.building}"


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    class_assigned = models.ForeignKey(ClassNum, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name or ""}'
