from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DumpConfig(AppConfig):
    name = 'application.dump'
    verbose_name = _('Dump')
    label = 'dump'

    def ready(self):
        super(DumpConfig, self).ready()

        # import datetime
        # start_date = datetime.datetime.now()
        # from application.archive.utils import make_archive
        # print(make_archive(start_date))
