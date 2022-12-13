import datetime

from celery import shared_task
from django.db import transaction


@shared_task(name='mobile_push')
def mobile_push():

    from application.mobile.models import Notification
    from application.mobile.utils import push
    from application.survey.models import UserDevice

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
            devices = UserDevice.objects.filter(user=i.user)

            for device in devices:
                result = push(device.key, i.title, i.message, i.category)
                i.result = result
                i.save(update_fields=['result'])

    transaction.commit()

    return s
