from preferences.registry import preferences, StringPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class OrderEmail(StringPreference):
    name = _('Order e-mail')
    category = _('Agent bot')
    default = 'mail@engine2.ru'


@preferences.register
class DadataApiKey(StringPreference):
    name = _('Dadata api key')
    category = _('Agent bot')


@preferences.register
class DadataSecretKey(StringPreference):
    name = _('Dadata secret key')
    category = _('Agent bot')


@preferences.register
class EndDay(StringPreference):
    name = _('Time day ends')
    category = _('Agent bot')
    default = '18:00'
