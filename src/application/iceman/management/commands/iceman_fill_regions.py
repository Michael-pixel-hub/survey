import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    help = 'Iceman fill regions'

    def handle(self, *args, **options):

        print('Iceman fill regions ...')

        from application.iceman.models import Region

        csv_file = os.path.join(settings.DATA_DIR, 'region.csv')

        with open(csv_file, newline='') as csv_file:
            spam_reader = csv.reader(csv_file, delimiter=',')
            for row in spam_reader:
                try:
                    Region.objects.get(short_name=row[0])
                except Region.DoesNotExist:
                    region = Region(short_name=row[0], name=row[2])
                    region.save()

            csv_file.close()
