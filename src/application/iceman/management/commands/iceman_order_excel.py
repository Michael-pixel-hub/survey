from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Iceman make order'

    def add_arguments(self, parser):
        parser.add_argument('order_id', nargs='+', type=int)

    def handle(self, *args, **options):

        print('Iceman make order ...')

        from application.iceman.models import Order
        from application.iceman.utils import make_order_excel

        for order_id in options['order_id']:
            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                print(f'Order {order_id} not found')
                continue

            make_order_excel(order, mail_send=False)
