# Generated by Django 5.1.1 on 2024-10-23 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AdminPanel", "0002_user_is_superuser"),
    ]

    operations = [
        migrations.CreateModel(
            name="Building",
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
                ("number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="ClassNum",
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
                ("grade", models.IntegerField()),
                ("letter", models.CharField(max_length=1)),
                (
                    "building",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.building",
                    ),
                ),
            ],
            options={
                "unique_together": {("grade", "letter")},
            },
        ),
        migrations.CreateModel(
            name="Person",
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
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("middle_name", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "class_assigned",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AdminPanel.classnum",
                    ),
                ),
            ],
        ),
    ]