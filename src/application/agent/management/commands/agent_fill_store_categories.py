from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Agent fill store categories'

    def handle(self, *args, **options):

        print('Agent fill store categories...')

        from application.agent.models import Store, StoreCategory

        category_default = StoreCategory.objects.filter(default=True).first()

        stores = Store.objects.all().select_related('user', 'user__status_agent', 'loyalty_department')

        for i in stores:

            if i.loyalty_department:
                category = StoreCategory.objects.get(name__iexact=i.loyalty_department.name)
                i.category = category
                i.save()
                continue

            if i.user.status_agent:
                try:
                    category = StoreCategory.objects.get(name__iexact=i.user.status_agent.name)
                    i.category = category
                except StoreCategory.DoesNotExist:
                    i.category = category_default
                i.save()
            else:
                i.category = category_default
                i.save()
