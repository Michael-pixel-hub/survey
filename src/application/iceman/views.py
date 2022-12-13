import datetime
import io

from dal import autocomplete
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.postgres.aggregates.general import ArrayAgg
from django.db.models import (OuterRef, Subquery, Count, Min, Max, FloatField, DateField, Exists, IntegerField, Sum, Q,
                              Value)
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, View, TemplateView
from xlsxwriter.workbook import Workbook
from django.core.paginator import Paginator

from application.survey.models import (UserSub, User, UserStatusIceman,
                                       Task, UserDeviceIceman)
from application.supervisor.models import UserSchedule, UserScheduleTaskExecution

from .forms import MessageForm
from .models import Notification, StoreTaskSchedule, Store, Region, StoreTask, Order
from .utils import message_reciver_filter


class MessageUsersCountView(View):

    def get(self, request):

        users_list, _ = message_reciver_filter(request, request.GET.get)

        users_count = len(users_list)

        return HttpResponse(users_count)


class MessageView(FormView):

    template_name = 'iceman/message_v2.html'
    form_class = MessageForm
    success_url = reverse_lazy('iceman:message')

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MessageView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(MessageView, self).get(request, *args, **kwargs)

    def form_valid(self, form):

        users_list, is_empty_filter = message_reciver_filter(self.request, form.cleaned_data.get)

        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        
        if is_empty_filter:
            notification = Notification()
            notification.title = title
            notification.message = message
            notification.category = 'important'
            notification.save()
        else:
            for user in users_list:

                notification = Notification()
                notification.user = user
                notification.title = title
                notification.message = message
                notification.category = 'important'
                notification.save()

        messages.success(self.request, _('The message was successfully sent out'))

        return super(MessageView, self).form_valid(form)


class ExportStoresView(View):

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):

        # Excel
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        headers = ['Источник', 'Название', 'Код', 'Регион', 'Адрес', 'Склад', 'Долгота', 'Широта', 'ИНН', 'Договор',
                   'Телефон', 'ФИО', 'Тип цены', 'Задача продажи',  'Дни доставки', 'Отсрочка', ]
        widths = [13, 30, 11, 20, 40, 15, 9, 9, 11, 13, 12, 18, 13, 19, 16, 12, ]

        header_format_dict = {'bg_color': '#eeeeee', 'bold': True, 'border': 1}
        h_fmt = workbook.add_format(header_format_dict)
        worksheet.write_row(0, 0, headers, h_fmt)
        worksheet.autofilter(0, 0, len(widths) - 1, len(widths) - 1)
        all_format_dict = {'font_size': 9, 'border': 1}
        a_fmt = workbook.add_format(all_format_dict)
        format_dict = {'num_format': 'dd.mm.yyyy hh:mm:ss', 'font_size': 9}
        fmt = workbook.add_format(format_dict)
        geo_fmt = workbook.add_format({'num_format': '0.0000000', 'font_size': 9, 'border': 1})
        worksheet.set_column(0, 0, cell_format=fmt)
        for i in range(len(widths)):
            worksheet.set_column(i, i, width=widths[i])

        # Источник
        source_id = None
        if request.POST.get('source'):
            try:
                source_id = int(request.POST['source'])
            except ValueError:
                pass

        # Регион
        region_id = None
        if request.POST.get('region'):
            try:
                region_id = int(request.POST['region'])
            except ValueError:
                pass

        # Тип
        store_type = None
        if request.POST.get('store_type'):
            store_type = request.POST['store_type']

        # Данные
        items = Store.objects.all().annotate(stocks=ArrayAgg('iceman_store_stock_store__stock__name'))
        if region_id is not None:
            items = items.filter(region_id=region_id)
        if source_id is not None:
            items = items.filter(source_id=source_id)
        if store_type is not None:
            items = items.filter(type=store_type)
        items = items.select_related('region', 'source')

        # Make Excel data
        row_num = 0
        for i in items:

            for stock in i.stocks:
                row_num += 1
                worksheet.write(row_num, 0, i.source.name, a_fmt)
                worksheet.write(row_num, 1, i.name, a_fmt)
                worksheet.write(row_num, 2, i.code if i.code is not None else '', a_fmt)
                worksheet.write(row_num, 3, i.region.name if i.region is not None else '', a_fmt)
                worksheet.write(row_num, 4, i.address, a_fmt)
                worksheet.write(row_num, 5, stock if stock is not None else '', a_fmt)
                worksheet.write(row_num, 6, i.longitude if i.longitude is not None else '', geo_fmt)
                worksheet.write(row_num, 7, i.latitude if i.latitude is not None else '', geo_fmt)
                worksheet.write(row_num, 8, i.inn, a_fmt)
                worksheet.write(row_num, 9, 'Да' if i.is_agreement else 'Нет', a_fmt)
                worksheet.write(row_num, 10, i.lpr_phone if i.lpr_phone is not None else '', a_fmt)
                worksheet.write(row_num, 11, i.lpr_fio if i.lpr_fio is not None else '', a_fmt)
                worksheet.write(row_num, 12, i.price_type if i.price_type is not None else '', a_fmt)
                worksheet.write(row_num, 13, 'Да' if i.is_order_task else 'Нет', a_fmt)
                worksheet.write(row_num, 14, i.schedule, a_fmt)
                worksheet.write(row_num, 15, i.payment_days if i.payment_days is not None else '', a_fmt)

        # Done
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename="iceman_stores_%s.xls"' % \
                                          datetime.datetime.now()
        output.close()

        return response


class ExportTasksView(View):

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):

        # Excel
        output = io.BytesIO()
        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        headers = ['Код магазина', 'Задача', 'Расписание', 'Пользователь']
        widths = [20, 20, 20, 20]

        header_format_dict = {'bg_color': '#eeeeee', 'bold': True, 'border': 1}
        h_fmt = workbook.add_format(header_format_dict)
        worksheet.write_row(0, 0, headers, h_fmt)
        worksheet.autofilter(0, 0, len(widths) - 1, len(widths) - 1)
        all_format_dict = {'font_size': 9, 'border': 1}
        a_fmt = workbook.add_format(all_format_dict)
        format_dict = {'num_format': 'dd.mm.yyyy hh:mm:ss', 'font_size': 9}
        fmt = workbook.add_format(format_dict)
        worksheet.set_column(0, 0, cell_format=fmt)
        for i in range(len(widths)):
            worksheet.set_column(i, i, width=widths[i])

        # Источник
        source_id = None
        if request.POST.get('source'):
            try:
                source_id = int(request.POST['source'])
            except ValueError:
                pass

        # Задача
        task_id = None
        if request.POST.get('task'):
            try:
                task_id = int(request.POST['task'])
            except ValueError:
                pass

        # Регион
        region_id = None
        if request.POST.get('region'):
            try:
                region_id = int(request.POST['region'])
            except ValueError:
                pass

        # Данные
        items = StoreTaskSchedule.objects.all()
        if task_id is not None:
            items = items.filter(task_id=task_id)
        if region_id is not None:
            items = items.filter(store__region_id=region_id)
        if source_id is not None:
            items = items.filter(store__source_id=source_id)
        items = items.select_related('task', 'store', 'store__region', 'store__source')

        # Make Excel data
        row_num = 0
        for i in items:
            row_num += 1
            worksheet.write(row_num, 0, i.store.code, a_fmt)
            worksheet.write(row_num, 1, i.task.name, a_fmt)
            schedule = ''
            if i.per_week is not None:
                schedule = f'*{i.per_week}'
            elif i.per_month is not None:
                schedule = f'**{i.per_month}'
            elif i.days_of_week != '':
                schedule = i.days_of_week
            elif i.is_once:
                schedule = '*'
            worksheet.write(row_num, 2, schedule, a_fmt)
            worksheet.write(row_num, 3, i.only_user.email if i.only_user else '', a_fmt)

        # Done
        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename="iceman_tasks_%s.xls"' % \
                                          datetime.datetime.now()
        output.close()

        return response


class ReportsView(TemplateView):
    template_name = 'iceman/reports.html'

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReportsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Context
        context = super(ReportsView, self).get_context_data(**kwargs)

        # Task execution report
        # context['te_report_statuses'] = TasksExecution.statuses
        # context['agent_orders_statuses'] = AgentOrder.statuses
        # context['regions'] = Region.objects.all()
        # context['loyalty_departments'] = Department.objects.filter(is_public=True)
        # context['loyalty_programs'] = Program.objects.filter(is_public=True)
        # context['taxpayers_users'] = settings.TAXPAYERS_STAFF_USERS

        # Exit
        return context


class ReportIcemansView(TemplateView):
    """
    Отчет по Icemana (отчет №3)
    """
    template_name = 'iceman/reports.icemans.html'

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReportIcemansView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        # Context
        context = super(ReportIcemansView, self).get_context_data(**kwargs)

        try:
            datetime_start = self.request.GET.get('datetime_start')
            datetime_start = datetime.datetime.strptime(datetime_start, "%d.%m.%Y")
            datetime_start = datetime_start.replace(hour=0, minute=0, second=0, microsecond=0)
        except (TypeError, ValueError):
            datetime_start = None

        try:
            datetime_end = self.request.GET.get('datetime_end')
            datetime_end = datetime.datetime.strptime(datetime_end, "%d.%m.%Y")
            datetime_end = datetime_end.replace(hour=0, minute=0, second=0, microsecond=0)
            datetime_end = datetime_end + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
        except (TypeError, ValueError):
            datetime_end = None

        try:
            region = self.request.GET.getlist('region')
        except (TypeError, ValueError):
            region = None

        try:
            superviser = self.request.GET.get('superviser')
        except (TypeError, ValueError):
            superviser = None

        try:
            statusiceman = self.request.GET.get('statusiceman')
        except (TypeError, ValueError):
            statusiceman = None

        if not datetime_start:
            datetime_start = datetime.datetime.today()
            datetime_start = datetime_start.replace(hour=0, minute=0, second=0, microsecond=0)
        if not datetime_end:
            datetime_end = datetime.datetime.today()
            datetime_end = datetime_end.replace(hour=0, minute=0, second=0, microsecond=0)
            datetime_end = datetime_end + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

        context['datetime_start'] = datetime_start
        context['datetime_end'] = datetime_end
        context['region'] = region
        context['superviser'] = superviser
        context['regions_selected'] = Region.objects.filter(id__in=region)
        context['superviser_selected'] = User.objects.filter(id=superviser)
        context['statusiceman_selected'] = UserStatusIceman.objects.filter(id=statusiceman)

        order_region_filter = {}
        if region:
            order_region_filter['store__region__in'] = region

        statusiceman_filter = {}
        if statusiceman:
            statusiceman_filter['schedule__user__status_iceman'] = statusiceman

        order_statusiceman_filter = {}
        if statusiceman:
            order_statusiceman_filter['user__status_iceman'] = statusiceman

        te_count = UserScheduleTaskExecution.objects.filter(
            schedule__date__gte=datetime_start, schedule__date__lte=datetime_end,
            schedule__user_id=OuterRef('user_id'),
            **statusiceman_filter).values('schedule__user_id').annotate(
            count=Count('schedule__user_id')).order_by().values('count')

        te_count_done = UserScheduleTaskExecution.objects.filter(
            te__isnull=False, te__date_start__gte=datetime_start,
            te__date_end__lte=datetime_end,
            schedule__user_id=OuterRef('user_id'),
            **statusiceman_filter).values('schedule__user_id').annotate(
            count=Count('schedule__user_id')).order_by().values('count')

        te_min_date = UserScheduleTaskExecution.objects.filter(
            te__isnull=False, te__date_start__gte=datetime_start, te__date_end__lte=datetime_end,
            schedule__user_id=OuterRef('user_id'),
            **statusiceman_filter).values('schedule__user_id').annotate(
            min=Min('te__date_start')).order_by().values('min')

        te_max_date = UserScheduleTaskExecution.objects.filter(
            te__isnull=False, te__date_start__gte=datetime_start, te__date_end__lte=datetime_end,
            schedule__user_id=OuterRef('user_id'),
            **statusiceman_filter).values('schedule__user_id').annotate(
            max=Max('te__date_start')).order_by().values('max')

        order_count = Order.objects.filter(
            **order_region_filter,
            **order_statusiceman_filter,
            date_create__gte=datetime_start, date_create__lte=datetime_end,
            user_id=OuterRef('user_id')
        ).values('user_id').annotate(count=Count('user_id')).order_by().values('count')

        order_sum = Order.objects.filter(
            **order_region_filter,
            **order_statusiceman_filter,
            date_create__gte=datetime_start, date_create__lte=datetime_end,
            user_id=OuterRef('user_id')
        ).values('user_id').annotate(sum=Sum('price')).order_by().values('sum')

        main_filter = {}
        if datetime_start:
            main_filter['date__gte'] = datetime_start

        if datetime_end:
            main_filter['date__lte'] = datetime_end

        if statusiceman:
            main_filter['user__status_iceman'] = statusiceman

        schedule = UserSchedule.objects.select_related('user').filter(**main_filter).values(
            'user_id', 'user__name', 'user__surname', 'user__email', 'user__status__name',
            'user__status_iceman__name').distinct().annotate(
            te_count=Subquery(te_count, output_field=IntegerField()),
            te_count_done=Subquery(te_count_done, output_field=IntegerField()),
            te_min_date=Subquery(te_min_date, output_field=DateField()),
            te_max_date=Subquery(te_max_date, output_field=DateField()),
            order_count=Subquery(order_count, output_field=IntegerField()),
            order_sum=Subquery(order_sum, output_field=FloatField()),
        )

        route_region_filter = {}

        # Отключено условие, обязывающее пользователя выбрать регион или супервайзера.
        # В шаблоне также отключена строка соответствующего предупреждения.
        # if region or (not region and not superviser):
        if region:
            route_region_filter['region__in'] = region

        superviser_filter = {}
        if superviser:
            superviser_filter['only_user_id__in'] = UserSub.objects.select_related('user_sub').filter(
                user_id=superviser).order_by('user_sub__id').distinct('user_sub__id').values('user_sub__id')

        region_users = StoreTask.objects.filter(
            only_user_id=OuterRef('user_id'),
            **route_region_filter,
            **superviser_filter
        )

        schedule = schedule.annotate(region_users=Exists(region_users)).filter(region_users=True)

        schedule = schedule.order_by('user__surname', 'user__name')

        content = []
        row = {}
        if_true = lambda x: x if x else ''
        if_true_zero = lambda x: x if x else 0
        for user in schedule:

            if user['te_count_done'] and user['te_count'] and user['te_count'] > 0:
                progress = int(user['te_count_done']/user['te_count']*100)
            else:
                progress = 0

            if progress < 33:
                progress_color = '#ec9399'
            elif progress >= 33 and progress < 66:
                progress_color = '#fbf894'
            elif progress >= 66:
                progress_color = '#98fc98'

            if user['order_sum']:
                order_sum = '{:.2f}'.format(user['order_sum'])
            else:
                order_sum = '0'

            row = {
                'user_id': user['user_id'],
                'fio': User(name=user['user__name'], surname=user['user__surname']).fio + ', '\
                           + if_true(user['user__email']) + ', ' + str(if_true(user['user__status_iceman__name'])),
                'te_count': str(if_true_zero(user['te_count'])),
                'te_count_done': str(if_true_zero(user['te_count_done'])),
                'te_min_date': user['te_min_date'],
                'te_max_date': user['te_max_date'],
                'progress': progress,
                'progress_color': progress_color,
                'order_count': if_true_zero(user['order_count']),
                'order_sum': order_sum
            }
            content.append(row)

        data_r = []
        data_r.append({'data': content})
        context['data'] = data_r

        return context

    def get(self, request, *args, **kwargs):

        response = super(ReportIcemansView, self).get(request, *args, **kwargs)

        if self.request.GET.get('export_report', None):
            
            context = self.get_context_data(*args, **kwargs)

            # Excel
            output = io.BytesIO()
            workbook = Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()

            all_format_dict = {'font_size': 9}
            a_fmt = workbook.add_format(all_format_dict)
            format_dict = {'num_format': 'dd.mm.yyyy hh:mm:ss', 'font_size': 9}
            d_fmt = workbook.add_format(format_dict)
            percent_fmt = workbook.add_format({'num_format': '0%'})

            headers = ['Торговый представитель', 'Количество возможных заданий',
                       'Количество выполненных заданий', 'Количество заказов', 'Сумма заказов',
                       'Первое задание', 'Последнее задание', 'Прогресс']
            widths = [65, 30, 30, 20, 15, 20, 20, 15]

            # Make Excel data
            row_num = 0
            for i in context['data'][0]['data']:
                row_num += 1
                worksheet.write(row_num, 0, i['fio'], a_fmt)
                worksheet.write(row_num, 1, int(i['te_count']), a_fmt)
                worksheet.write(row_num, 2, int(i['te_count_done']), a_fmt)
                worksheet.write(row_num, 3, int(i['order_count']), a_fmt)
                worksheet.write(row_num, 4, float(i['order_sum']), a_fmt)
                worksheet.write(row_num, 5, i['te_min_date'], d_fmt)
                worksheet.write(row_num, 6, i['te_max_date'], d_fmt)
                worksheet.write(row_num, 7, i['progress']/100, percent_fmt)

            header_format_dict = {'bg_color': '#eeeeee', 'bold': True, 'border': 1}
            h_fmt = workbook.add_format(header_format_dict)

            worksheet.write_row(0, 0, headers, h_fmt)
            worksheet.autofilter(0, 0, 1, len(headers) - 1)

            for i in range(len(widths)):
                worksheet.set_column(i, i, width=widths[i])

            # Done
            workbook.close()
            output.seek(0)
            response = HttpResponse(output.read(),
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'attachment; filename="report_iceman_%s.xls"' % \
                                              datetime.datetime.now()

            output.close()

        return response


class UserSubsAutocompleteView(autocomplete.Select2QuerySetView):

    def get_result_label(self, result):
        label = ''
        if result.fio.strip() != '':
            label += f'{result.fio} '
        if result.phone:
            label += f'{result.phone} '
        if result.email:
            label += f'{result.email} '
        if not label:
            label = f'Супервайзер # {result.id}'
        return label

    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.filter(
            id__in=UserSub.objects.values('user_id').order_by('user_id').distinct('user_id')
        ).order_by('surname')
        if self.q:
            qs = qs.annotate(search_name=Concat('name', Value(' '), 'surname')).filter(
                Q(surname__icontains=self.q) | Q(email__icontains=self.q) | Q(
                    phone__icontains=self.q) | Q(name__icontains=self.q))
        return qs


class RegionsAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return Region.objects.none()

        qs = Region.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class StatusIcemanAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return UserStatusIceman.objects.none()

        qs = UserStatusIceman.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class IcemanTaskListReportView(TemplateView):
    """
    Отчет по задачам торговых представителей
    """
    template_name = 'iceman/reports.iceman_task_list.html'

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IcemanTaskListReportView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        # Context
        context = super(IcemanTaskListReportView, self).get_context_data(**kwargs)

        try:
            page = self.request.GET.get('page', 1)
        except (TypeError, ValueError):
            page = 1

        try:
            datetime_start = self.request.GET.get('datetime_start')
            datetime_start = datetime.datetime.strptime(datetime_start, "%d.%m.%Y")
            datetime_start = datetime_start.replace(hour=0, minute=0, second=0, microsecond=0)
        except (TypeError, ValueError):
            datetime_start = None

        try:
            datetime_end = self.request.GET.get('datetime_end')
            datetime_end = datetime.datetime.strptime(datetime_end, "%d.%m.%Y")
            datetime_end = datetime_end.replace(hour=0, minute=0, second=0, microsecond=0)
            datetime_end = datetime_end + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
        except (TypeError, ValueError):
            datetime_end = None

        try:
            user = self.request.GET.get('id_user')
        except (TypeError, ValueError):
            user = None

        try:
            task_isdone = self.request.GET.get('task_isdone', '')
        except (TypeError, ValueError):
            task_isdone = ''

        if not datetime_start:
            datetime_start = datetime.datetime.today()
            datetime_start = datetime_start.replace(hour=0, minute=0, second=0, microsecond=0)
        if not datetime_end:
            datetime_end = datetime.datetime.today()
            datetime_end = datetime_end.replace(hour=0, minute=0, second=0, microsecond=0)
            datetime_end = datetime_end + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)

        context['datetime_start'] = datetime_start
        context['datetime_end'] = datetime_end
        context['id_user'] = user
        context['user_selected'] = User.objects.filter(id=user)
        context['task_isdone'] = task_isdone
        context['task_isdone_selected'] = task_isdone
        
        task_money = Task.objects.filter(
            id=OuterRef('task_id')).order_by().values('money')
        
        isdone_filter = {}
        if task_isdone == 'Задача выполнена':
            isdone_filter['te__isnull'] = False
        elif task_isdone == 'Задача не выполнена':
            isdone_filter['te__isnull'] = True

        user_tasks = UserScheduleTaskExecution.objects.select_related(
            'schedule__user', 'te'
        ).filter(
            schedule__date__gte=datetime_start, schedule__date__lte=datetime_end,
            schedule__user__id=user,
            **isdone_filter
        ).all()

        content = []
        row = {}
        user_obj = User.objects.filter(id=user).first()
        if_true = lambda x: x if x else ''
        if_true_zero = lambda x: x if x else 0
        if_true_hyphen = lambda x: x if x else '-'
        for task in user_tasks:

            if user_obj.status_iceman:
                status_iceman_name = ', ' + user_obj.status_iceman.name
            else:
                status_iceman_name = '' 

            if task.te:
                start_date = task.te.date_start
                end_date = task.te.date_end
                te_id = task.te.id
                te_money = task.te.money
            else:
                start_date = ''
                end_date = ''
                te_id = ''
                te_money = ''

            row = {
                'user_id': task.schedule.user.id,
                'fio': user_obj.fio + ', ' + if_true(user_obj.email) + ', ' + status_iceman_name,
                'task': task.task_name,
                'te_id': te_id,
                'route': if_true_hyphen(task.schedule.route),
                'store': task.store_code + '-' + task.store_client_name + '-' + task.store_address,
                'store_id': task.store_id,
                'date': task.schedule.date,
                'start_date': start_date,
                'end_date': end_date,
                'user_money': te_money
            }
            content.append(row)

        paginator = Paginator(content, 50)

        page_obj = paginator.get_page(page)
        context['page_obj'] = page_obj
        context['quantiy'] = len(user_tasks)

        data_r = []
        data_r.append({'data': page_obj})
        context['data'] = data_r

        return context


class TaskIsdoneAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        class TaskIsdone():
            def __init__(self, pk):#, value):
                self.pk = pk
               # self.value = value

            def __str__(self):
                return self.pk

        choice_list = [TaskIsdone('Задача выполнена'), TaskIsdone('Задача не выполнена')]

        qs = choice_list

        return qs


class UsersDeviceAutocompleteView(autocomplete.Select2QuerySetView):

    def get_result_label(self, result):
        label = ''
        if result.fio.strip() != '':
            label += f'{result.fio} '
        if result.phone:
            label += f'{result.phone} '
        if result.email:
            label += f'{result.email} '
        if not label:
            label = f'Пользователь # {result.id}'
        return label

    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.filter(id__in=UserDeviceIceman.objects.values('user__id')).all()

        if self.q:
            qs = qs.annotate(search_name=Concat('name', Value(' '), 'surname')).filter(
                Q(username__icontains=self.q) | Q(email__icontains=self.q) | Q(phone__icontains=self.q) | Q(
                    search_name__icontains=self.q))

        return qs
