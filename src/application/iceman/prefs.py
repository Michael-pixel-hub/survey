from preferences.registry import preferences, StringPreference, NumberPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class Version(StringPreference):
    name = _('Version')
    category = _('Iceman')


@preferences.register
class SalesTask(NumberPreference):
    name = 'Ид задачи продажи'
    category = _('Iceman')


@preferences.register
class GetMoneyTask(NumberPreference):
    name = 'Ид задачи получить деньги'
    category = _('Iceman')
