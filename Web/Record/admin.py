from django.contrib import admin

from Web.Record.models import Record, IncidentRecord



# # Register your models here.
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_filter = ('frame', 'class_num', 'letter', 'lesson_num')


@admin.register(IncidentRecord)
class IncidentRecordAdmin(admin.ModelAdmin):
    list_filter = ['status']