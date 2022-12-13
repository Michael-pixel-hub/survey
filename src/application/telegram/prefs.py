from preferences.registry import preferences, StringPreference, NumberPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class BotToken(StringPreference):
    name = _('Bot token')
    category = _('Telegram')


@preferences.register
class BotName(StringPreference):
    name = _('Bot name')
    category = _('Telegram')


@preferences.register
class SiteUrl(StringPreference):
    name = _('Site url')
    category = _('Site')


@preferences.register
class AppmetricaApikey(StringPreference):
    name = _('AppMetrica Apikey')
    category = _('Telegram')


@preferences.register
class GoodsPerPage(NumberPreference):
    name = _('Goods per page')
    category = _('Telegram')
    default = 15
