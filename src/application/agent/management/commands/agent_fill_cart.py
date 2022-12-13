from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Agent fill cart'

    def handle(self, *args, **options):

        print('Agent fill cart...')

        from application.agent.models import OrderGood, Good

        goods = OrderGood.objects.all()

        for i in goods:
            if i.good_source is None:

                try:
                    good = Good.objects.get(category=i.category, name=i.name, is_public=True)
                    if good:
                        i.good_source = good
                        i.save()
                except:
                    pass
