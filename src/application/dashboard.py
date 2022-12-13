"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'src.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'src.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
try:
    from django.urls import reverse, reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

from preferences.utils import get_setting


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for src.
    """
    def init_with_context(self, context):

        site_name = get_admin_site_name(context)

        bot_url = 'https://t.me/%s' % get_setting('telegram_botname')
        bot_url_profi = 'https://t.me/%s' % get_setting('profi_botname')

        is_superuser = context['user'].is_superuser
        is_task_user = context['user'].email in settings.ADD_TASK_USERS

        # append a link list module for "quick links"
        imports = [[_('Import data'), reverse_lazy('survey:import')], ]
        if is_task_user:
            imports += [[_('Import tasks'), reverse_lazy('survey:import-tasks')], ]
            imports += [['Сменить пароль пользователю', reverse_lazy('users:password')], ]
        if is_superuser:
            self.children.append(modules.LinkList(
                _('Quick links'),
                layout='inline',
                draggable=False,
                deletable=False,
                collapsible=False,
                children=imports + [
                    [_('Export data'), reverse_lazy('survey:export')],
                    [_('Download images'), reverse_lazy('survey:download_images')],
                    [_('Reports'), reverse_lazy('survey:reports')],
                    [_('Log out'), reverse('%s:logout' % site_name)],
                ]
            ))
        elif context['user'].task.values_list('id', flat=True):
            self.children.append(modules.LinkList(
                _('Quick links'),
                layout='inline',
                draggable=False,
                deletable=False,
                collapsible=False,
                children=[
                    [_('Reports'), reverse_lazy('survey:reports')],
                    [_('Download images'), reverse_lazy('survey:download_images')],
                    [_('Change password'),
                     reverse('%s:password_change' % site_name)],
                    [_('Log out'), reverse('%s:logout' % site_name)],
                ]
            ))
        else:
            self.children.append(modules.LinkList(
                _('Quick links'),
                layout='inline',
                draggable=False,
                deletable=False,
                collapsible=False,
                children=[
                    [_('Change password'),
                     reverse('%s:password_change' % site_name)],
                    [_('Log out'), reverse('%s:logout' % site_name)],
                ]
            ))

        # append an app list module for "Applications"

        self.children.append(modules.Group(
            title=_('Users'),
            display='tabs',
            children=(
                modules.AppList(
                    _('Data'),
                    models=('application.survey.models.all.User', 'application.solar_staff.models.SolarStaffPayments',
                            'application.survey.models.all.Rank',
                            'application.survey.models.te.Act', 'application.solar_staff.models.Payment',
                            'application.survey.models.all.UserDelete',
                            'application.survey.models.te.Penalty'),
                ),
                modules.AppList(
                    'Справочники',
                    models=('application.survey.models.all.UserStatus',
                            'application.survey.models.all.UserStatusIceman', 'application.survey.models.all.Bank'),
                ),
            )
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Chistaya liniya'),
            models=('application.survey.models.all.Category', 'application.survey.models.all.Region',
                    'application.survey.models.all.Client', 'application.survey.models.all.Store',
                    'application.survey.models.all.Good', 'application.survey.models.all.Assortment',
                    'application.survey.models.all.Agreement', 'application.survey.models.all.StoreTask',
                    'application.survey.models.te.StoreTaskAvail', ),
        ))

        # append an app list module for "Applications"
        self.children.append(modules.Group(
            title=_('Tasks'),
            display='tabs',
            children=(
                modules.AppList(
                    _('Tasks'),
                    models=('application.survey.models.all.Task', 'application.survey.models.all.TaskCustomer',
                            'application.survey.models.all.TaskQuestionnaire',
                            'application.survey.models.te.TasksExecution',
                            'application.survey.models.te.TasksExecutionInspector',
                            'application.survey.models.te.TasksExecutionCheck',
                            'application.survey.models.te.TasksExecutionCheckInspector',
                            'application.survey.models.te.ActCheck'),
                ),
                modules.AppList(
                    _('Archive'),
                    models=('application.archive.models.ArchiveTasksExecution', ),
                ),
                modules.AppList(
                    'Справочники',
                    models=('application.survey.models.all.OutReason', 'application.ai.models.AIProject'),
                ),                
            )
        ))

        # self.children.append(modules.AppList(
        #     _('Tasks'),
        #     models=('application.survey.models.all.Task', 'application.survey.models.all.TaskCustomer',
        #             'application.survey.models.te.TasksExecution', 'application.survey.models.te.TasksExecutionCheck',
        #             'application.archive.models.ArchiveTasksExecution'),
        # ))

        # append an app list module for "Applications"
        if is_superuser:
            self.children.append(modules.Group(
                title=_('Telegram bot'),
                display='tabs',
                children=(
                    modules.LinkList(
                        _('Quick links'),
                        layout='inline',
                        draggable=False,
                        deletable=False,
                        collapsible=False,
                        children=[
                            [_('Run bot'), bot_url],
                            [_('Sending messages'), reverse_lazy('telegram:message')],
                            [_('Sending messages group'), reverse_lazy('telegram:message_group')],
                            [_('Sending messages stores'), reverse_lazy('telegram:message_stores')],
                        ]
                    ),
                    modules.AppList(
                        _('Channels'),
                        models=('application.telegram.models.Channel',),
                    ),
                    modules.AppList(
                        _('Manage'),
                        models=('application.telegram.models.String', 'application.telegram.models.Menu',),
                    )
                )
            ))

        # append an app list module for "Applications"
        if is_superuser:
            self.children.append(modules.Group(
                title=_('Mobile app'),
                display='tabs',
                children=(
                    modules.LinkList(
                        _('Quick links'),
                        layout='inline',
                        draggable=False,
                        deletable=False,
                        collapsible=False,
                        children=[
                            [_('Sending messages'), reverse_lazy('mobile:message')],
                        ]
                    ),
                    modules.AppList(
                        _('Data'),
                        models=('application.survey.models.all.UserDevice', 'application.mobile.models.Notification',),
                    ),
                )
            ))

        # append an app list module for "Applications"
        if is_superuser:
            self.children.append(modules.Group(
                title=_('Iceman'),
                display='tabs',
                children=(
                    modules.LinkList(
                        _('Quick links'),
                        layout='inline',
                        draggable=False,
                        deletable=False,
                        collapsible=False,
                        children=[
                            [_('Sending messages'), reverse_lazy('iceman:message')],
                            [_('Import stores'), reverse_lazy('iceman-imports:import-stores')],
                            [_('Import products'), reverse_lazy('iceman-imports:import-products')],
                            [_('Import tasks'), reverse_lazy('iceman-imports:import-tasks')],
                            [_('Reports'), reverse_lazy('iceman:reports')],
                        ]
                    ),
                    modules.ModelList(
                        _('Orders'),
                        models=('application.iceman.models.Order', )
                    ),
                    modules.AppList(
                        _('Mobile application'),
                        models=('application.survey.models.all.UserDeviceIceman',
                                'application.iceman.models.Notification',)
                    ),
                    modules.ModelList(
                        _('Data'),
                        models=('application.iceman.models.Source', 'application.iceman.models.Region',
                                'application.iceman.models.Stock', 'application.iceman.models.Store',
                                'application.iceman.models.Document', 'application.iceman.models.DocumentGroup',
                                'application.iceman.models.Brand',
                                'application.iceman.models.Category', 'application.iceman.models.Product',
                                'application.iceman.models.SourceProduct', 'application.iceman.models.StoreTask',
                                'application.iceman.models.StoreTaskSchedule')
                    ),
                    modules.AppList(
                        _('Payments'),
                        models=('application.agent.models.TinkoffPayment',),
                    ),
                    modules.AppList(
                        _('Manage'),
                        models=('application.iceman_imports.models.ImportStores',
                                'application.iceman_imports.models.ImportProducts',
                                'application.iceman_imports.models.ImportTasks',
                                'application.iceman_imports.models.UploadRequest'),
                    ),
                )
            ))

        # append an app list module for "Applications"
        if is_superuser:
            self.children.append(modules.Group(
                title=_('Loyalty bot'),
                display='tabs',
                children=(
                    modules.AppList(
                        _('Data'),
                        models=('application.loyalty.models.Department', 'application.loyalty.models.Program',
                                'application.loyalty.models.Store', 'application.agent.models.PromoCode', ),
                    ),
                )
            ))

        # append an app list module for "Applications"
        if is_superuser:
            self.children.append(modules.Group(
                title=_('Agent'),
                display='tabs',
                children=(
                    modules.AppList(
                        _('User data'),
                        models=('application.agent.models.Store', 'application.agent.models.Order'),
                    ),
                    modules.AppList(
                        _('Data'),
                        models=('application.agent.models.Category', 'application.agent.models.Brand',
                                'application.agent.models.Good', 'application.agent.models.City',
                                'application.agent.models.Schedule', 'application.agent.models.StoreCategory'),
                    ),
                    modules.AppList(
                        _('Manage'),
                        models=('application.agent.models.Import', ),
                    ),
                    modules.AppList(
                        _('Payments'),
                        models=('application.agent.models.Payment', 'application.agent.models.TinkoffPayment',),
                    ),
                )
            ))

        # # append an app list module for "Applications"
        # if is_superuser:
        #     self.children.append(modules.Group(
        #         title=_('Telegram profi bot'),
        #         display='tabs',
        #         children=(
        #             modules.LinkList(
        #                 _('Quick links'),
        #                 layout='inline',
        #                 draggable=False,
        #                 deletable=False,
        #                 collapsible=False,
        #                 children=[
        #                     [_('Run bot'), bot_url_profi],
        #                     [_('Sending messages'), reverse_lazy('profi:message')],
        #                 ]
        #             ),
        #             modules.AppList(
        #                 _('Data'),
        #                 models=('application.profi.models.User', 'application.profi.models.Task',
        #                         'application.profi.models.Report', 'application.profi.models.Order'),
        #             ),
        #             modules.AppList(
        #                 _('Manage'),
        #                 models=('application.profi.models.String', 'application.profi.models.Menu',),
        #             ),
        #         )
        #     ))

        # append an app list module for "Administration"
        if is_superuser:
            self.children.append(modules.Group(
                title=_('Administration'),
                display='tabs',
                children=(
                    modules.AppList(
                        _('Authentication'),
                        models=('application.users.models.User', 'django.contrib.auth.*',
                                'django.contrib.admin.models.LogEntry', ),
                    ),
                    modules.AppList(
                        _('API'),
                        models=('rest_framework.authtoken.*',),
                    ),
                    modules.AppList(
                        _('Import'),
                        models=('application.survey.models.all.Import',),
                    ),
                    modules.AppList(
                        _('System management'),
                        models=('cache_model.*',)
                    ),
                    modules.AppList(
                        _('Requests'),
                        models=('application.survey.models.all.UploadRequests',
                                'application.survey.models.all.ExternalRequests',
                                'application.survey.models.all.Request',
                                'application.survey.models.all.Sms'),
                    ),
                    modules.AppList(
                        _('Settings'),
                        models=('preferences.*', 'application.solar_staff_accounts.models.SolarStaffAccount', ),
                    ),
                ),
            ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

        # # append another link list module for "support".
        # if is_superuser:
        #     self.children.append(modules.LinkList(
        #         _('Support'),
        #         children=[
        #             {
        #                 'title': _('Support telegram'),
        #                 'url': 'https://t.me/mr_rown',
        #                 'external': True,
        #             },
        #         ]
        #     ))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for src.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
