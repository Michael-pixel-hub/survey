from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Auto load data from inn'

    def handle(self, *args, **options):

        print('Load data from inn ...')

        from application.agent.models import Store
        from application.agent.utils import save_inn

        stores = Store.objects.all()

        for i in stores:
            print(f'Getting data for store id {i.id}')
            if i.inn:
                print(save_inn(i.id))
