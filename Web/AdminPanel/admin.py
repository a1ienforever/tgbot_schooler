from django.contrib import admin
from unfold.admin import ModelAdmin

from Web.AdminPanel.models import TgUser, User
from Web.Schooler.models import ClassNum, Building, Person

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Администрация школы"


@admin.register(TgUser)
class TgUserAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass
