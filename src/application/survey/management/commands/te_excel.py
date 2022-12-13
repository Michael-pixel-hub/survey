import io

from datetime import datetime
from django.core.management.base import BaseCommand
from django.db.models import (OuterRef, Subquery, Count, Min, Max, FloatField, DateField, Exists,
                              ExpressionWrapper, IntegerField, DateTimeField, CharField)
from xlsxwriter.workbook import Workbook


class Command(BaseCommand):

    help = 'Export task executions to Excel'

    def handle(self, *args, **options):

        print('Export task executions to Excel ...')

        from application.survey.models import TasksExecution, StoreTask

        # items
        users = StoreTask.objects.filter(
            only_user_id=OuterRef('user_id'),
        )

        items = TasksExecution.objects.filter(
            date_start__range=[datetime(2022, month=8, day=26), datetime(2022, month=9, day=2)],
        ).select_related('user', 'task', 'store')
        items = items.annotate(users=Exists(users)).filter(users=True).order_by('date_start')

        # Excel
        workbook = Workbook('tasks.xls')
        worksheet = workbook.add_worksheet()

        headers = ['Время начала', 'Время завершения', 'Пользователь', 'Задача', 'Код магазина', 'Адрес', 'Широта',
                   'Долгота']

        widths = [16, 21, 20, 20, 20, 50, 11, 11]

        header_format_dict = {'bg_color': '#eeeeee', 'bold': True, 'border': 1}
        h_fmt = workbook.add_format(header_format_dict)
        worksheet.write_row(0, 0, headers, h_fmt)
        worksheet.autofilter(0, 0, len(headers) - 1, len(headers) - 1)
        all_format_dict = {'font_size': 9}
        a_fmt = workbook.add_format(all_format_dict)
        format_dict = {'num_format': 'dd.mm.yyyy hh:mm:ss', 'font_size': 9}
        fmt = workbook.add_format(format_dict)
        worksheet.set_column(0, 0, cell_format=fmt)
        for i in range(len(widths)):
            worksheet.set_column(i, i, width=widths[i])

        # Make Excel data
        row_num = 0
        for i in items:
            row_num += 1
            worksheet.write(row_num, 0, i.date_start, fmt)
            worksheet.write(row_num, 1, i.date_end, fmt)
            worksheet.write(row_num, 2, i.user.email if i.user else '', a_fmt)
            worksheet.write(row_num, 3, i.task.name if i.task else '', a_fmt)
            worksheet.write(row_num, 4, i.store.code if i.store else '', a_fmt)
            worksheet.write(row_num, 5, i.store.address if i.store else '', a_fmt)
            worksheet.write(row_num, 6, i.longitude, a_fmt)
            worksheet.write(row_num, 7, i.latitude, a_fmt)

        # Done
        workbook.close()
