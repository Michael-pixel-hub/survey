import datetime
import requests

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.db.models import Sum

from preferences.utils import get_setting


@shared_task(name='import_data_from_file_agent')
def import_data(file, file_name):

    from application.agent.utils import import_data_from_file

    import_data_from_file(file, file_name)

    return 'OK'


@shared_task(name='agent_send_mail')
def agent_send_mail(order_id):

    from application.agent.models import Order
    from application.agent.utils import make_order_excel

    try:
        obj = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return 'Order %s not found' % order_id

    return make_order_excel(obj)


@shared_task(name='agent_send_telegram_channels')
def agent_send_telegram_channels():

    from application.agent.models import Order, OrderGood
    from application.telegram.models import String

    bot_token = get_setting('telegram_bottoken')

    s = String.get_string('msg_agent_telegram_channel_item')

    orders = Order.objects.filter(telegram_channel_status=1).order_by('date_order')[:5]

    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(
        token=bot_token,
    )

    count = 0
    sent_count = 0

    for i in orders:
        i.telegram_channel_status = 2
        i.save()
    transaction.commit()

    for i in orders:

        count += 1

        try:
            current_channel_id = i.store.category.telegram_channel_id
        except:
            current_channel_id = None

        if current_channel_id is None:
            continue

        goods = OrderGood.objects.filter(order=i)
        goods_s = ''
        for g in goods:
            goods_s += '`"%s" %s %s на сумму %s руб.`\n' % (g.name, g.count, g.unit, round(g.sum, 2))

        message = s.format(
            id=i.id,
            date=i.date_order.strftime('%d.%m.%Y %H:%M'),
            delivery_date=i.delivery_date.strftime('%d.%m.%Y'),
            delivery_address=i.delivery_address,
            sum=i.sum,
            comment=i.comment,
            goods=goods_s,
            store=i.store.name if i.store else '',
            status=i.get_status_display(),
            email=i.user.email,
            advisor=i.user.advisor,
            check='Нужен' if i.need_check else 'Нет',
            store_category=i.store.category.name if i.store and i.store.category else '',
            source='Телеграм бот',
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

        i.telegram_channel_status = 2
        i.save()

    return 'Sent to telegram channel agent %s of  %s' % (sent_count, count)


@shared_task(name='calc_cashback')
def calc_cashback():

    from application.agent.models import Store, Order
    from application.loyalty.models import Program, ProgramPeriod

    programs = Program.objects.filter(is_public=True)

    for program in programs:

        period = ProgramPeriod.objects.filter(program=program, current=True).first()
        if period is None:
            continue

        stores = Store.objects.filter(loyalty_program=program)

        date_start = datetime.datetime(period.date_start.year, period.date_start.month, period.date_start.day)
        date_end = datetime.datetime(period.date_end.year, period.date_end.month, period.date_end.day, 23, 59, 59)

        for store in stores:

            # Cashback payed
            sum = Order.objects.filter(
                date_order__gte=date_start, date_order__lte=date_end, status__in=[6, 5], store=store
            ).aggregate(sum=Sum('cashback_sum'))['sum']
            sum = round(sum, 2) if sum is not None else 0

            store.loyalty_cashback_payed = sum

            # Cashback for pay
            cashback_for_pay = 0.0
            if store.loyalty_plan <= store.loyalty_fact:
                cashback_for_pay = store.loyalty_sumcashback - store.loyalty_cashback_payed
            if cashback_for_pay < 0:
                cashback_for_pay = 0.0
            if store.is_deleted:
                cashback_for_pay = 0.0
            store.loyalty_cashback_to_pay = cashback_for_pay

            store.save()

    return 'Ok'
