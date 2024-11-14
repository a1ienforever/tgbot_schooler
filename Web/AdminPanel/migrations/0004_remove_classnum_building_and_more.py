# Generated by Django 5.1.1 on 2024-10-23 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("AdminPanel", "0003_building_classnum_person"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="classnum",
            name="building",
        ),
        migrations.AlterUniqueTogether(
            name="classnum",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="person",
            name="class_assigned",
        ),
        migrations.RemoveField(
            model_name="record",
            name="date",
        ),
        migrations.DeleteModel(
            name="Building",
        ),
        migrations.DeleteModel(
            name="ClassNum",
        ),
        migrations.DeleteModel(
            name="Person",
        ),
        migrations.DeleteModel(
            name="Record",
        ),
        migrations.DeleteModel(
            name="RecordDate",
        ),
    ]