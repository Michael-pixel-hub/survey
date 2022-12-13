from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    name = 'application.users'
    verbose_name = _("Authentication and Authorization")

    def ready(self):
        super(UsersConfig, self).ready()
