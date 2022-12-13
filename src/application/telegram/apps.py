from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TelegramConfig(AppConfig):
    name = 'application.telegram'
    verbose_name = _('Telegram')
    label = 'telegram'

    def ready(self):
        super(TelegramConfig, self).ready()
        #
        # from application.survey.tasks import clear_upload_dir
        # print(clear_upload_dir())
