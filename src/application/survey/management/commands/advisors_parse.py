import os

from application.survey.models import User
from django.conf import settings
from django.core.management.base import BaseCommand
from openpyxl import load_workbook


class Command(BaseCommand):

    help = 'Advisors parse'

    def handle(self, *args, **options):

        print('Advisors parse ...')

        wb = load_workbook(os.path.join(settings.DATA_DIR, 'users_advisors.xlsx'))
        ws = wb.worksheets[0]

        col = 0

        for i in ws.rows:

            col += 1

            if col <= 1:
                continue
            users = User.objects.filter(email__iexact=i[0].value)

            if users:
                users.update(advisor=i[1].value)
