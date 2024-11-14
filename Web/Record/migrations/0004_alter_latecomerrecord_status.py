# Generated by Django 5.1.1 on 2024-11-11 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Record", "0003_latecomerrecord_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="latecomerrecord",
            name="status",
            field=models.CharField(
                choices=[("Без формы", "Без формы"), ("Опоздал", "Опоздал")],
                max_length=20,
            ),
        ),
    ]
