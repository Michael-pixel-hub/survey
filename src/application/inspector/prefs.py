from preferences.registry import preferences, StringPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class Url(StringPreference):
    name = _('Url')
    category = _('Inspector')


@preferences.register
class Token(StringPreference):
    name = _('Token')
    category = _('Inspector')
