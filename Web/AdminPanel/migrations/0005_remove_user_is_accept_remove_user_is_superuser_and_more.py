# Generated by Django 5.1.1 on 2024-11-12 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AdminPanel", "0004_remove_classnum_building_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_accept",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_superuser",
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("director", "Директор"),
                    ("deputy", "Завуч"),
                    ("teacher", "Учитель"),
                ],
                max_length=10,
                null=True,
            ),
        ),
    ]
