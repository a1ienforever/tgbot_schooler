import datetime

from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class DateRangeFilter(SimpleListFilter):
    title = _('Дата')
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return [
            ('today', _('Сегодня')),
            ('past_7_days', _('Последние 7 дней')),
            ('this_month', _('Этот месяц')),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'today':
            return queryset.filter(date=datetime.date.today())
        elif value == 'past_7_days':
            return queryset.filter(date__gte=datetime.date.today() - datetime.timedelta(days=7))
        elif value == 'this_month':
            start_date = datetime.date.today().replace(day=1)
            return queryset.filter(date__gte=start_date)
        return queryset