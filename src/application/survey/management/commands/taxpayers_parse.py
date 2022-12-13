import datetime
import os

from application.survey.models import Act, User
from django.conf import settings
from django.core.management.base import BaseCommand
from openpyxl import load_workbook


class Command(BaseCommand):

    help = 'Taxpayers parse'

    def handle(self, *args, **options):

        print('Taxpayers parse ...')

        wb = load_workbook(os.path.join(settings.DATA_DIR, 'taxpayers_with_inn.xlsx'))
        ws = wb.worksheets[0]

        col = 0

        for i in ws.rows:

            col += 1

            if col <= 1:
                continue

            act_exists = Act.objects.filter(number=i[1].value).count()
            if act_exists > 0:
                print(f'Act {i[1].value} allready exists')
                continue

            user_obj = User.objects.filter(email__iexact=i[7].value).first()

            act_obj = Act()
            act_obj.date = datetime.datetime.strptime(i[0].value, '%d.%m.%Y %H:%M:%S')
            act_obj.number = i[1].value
            act_obj.user_fio = i[2].value
            act_obj.sum = i[4].value
            act_obj.user = user_obj
            act_obj.user_email = i[7].value
            act_obj.user_inn = i[8].value
            act_obj.save()
