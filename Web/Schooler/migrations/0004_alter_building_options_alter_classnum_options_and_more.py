# Generated by Django 5.1.1 on 2024-11-14 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Schooler", "0003_alter_building_options_alter_classnum_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="building",
            options={"verbose_name": "Корпус", "verbose_name_plural": "Корпусы"},
        ),
        migrations.AlterModelOptions(
            name="classnum",
            options={"verbose_name": "Класс", "verbose_name_plural": "Классы"},
        ),
        migrations.AlterModelOptions(
            name="person",
            options={"verbose_name": "Ученика", "verbose_name_plural": "Ученики"},
        ),
    ]
