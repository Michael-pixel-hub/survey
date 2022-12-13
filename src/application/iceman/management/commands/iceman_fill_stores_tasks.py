from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Iceman fill stores tasks'

    def handle(self, *args, **options):

        print('Iceman fill stores tasks ...')

        from application.iceman.tasks import iceman_fill_stores_tasks

        print(iceman_fill_stores_tasks())
