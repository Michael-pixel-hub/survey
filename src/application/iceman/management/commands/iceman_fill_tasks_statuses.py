from django.core.management.base import BaseCommand

from application.iceman.models import Order
from application.survey.models import TasksExecution


class Command(BaseCommand):

    help = 'Iceman fill tasks_statuses'

    def handle(self, *args, **options):

        print('Iceman fill tasks_statuses ...')

        orders = Order.objects.all()

        for order in orders:

            if order.task_id is None:
                order.task_status = None
                order.save(update_fields=['task_status'])
                continue

            try:
                te = TasksExecution.objects.get(id=order.task_id)
            except TasksExecution.DoesNotExist:
                order.task_status = None
                order.save(update_fields=['task_status'])
                continue

            order.task_status = te.status
            order.save(update_fields=['task_status'])
