from django.contrib import admin
from unfold.admin import ModelAdmin



admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Администрация школы"
admin.site.name = "Администрация школы"
admin.site.site_title = "Администрация школы"

from django.contrib.auth.models import Group, User
admin.site.unregister(Group)
admin.site.unregister(User)


from Web.AdminPanel.models import TgUser, User
@admin.register(TgUser)
class TgUserAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass
