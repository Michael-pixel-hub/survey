from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Set to stores default region'

    def handle(self, *args, **options):

        print('Apply regions to agent stores ...')

        from application.agent.models import Store, City

        try:
            city = City.objects.get(code='СПБ')
        except City.DoesNotExist:
            print('Error! Default city does not exists.')
            return

        rows = Store.objects.filter(city__isnull=True).update(city=city)

        print('Ok. Updated %s rows' % rows)
