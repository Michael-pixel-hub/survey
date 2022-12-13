from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Iceman fix orders payment days'

    def handle(self, *args, **options):

        print('Iceman fix orders payment days ...')

        from application.iceman.models import Order

        orders = Order.objects.filter(payment_days__isnull=True, store__isnull=False).select_related('store', 'store__source')

        for order in orders:
            order.payment_days = order.store.payment_days \
                if order.store.payment_days else order.store.source.payment_days
            order.save(update_fields=['payment_days'])
