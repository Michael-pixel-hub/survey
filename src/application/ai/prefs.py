from preferences.registry import preferences, StringPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class Url(StringPreference):
    name = _('Url')
    category = _('Shop Survey AI')


@preferences.register
class Token(StringPreference):
    name = _('Token')
    category = _('Shop Survey AI')
