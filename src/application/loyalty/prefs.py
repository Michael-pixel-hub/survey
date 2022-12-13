from preferences.registry import preferences, StringPreference
from django.utils.translation import ugettext_lazy as _


@preferences.register
class TelegramChannelId(StringPreference):
    name = _('Telegram channel Id')
    category = _('Loyalty bot')
