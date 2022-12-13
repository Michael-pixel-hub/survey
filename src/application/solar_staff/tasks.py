from celery import shared_task
from datetime import datetime


@shared_task(name='solar_staff_pay')
def solar_staff_pay(te_id):

    from application.survey.models import TasksExecution
    from application.solar_staff.classes import SolarStaff

    try:
        obj = TasksExecution.objects.get(id=te_id)
    except TasksExecution.DoesNotExist:
        return 'Task execution %s not found' % te_id

    if obj.task.ss_account:
        solar_obj = SolarStaff(obj.task.ss_account.salt, obj.task.ss_account.client_id)
    else:
        solar_obj = SolarStaff()

    if solar_obj.payout(obj):
        obj.status = 4
        obj.save()
        return 'OK'
    else:
        return 'Not payed'


@shared_task(name='solar_staff_pay_queue')
def solar_staff_pay_queue():

    from application.survey.models import TasksExecution
    from application.solar_staff.classes import SolarStaff

    try:
        obj = TasksExecution.objects.filter(status=6).order_by('?').first()
    except TasksExecution.DoesNotExist:
        return 'No tasks for pay'

    if not obj:
        return 'No tasks for pay'

    if obj.task.ss_account:
        solar_obj = SolarStaff(obj.task.ss_account.salt, obj.task.ss_account.client_id)
    else:
        solar_obj = SolarStaff()

    if solar_obj.payout(obj):
        obj.status = 4
        obj.save()
        return 'Payed task id %s' % obj.id
    else:
        obj.status = 7
        obj.save()
        return 'Not payed task id %s' % obj.id


@shared_task(name='solar_staff_pay_queue_orders')
def solar_staff_pay_queue_orders():

    from application.agent.models import Order
    from application.solar_staff.classes import SolarStaff

    # Заказы с нулевым кешбеком не платим
    Order.objects.filter(status=3, cashback_sum=0).update(status=5)

    try:
        obj = Order.objects.filter(status=3, cashback_sum__gt=0).order_by('?').first()
    except Order.DoesNotExist:
        return 'No orders for pay'

    if not obj:
        return 'No orders for pay'

    if obj.ss_account:
        solar_obj = SolarStaff(obj.ss_account.salt, obj.ss_account.client_id)
    else:
        solar_obj = SolarStaff()

    if solar_obj.payout_order(obj):
        obj.status = 6
        obj.save()
        return 'Payed order id %s' % obj.id
    else:
        obj.status = 7
        obj.save()
        return 'Not payed order id %s' % obj.id


@shared_task(name='solar_staff_user_reg')
def solar_staff_user_reg():

    from application.survey.models import User
    from application.solar_staff.classes import SolarStaff

    try:
        obj = User.objects.filter(is_need_solar_staff_reg=True).order_by('?').first()
    except User.DoesNotExist:
        return 'No users for register on Solar staff'

    if not obj:
        return 'No users for register on Solar staff'

    solar_obj = SolarStaff()
    if solar_obj.worker_create(obj.email, obj.name, obj.surname):
        obj.is_need_solar_staff_reg = False
        obj.save()
        return 'Register user %s id %s in Solar staff' % (obj.email, obj.id)
    else:
        obj.is_need_solar_staff_reg = False
        obj.save()
        return 'Not register user %s id %s in Solar staff' % (obj.email, obj.id)


@shared_task(name='solar_staff_pay_queue_payments')
def solar_staff_pay_queue_payments():

    from application.solar_staff.models import Payment
    from application.solar_staff.classes import SolarStaff

    # Заказы с нулевым кешбеком не платим
    obj = Payment.objects.filter(status=2, sum__gt=0).order_by('?').first()

    if not obj:
        return 'No payments for pay'

    if obj.ss_account:
        solar_obj = SolarStaff(obj.ss_account.salt, obj.ss_account.client_id)
    else:
        solar_obj = SolarStaff()

    if solar_obj.payout_payment(obj):
        obj.status = 3
        obj.date_payment = datetime.now()
        obj.save()
        return 'Payed payment id %s' % obj.id
    else:
        obj.status = 4
        obj.date_payment = datetime.now()
        obj.save()
        return 'Not payed payment id %s' % obj.id
