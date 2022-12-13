import psycopg2
import re

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Apply agent goods'

    def handle(self, *args, **options):

        print('Apply agent goods...')

        from application.agent.models import Good

        connection = psycopg2.connect(database='shop_survey', user='postgres', password='postgres', host='localhost')
        cursor = connection.cursor()

        cursor.execute(
            'SELECT name, description, image  FROM  agent_goods_old WHERE description != \'\' or image != \'\''
        )

        data = cursor.fetchall()

        count = 0

        for i in data:

            name = re.sub(' +', ' ', i[0]).strip()

            try:
                goods = Good.objects.filter(name=name)
            except Good.DoesNotExist:
                continue

            for j in goods:
                j.description = i[1]
                j.image = i[2]
                j.save()

            count += 1

        cursor.close()
        connection.close()

        print('Done %s goods...' % count)
