from preferences.registry import preferences, StringPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class Version(StringPreference):
    name = _('Version')
    category = _('Mobile app')
