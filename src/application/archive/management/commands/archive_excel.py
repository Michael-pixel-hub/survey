import io

from datetime import datetime
from django.core.management.base import BaseCommand
from xlsxwriter.workbook import Workbook


class Command(BaseCommand):

    help = 'Export archive to Excel'

    def handle(self, *args, **options):

        print('Export archive to Excel ...')

        from application.archive.models import ArchiveTasksExecution

        # items
        items = ArchiveTasksExecution.objects.filter(
            date_start__range=[datetime(2021, month=12, day=1), datetime(2022, month=1, day=1)]
        ).select_related('user', 'task', 'store').order_by('date_start')

        # Excel
        workbook = Workbook('archive.xls')
        worksheet = workbook.add_worksheet()

        headers = ['Дата', 'Ид пользователя', 'Пользователь', 'Задача', 'Сумма, руб.', 'Сумма, номинал',
                   'Статус', 'Код магазина', 'Адрес', 'Чек']

        widths = [15, 19, 28, 25, 15, 15, 15, 17, 50, 18]

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
            worksheet.write(row_num, 1, i.user.id if i.user else '', a_fmt)
            worksheet.write(row_num, 2, i.user.email if i.user else '', a_fmt)
            worksheet.write(row_num, 3, i.task.name if i.task else '', a_fmt)
            worksheet.write(row_num, 4, i.money, a_fmt)
            worksheet.write(row_num, 5, i.money_source, a_fmt)
            worksheet.write(row_num, 6, i.get_status_display(), a_fmt)
            worksheet.write(row_num, 7, i.store.code if i.store else '', a_fmt)
            worksheet.write(row_num, 8, i.store.address if i.store else '', a_fmt)
            worksheet.write(row_num, 9, 'Да' if i.check else 'Нет', a_fmt)

        # Done
        workbook.close()
