from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ArchiveConfig(AppConfig):
    name = 'application.archive'
    verbose_name = _('Archive')
    label = 'archive'

    def ready(self):
        super().ready()

        # from application.archive.utils import load_te
        # load_te()
