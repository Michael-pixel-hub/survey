import datetime
import requests
import uuid

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.db.models import Q, Count
from preferences.utils import get_setting

from application.iceman.models import StoreTaskSchedule


@shared_task(name='mobile_push_iceman')
def mobile_push_iceman():

    from application.iceman.models import Notification
    from application.iceman.utils import push
    from application.survey.models import UserDeviceIceman

    start_date = datetime.datetime.now() - datetime.timedelta(hours=24)

    objects = Notification.objects.filter(
        date_create__gte=start_date, is_sent=False
    ).select_related('user').order_by('-date_create')[:20]

    s = ''

    for i in objects:

        # Обновляем
        i.is_sent = True
        i.save(update_fields=['is_sent'])
        transaction.commit()

    for i in objects:

        # Добавляем
        s += str(i.id) + '; '

        if i.user is None:

            # Рассылка по всем
            result = push(None, i.title, i.message, i.category)
            i.result = result
            i.save(update_fields=['result'])

        else:

            # Рассылка по устройствам пользователя
            devices = UserDeviceIceman.objects.filter(user=i.user)

            for device in devices:
                result = push(device.key, i.title, i.message, i.category)
                i.result = result
                i.save(update_fields=['result'])

    transaction.commit()

    return s


@shared_task(name='iceman_fill_stores_tasks')
def iceman_fill_stores_tasks():

    from application.iceman.models import Store, StoreTask, Order, StoreTaskSchedule
    from application.survey.models import TasksExecution

    # Не надо удалять все задачи
    StoreTask.objects.all().update(is_sync=False, lock_user_id=None, completed=False, done=False, days_of_week='')

    # Задача продажи
    sales_task_id = get_setting('iceman_salestask')

    # StoreTask.objects.filter(task_id=sales_task_id).update(is_sync=False)
    stores = Store.objects.filter(is_public=True, is_order_task=True)

    for store in stores:

        # Смотрим если ли открытый заказ в этом магазине, новый или просрок
        last_order = Order.objects.filter(store=store).first()
        if last_order is not None and last_order.status in [1, 2, 5]:
            continue

        # Добавляем задачу
        try:
            store_task = StoreTask.objects.get(store=store, task_id=sales_task_id)
        except:
            store_task = StoreTask(store=store, task_id=sales_task_id)

        store_task.task_id = sales_task_id
        store_task.lock_user_id = None
        store_task.completed = False
        store_task.is_sync = True
        store_task.region_id = store.region_id
        store_task.save()

    # Задача получить деньги
    get_money_task_id = get_setting('iceman_getmoneytask')

    orders = Order.objects.filter(status=2)
    for order in orders:

        if order.store is None:
            continue

        if order.task_id is not None:
            try:
                te = TasksExecution.objects.get(id=order.task_id)
                if te.task_id == get_money_task_id:
                    continue
            except TasksExecution.DoesNotExist:
                pass

        try:
            store_task = StoreTask.objects.get(store=order.store, task_id=get_money_task_id)
        except:
            store_task = StoreTask(store=order.store, task_id=get_money_task_id)

        store_task.task_id = get_money_task_id
        store_task.lock_user_id = None
        store_task.completed = False
        store_task.is_sync = True
        store_task.region_id = order.store.region_id
        store_task.save()

    # Обычные задачи
    day_of_week = str(datetime.datetime.today().weekday() + 1)
    week_start = datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().weekday())
    week_start = datetime.datetime.combine(week_start, datetime.time())
    week_end = week_start + datetime.timedelta(days=7) - datetime.timedelta(seconds=1)

    month_start = datetime.datetime.combine(datetime.date(
        datetime.datetime.today().year, datetime.datetime.today().month, 1), datetime.time())
    if datetime.datetime.today().month == 12:
        month_end = datetime.datetime.combine(datetime.date(datetime.datetime.today().year + 1, 1, 1), datetime.time())
    else:
        month_end = datetime.datetime.combine(datetime.date(datetime.datetime.today().year,
                                                            datetime.datetime.today().month + 1, 1), datetime.time())
    month_end = month_end - datetime.timedelta(seconds=1)

    schedules = StoreTaskSchedule.objects.all().prefetch_related('store', 'task', 'only_user')
    for schedule in schedules:

        # Один раз
        if schedule.is_once and not TasksExecution.objects.filter(
                store_iceman=schedule.store, task=schedule.task).filter(~Q(status=5)).exists():
            continue

        # # Дни недели
        # if schedule.days_of_week and day_of_week not in schedule.days_of_week and schedule.task.type != 'sales_go':
        #     continue

        # Кол-во раз в неделю
        if schedule.per_week:
            done_tasks_week = TasksExecution.objects.filter(
                task=schedule.task,
                store_iceman=schedule.store,
                date_end__lte=week_end, date_end__gte=week_start
            ).filter(~Q(status=5)).count()
            if done_tasks_week >= schedule.per_week:
                continue

        # Кол-во раз в месяц
        if schedule.per_month:
            done_tasks_month = TasksExecution.objects.filter(
                task=schedule.task,
                store_iceman=schedule.store,
                date_end__lte=month_end, date_end__gte=month_start
            ).filter(~Q(status=5)).count()
            if done_tasks_month >= schedule.per_month:
                continue

        try:
            store_task = StoreTask.objects.get(store=schedule.store, task_id=schedule.task.id)
        except:
            store_task = StoreTask(store=schedule.store, task_id=schedule.task.id)

        store_task.days_of_week = ''

        # Дни недели
        if schedule.days_of_week: # and day_of_week not in schedule.days_of_week:
            store_task.days_of_week = schedule.days_of_week

        store_task.lock_user_id = None
        store_task.completed = False
        store_task.is_sync = True
        store_task.done = False
        store_task.region_id = schedule.store.region_id
        store_task.only_user_id = schedule.only_user.id if schedule.only_user else None
        store_task.save()

    # Удаляем старые задачи
    StoreTask.objects.filter(is_sync=False).delete()

    return 'Ok'


@shared_task(name='iceman_stores_dadata')
def iceman_stores_dadata():

    from application.iceman.models import Store

    stores = Store.objects.filter(inn_auto=True)

    for store in stores:
        store.save()
        if store.inn_name is not None and store.inn_name != '':
            store.name = store.inn_name
            store.save(update_fields=['name'])

    return 'Ok'


@shared_task(name='iceman_orders_send_mail')
def iceman_orders_send_mail():

    from application.iceman.models import Order
    from application.iceman.utils import make_order_excel

    orders = Order.objects.filter(email_status='wait', store__inn_auto=False).exclude(status=5)[:5]
    for order in orders:
        order.email_status = 'sent'
        order.save(update_fields=['email_status'])
        transaction.commit()

    for order in orders:
        make_order_excel(order)

    return 'OK'


@shared_task(name='iceman_tasks_apply')
def iceman_tasks_apply():

    from application.iceman.models import Order
    from application.survey.models import TasksExecution

    # Инициализация
    sales_task_id = get_setting('iceman_salestask')
    get_money_task_id = get_setting('iceman_getmoneytask')
    month_ago = datetime.datetime.now() - datetime.timedelta(days=180)

    # Проставляем статусы заказов
    orders = Order.objects.filter(date_create__gt=month_ago)
    for order_obj in orders:

        # Заказ просрочен
        if order_obj.days_overdue is not None and order_obj.days_overdue > 0 and order_obj.status in [1, 3]:
            order_obj.status = 2
            order_obj.save(update_fields=['status'])

        # Заказ оплачен
        if order_obj.is_payed and order_obj.status in [1, 2]:
            order_obj.status = 3
            order_obj.save(update_fields=['status'])

    # Проставляем статусы задач
    tasks_executions = TasksExecution.objects.filter(task_id__in=[sales_task_id, get_money_task_id],
                                                     date_end__gt=month_ago)

    for te_obj in tasks_executions:
        order = Order.objects.filter(task_id=te_obj.id).first()

        if order:
            
            # Просрочена
            if order.status == 2 and te_obj.status not in [4, 5, 6, 7]:
                te_obj.status = 5
                te_obj.save(update_fields=['status'])

            # Оплачена
            if order.status == 3 and te_obj.status not in [4, 3, 6, 7]:
                te_obj.status = 3
                te_obj.date_end = datetime.datetime.now()
                te_obj.save(update_fields=['status', 'date_end'])

            # Отменена
            if order.status == 4 and te_obj.status not in [4, 5, 6, 7]:
                te_obj.status = 5
                te_obj.save(update_fields=['status'])

        else:

            # Нет задачи...
            if te_obj.status not in [4, 5, 6, 7]:
                te_obj.status = 5
                te_obj.save(update_fields=['status'])

    # Закрываем заказ если он открыт 8 часов назад
    eight_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=8)
    tasks_executions = TasksExecution.objects.filter(task_id__in=[sales_task_id, get_money_task_id], status=1,
                                                     date_start__lt=eight_hours_ago)

    for te_obj in tasks_executions:

        order = Order.objects.filter(task_id=te_obj.id).first()
        if order:
            order.delete()

        te_obj.status = 5
        te_obj.save(update_fields=['status'])

    # Задача продажи
    sales_date = datetime.datetime.now() - datetime.timedelta(hours=1)
    tasks = TasksExecution.objects.filter(task__type='payment', date_end__gt=sales_date)
    for te in tasks:

        # Магазина нет
        if te.store_iceman is None:
            continue

        # Уже есть заказ с такой задачей
        order = Order.objects.filter(task_id=te.id).first()
        if order:
            continue

        # Ищем последний заказ
        order = Order.objects.filter(store=te.store_iceman).first()
        if order and te.status == 2:
            order.user_money = te.user
            order.task_id = te.id
            order.save(update_fields=['user_money', 'task_id'])
            te.money = order.user_sum
            te.save(update_fields=['money'])

    return 'OK'


@shared_task(name='iceman_send_telegram_channels')
def iceman_send_telegram_channels():

    from application.iceman.models import Order, OrderProduct
    from application.telegram.models import String

    bot_token = get_setting('telegram_bottoken')

    s = String.get_string('msg_agent_telegram_channel_item')

    orders = Order.objects.filter(telegram_status='wait').order_by('date_create')[:5]

    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(
        token=bot_token,
    )

    count = 0
    sent_count = 0

    for i in orders:
        i.telegram_status = 'sent'
        i.save(update_fields=['telegram_status'])
    transaction.commit()

    for i in orders:

        count += 1

        try:
            current_channel_id = i.source.telegram_id
            if i.store.type == 'go' and i.source.go_telegram_id:
                current_channel_id = i.source.go_telegram_id
        except:
            continue

        if current_channel_id is None:
            continue

        goods = i.products
        goods_s = ''
        for g in goods:
            goods_s += '`"%s" %s %s на сумму %s руб.`\n' % (g.name, g.count, g.unit, round(g.price, 2))

        message = s.format(
            id=i.order_id,
            date=i.date_create.strftime('%d.%m.%Y %H:%M'),
            delivery_date=i.delivery_date.strftime('%d.%m.%Y'),
            delivery_address=i.delivery_address,
            sum=i.price,
            comment=i.comment,
            goods=goods_s,
            store=i.store.name if i.store else '',
            status=i.get_status_display(),
            email=i.user.email,
            advisor=i.user.advisor,
            check='',
            store_category='Айсмен',
            source='Приложение Айсмен',
        )

        data = {
            'chat_id': current_channel_id,
            'text': message,
            'parse_mode': 'Markdown'
        }

        r = requests.get(url, data=data)

        if r.status_code != 200:
            logger = get_task_logger(__name__)
            logger.error(r.text)
        else:
            sent_count += 1

    return 'Sent to telegram channel agent %s of  %s' % (sent_count, count)


@shared_task(name='iceman_fill_tasks_statuses')
def iceman_fill_tasks_statuses():

    from application.iceman.models import Order
    from application.survey.models import TasksExecution

    three_month_ago = datetime.datetime.now() - datetime.timedelta(days=180)

    orders = Order.objects.filter(date_create__gt=three_month_ago)

    for order in orders:

        te = None

        if order.task_id is not None:
            try:
                te = TasksExecution.objects.get(id=order.task_id)
            except TasksExecution.DoesNotExist:
                continue

        if te is None:
            if order.task_status is not None:
                order.task_status = None
                order.save(update_fields=['task_status'])
        else:
            if order.task_status != te.status:
                order.task_status = te.status
                order.save(update_fields=['task_status'])


@receiver(post_save, sender=StoreTaskSchedule, dispatch_uid=str(uuid.uuid4()))
def iceman_fill_stores_tasks_by_signal(sender, instance, **kwargs):

    from application.iceman.models import StoreTask
    from application.survey.models import TasksExecution

    # Обычные задачи
    week_start = datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().weekday())
    week_start = datetime.datetime.combine(week_start, datetime.time())
    week_end = week_start + datetime.timedelta(days=7) - datetime.timedelta(seconds=1)

    month_start = datetime.datetime.combine(datetime.date(
        datetime.datetime.today().year, datetime.datetime.today().month, 1), datetime.time())
    if datetime.datetime.today().month == 12:
        month_end = datetime.datetime.combine(datetime.date(datetime.datetime.today().year + 1, 1, 1), datetime.time())
    else:
        month_end = datetime.datetime.combine(datetime.date(datetime.datetime.today().year,
                                                            datetime.datetime.today().month + 1, 1), datetime.time())
    month_end = month_end - datetime.timedelta(seconds=1)

    # Один раз
    if instance.is_once and not TasksExecution.objects.filter(
            store_iceman=instance.store, task=instance.task).filter(~Q(status=5)).exists():
        return 'Ok'

    # Кол-во раз в неделю
    if instance.per_week:
        done_tasks_week = TasksExecution.objects.filter(
            task=instance.task,
            store_iceman=instance.store,
            date_end__lte=week_end, date_end__gte=week_start
        ).filter(~Q(status=5)).count()
        if done_tasks_week >= instance.per_week:
            return 'Ok'

    # Кол-во раз в месяц
    if instance.per_month:
        done_tasks_month = TasksExecution.objects.filter(
            task=instance.task,
            store_iceman=instance.store,
            date_end__lte=month_end, date_end__gte=month_start
        ).filter(~Q(status=5)).count()
        if done_tasks_month >= instance.per_month:
            return 'OK'

    try:
        store_task = StoreTask.objects.get(store=instance.store, task_id=instance.task.id)
    except:
        store_task = StoreTask(store=instance.store, task_id=instance.task.id)

    store_task.days_of_week = ''

    # Дни недели
    if instance.days_of_week:
        store_task.days_of_week = instance.days_of_week

    store_task.region_id = instance.store.region_id
    store_task.only_user_id = instance.only_user.id if instance.only_user else None
    store_task.save()

    return 'Ok'


@receiver(pre_delete, sender=StoreTaskSchedule, dispatch_uid=str(uuid.uuid4()))
def iceman_fill_stores_tasks_by_signal_delete(sender, instance, **kwargs):

    from application.iceman.models import StoreTask, StoreTaskSchedule

    try:
        store_task = StoreTask.objects.get(store=instance.store, task_id=instance.task.id).delete()
    except:
        pass
