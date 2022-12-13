from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Iceman fill orders user sum'

    def handle(self, *args, **options):

        print('Iceman fill orders user sum ...')

        from application.iceman.models import Order
        from application.survey.models.te import TasksExecution

        orders = Order.objects.all()

        for order in orders:

            order.payment_sum_user = order.user_sum
            order.save(update_fields=['payment_sum_user'])

            if order.task_id:
                try:
                    te = TasksExecution.objects.get(id=order.task_id)
                    te.money = order.payment_sum_user
                    te.save(update_fields=['money'])
                except TasksExecution.DoesNotExist:
                    pass
