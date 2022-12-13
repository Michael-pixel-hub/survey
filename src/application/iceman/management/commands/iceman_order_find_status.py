import json

from datetime import datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Find status in iceman orders'

    def handle(self, *args, **options):

        from application.survey.models import UploadRequests

        date = datetime(2022, 6, 20)

        requests = UploadRequests.objects.filter(request_date__gt=date, request_data_type='iceman_orders')
        for request in requests:
            data = json.loads(request.request_text)

            for i in data['zakaz']:
                if i['doc'] == 'ICM1114':
                    if i['status'] == 'x':
                        print(i)
