from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):

    help = 'Fill iceman statuses'

    def handle(self, *args, **options):

        from application.iceman.models import Order
        from application.survey.models import User, UserDeviceIceman, UserStatusIceman, UserStatus

        # Ищем статус Айсмена
        print('Find Iceman status ...')
        try:
            iceman_status = UserStatusIceman.objects.get(name='Айсмен')
        except UserStatusIceman.DoesNotExist:
            print('Error! Status not found')
            return
        print('Found!')

        # Девайсы
        print('Fill devices ...')
        devices = UserDeviceIceman.objects.all().select_related('user', 'user__status_iceman')
        for device in devices:
            if device.user.status_iceman is None:
                device.user.status_iceman = iceman_status
                device.user.save(update_fields=['status_iceman'])
        print('Done!')

        # Ищем статус Айсмена
        print('Find status ...')
        status = None
        try:
            status = UserStatus.objects.get(name='Айсмен')
        except UserStatus.DoesNotExist:
            print('Error! Status not found')

        # Пользователи с этим статусом
        if status is not None:
            print('Found!')
            users = User.objects.filter(Q(status=status) | Q(status_agent=status))
            for user in users:
                if user.status_iceman is None:
                    user.status_iceman = iceman_status
                    user.save(update_fields=['status_iceman'])

            print('Done!')

        # Есть заказы
        print('Fill orders ...')
        orders = Order.objects.filter(user__isnull=False)
        for order in orders:
            if order.user.status_iceman is None:
                order.user.status_iceman = iceman_status
                order.user.save(update_fields=['status_iceman'])
        print('Done!')
