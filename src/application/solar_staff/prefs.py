from preferences.registry import preferences, StringPreference, NumberPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class Salt(StringPreference):
    name = _('Salt value')
    category = _('Solar staff')


@preferences.register
class ClientId(StringPreference):
    name = _('Client id')
    category = _('Solar staff')
