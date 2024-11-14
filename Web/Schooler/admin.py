from django.contrib import admin

from Web.Schooler.models import Person, ClassNum, Building
from unfold.admin import ModelAdmin


# Register your models here.


@admin.register(Person)
class PersonAdmin(ModelAdmin):
    ordering = ["last_name"]
    search_fields = [
        "last_name__startswith",
        "first_name__startswith",
        "middle_name__startswith",
        "class_assigned__grade",
    ]


@admin.register(ClassNum)
class ClassAdmin(ModelAdmin):
    ordering = ["grade"]
    search_fields = ["grade", "letter", "building__number"]


@admin.register(Building)
class BuildingAdmin(ModelAdmin):
    ordering = ["number"]
    search_fields = ["number"]
