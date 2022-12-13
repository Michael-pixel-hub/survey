"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'src.menu.CustomMenu'
"""

from django.conf import settings
try:
    from django.urls import reverse, reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu

from preferences.utils import get_setting


class CustomMenu(Menu):
    """
    Custom Menu for src admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)

    def init_with_context(self, context):

        is_superuser = context['user'].is_superuser
        is_task_user = context['user'].email in settings.ADD_TASK_USERS

        bot_url = 'https://t.me/%s' % get_setting('telegram_botname')
        bot_url_profi = 'https://t.me/%s' % get_setting('profi_botname')

        if is_superuser:

            imports = [items.MenuItem(_('Import data'), reverse_lazy('survey:import'))]
            if is_task_user:
                imports += [items.MenuItem(_('Import tasks'), reverse_lazy('survey:import-tasks'))]

            self.children += [
                items.MenuItem(_('Dashboard'), reverse('admin:index')),
                items.Bookmarks(),
                items.MenuItem(
                    _('Export/Import'),
                    children=imports + [
                        items.MenuItem(_('Export data'), reverse_lazy('survey:export')),
                        items.MenuItem(_('Download images'), reverse_lazy('survey:download_images')),
                    ]
                ),
                items.MenuItem(_('Reports'), reverse_lazy('survey:reports')),
                items.ModelList(
                    _('Chistaya liniya'),
                    models=('application.survey.*', )
                ),
                items.MenuItem(
                    _('Telegram'),
                    children=(
                        items.MenuItem(_('Run bot'), bot_url),
                        items.MenuItem(_('Sending messages'), reverse_lazy('telegram:message')),
                        items.MenuItem(_('Sending messages group'), reverse_lazy('telegram:message_group')),
                        items.MenuItem(_('Sending messages stores'), reverse_lazy('telegram:message_stores')),
                        items.ModelList(
                            _('Applications'),
                            models=('application.telegram.*',)
                        )
                    )
                ),
                items.MenuItem(
                    _('Mobile app'),
                    children=(
                        items.MenuItem(_('Sending messages'), reverse_lazy('mobile:message')),
                        items.ModelList(
                            _('Applications'),
                            models=('application.mobile.*', 'application.survey.models.all.UserDevice')
                        )
                    )
                ),
                items.MenuItem(
                    _('Iceman'),
                    children=(
                        items.MenuItem(_('Sending messages'), reverse_lazy('iceman:message')),
                        items.MenuItem(_('Import stores'), reverse_lazy('iceman-imports:import-stores')),
                        items.MenuItem(_('Import products'), reverse_lazy('iceman-imports:import-products')),
                        items.MenuItem(_('Import tasks'), reverse_lazy('iceman-imports:import-tasks')),
                        items.MenuItem(_('Reports'), reverse_lazy('iceman:reports')),
                        items.ModelList(
                            _('Mobile application'),
                            models=('application.survey.models.all.UserDeviceIceman',
                                    'application.iceman.models.Notification', )
                        ),
                        items.ModelList(
                            _('Data'),
                            models=('application.iceman.models.Source', 'application.iceman.models.Region',
                                    'application.iceman.models.Stock', 'application.iceman.models.Store',
                                    'application.iceman.models.Document', 'application.iceman.models.DocumentGroup',
                                    'application.iceman.models.Brand', 'application.iceman.models.Category',
                                    'application.iceman.models.Product', 'application.iceman.models.SourceProduct',
                                    'application.iceman.models.StoreTask', 'application.iceman.models.StoreTaskSchedule'
                                    )
                        ),
                        items.ModelList(
                            _('Orders'),
                            models=('application.iceman.models.Order', )
                        ),
                        items.ModelList(
                            _('Payments'),
                            models=('application.agent.models.TinkoffPayment',)
                        ),
                        items.ModelList(
                            _('Manage'),
                            models=('application.iceman_imports.models.ImportStores',
                                    'application.iceman_imports.models.ImportProducts',
                                    'application.iceman_imports.models.ImportTasks',
                                    'application.iceman_imports.models.UploadRequest'),
                        ),
                    )
                ),
                items.ModelList(
                    _('Agent'),
                    models=('application.agent.*',),
                    # children=(
                    #     items.MenuItem(_('Import data'), reverse_lazy('agent:import')),
                    #     items.ModelList(
                    #         _('Applications'),
                    #         models=('application.agent.*',)
                    #     )
                    # )
                ),
                items.ModelList(
                    _('Loyalty'),
                    models=('application.loyalty.*',),
                ),
                # items.MenuItem(
                #     _('Profi bot'),
                #     children=(
                #         items.MenuItem(_('Run bot'), bot_url_profi),
                #         items.MenuItem(_('Sending messages'), reverse_lazy('profi:message')),
                #         items.ModelList(
                #             _('Applications'),
                #             models=('application.profi.*',)
                #         )
                #     )
                # ),
                items.ModelList(
                    _('Administration'),
                    models=('django.contrib.auth.*', 'application.users.models.User', 'preferences.*', 'cache_model.*', ),
                ),
            ]

        else:

            self.children += [
                items.MenuItem(_('Dashboard'), reverse('admin:index')),
                items.Bookmarks(),
                items.ModelList(
                    _('Chistaya liniya'),
                    models=('application.survey.*', )
                ),
                items.ModelList(
                    _('Telegram'),
                    models=('application.telegram.*',)
                ),
                items.ModelList(
                    _('Profi bot'),
                    models=('application.profi.*',)
                ),
                items.ModelList(
                    _('Administration'),
                    models=('django.contrib.auth.*', 'users.models.User', 'preferences.*', 'cache_model.*', ),
                ),
            ]

        return super(CustomMenu, self).init_with_context(context)
