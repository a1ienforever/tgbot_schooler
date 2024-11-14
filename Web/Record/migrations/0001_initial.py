# Generated by Django 5.1.1 on 2024-10-23 16:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RecordDate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateField(auto_now_add=True, verbose_name="Дата создания"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Record",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("frame", models.IntegerField(verbose_name="корпус")),
                ("class_num", models.IntegerField(verbose_name="Класс")),
                ("letter", models.CharField(max_length=10, verbose_name="Буква")),
                ("count", models.IntegerField(verbose_name="Количество")),
                ("lesson_num", models.IntegerField(verbose_name="Номер урока")),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Record.recorddate",
                    ),
                ),
            ],
        ),
    ]