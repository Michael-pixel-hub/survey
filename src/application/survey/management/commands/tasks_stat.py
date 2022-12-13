import pandas as pd

from application.survey.models import TasksExecution
from datetime import datetime, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from pathlib import Path
from xlsxwriter.workbook import Workbook


class Command(BaseCommand):

    help = 'Collect tasks stats'

    def handle(self, *args, **options):

        print('Collect tasks stats...')

        # Подготавливаем
        date_start = datetime.now() - timedelta(days=90)

        # Новый файл
        excel_file = Path(settings.DATA_DIR) / 'tasks_stat_fill.xlsx'
        workbook = Workbook(excel_file)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ['Код клиента', 'Задание', 'Мин время, сек', 'Макс время, сек', 'Среднее время, сек'])

        # Читаем файл
        exists_excel_file = Path(settings.DATA_DIR) / 'tasks_stat.xlsx'
        df = pd.read_excel(exists_excel_file, header=0)

        for index, row in df.iterrows():

            store_code = row['Код клиента']
            task_name = row['Задание']

            tasks = TasksExecution.objects.filter(
                task__name=task_name, store__code=store_code, date_start__gte=date_start, date_end__isnull=False
            ).select_related('task', 'store')

            max_time = None
            min_time = None
            sum_times = 0

            for task in tasks:
                seconds = (task.date_end - task.date_start).seconds
                if max_time is None or max_time < seconds:
                    max_time = seconds
                if min_time is None or min_time > seconds:
                    min_time = seconds
                sum_times += seconds

            if tasks.count() == 0 or sum_times == 0:
                sum_times = None
            else:
                sum_times = sum_times / tasks.count()

            worksheet.write_row(index + 1, 0, [store_code, task_name, min_time, max_time, sum_times])

        # Конец
        workbook.close()
