# Generated by Django 5.1.1 on 2024-11-11 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Record", "0001_initial"),
        ("Schooler", "0002_alter_classnum_unique_together"),
    ]

    operations = [
        migrations.CreateModel(
            name="LatecomerRecord",
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
                ("date", models.DateField(auto_now_add=True)),
                (
                    "person_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Schooler.person",
                    ),
                ),
            ],
        ),
    ]
