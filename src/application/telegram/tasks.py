from datetime import datetime
import json
import requests
import time

from django.apps import apps
from django.db import transaction

from celery.task import task
from celery.utils.log import get_task_logger
from preferences.utils import get_setting

from .utils import escape


@task(name='send_message_all')
def send_message_all(text, field_filter=None):
    """
    Рассылка сообщений по всей базе
    :param text: Текст сообщения
    :param field_filter: Фильтрация пользователей, если нужно
    :return: Результат работы задания
    """

    from application.survey.models import User

    # bot = apps.get_app_config('telegram').bot

    users = User.objects.all()
    if field_filter is not None:
        users = users.filter(**{field_filter: True})

    count = 0
    count_all = 0

    bot_token = get_setting('telegram_bottoken')

    for user in users:

        count_all += 1

        if user.telegram_id is None:
            continue

        try:
            current_text = text

            fio = escape(str(user.fio or ''))
            username = escape(str(user.username or ''))

            current_text = current_text.replace('{{name}}', fio).replace('{{username}}', username)
            # bot.send_message(user.telegram_id, current_text, parse_mode='Markdown')

            url = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown'. \
                format(
                token=bot_token,
                chat_id=user.telegram_id,
                text=current_text
            )

            # proxy = {
            #     'https': "socks5://sockuser:sockpass@engine2.ru:1090",
            #     'http': "socks5://sockuser:sockpass@engine2.ru:1090"
            # }

            # requests.get(url, proxies=proxy)

            requests.get(url)

            count += 1
        except:
            continue

    return 'Sent messages {count} from {count_all}'.format(count=count, count_all=count_all)


@task(name='send_message')
def send_message(chat_id, text):
    """
    Отправка одного сообщения
    :param chat_id: Индентификатор пользователя телеграм
    :param text: тексто сообщения
    :return: Результат работы задания
    """

    # bot = apps.get_app_config('telegram').bot

    # bot.send_message(chat_id, text, parse_mode='Markdown')

    bot_token = get_setting('telegram_bottoken')

    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }

    # url = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown'. \
    #     format(
    #     token=bot_token,
    #     chat_id=chat_id,
    #     text=text
    # )

    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=bot_token)

    # proxy = {
    #     'https': "socks5://sockuser:sockpass@95.216.140.252:1080",
    #     'http': "socks5://sockuser:sockpass@95.216.140.252:1080"
    # }
    # r = requests.get(url, proxies=proxy)
    # print(r.text)

    # proxy = {
    #     'https': "socks5://sockuser:sockpass@engine2.ru:1090",
    #     'http': "socks5://sockuser:sockpass@engine2.ru:1090"
    # }

    r = requests.post(url, data=data)

    try:
        logger = get_task_logger(__name__)
        if r.status_code != 200:
            logger.error(r.text)
    except:
        pass

    return str(r.status_code)


@task(name='send_file')
def send_file(chat_id, file=None):

    bot_token = get_setting('telegram_bottoken')

    url = 'https://api.telegram.org/bot{token}/sendDocument?chat_id={chat_id}'.format(
        token=bot_token,
        chat_id=chat_id
    )

    if file:
        files = {'document': open(file, 'rb')}
        r = requests.post(url, files=files)
    else:
        pass

    try:
        logger = get_task_logger(__name__)
        if r.status_code != 200:
            logger.error(r.text)
    except:
        pass

    return str(r.status_code)


@task(name='send_message_keyboard')
def send_message_keyboard(chat_id, text, keyboard):
    """
    Отправка одного сообщения
    :param chat_id: Индентификатор пользователя телеграм
    :param text: тексто сообщения
    :return: Результат работы задания
    """

    bot_token = get_setting('telegram_bottoken')

    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(
        token=bot_token,
    )

    data = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': json.dumps(keyboard),
        'parse_mode': 'Markdown'
    }

    # proxy = {
    #     'https': "socks5://sockuser:sockpass@95.216.140.252:1080",
    #     'http': "socks5://sockuser:sockpass@95.216.140.252:1080"
    # }
    # r = requests.get(url, data=data, proxies=proxy)
    # print(r.text)

    # proxy = {
    #     'https': "socks5://sockuser:sockpass@engine2.ru:1090",
    #     'http': "socks5://sockuser:sockpass@engine2.ru:1090"
    # }

    r = requests.get(url, data=data)

    try:
        logger = get_task_logger(__name__)
        if r.status_code != 200:
            logger.error(r.text)
            logger.error(data)
        else:
            logger.info('Sent telegram %s' % chat_id)
    except:
        pass

    return str(r.status_code)


@task(name='send_telegram_channels')
def send_telegram_channels():

    def send_message_delay(url, data):
        response = requests.get(url, data=data)
        if response.status_code != 200:
            try:
                return_data = response.json()
                if return_data['parameters']['retry_after']:
                    time.sleep(int(return_data['parameters']['retry_after']) + 1)
                    response = requests.get(url, data=data)
                    try:
                        logger = get_task_logger(__name__)
                        logger.error('Sleep %s' % return_data['parameters']['retry_after'])
                    except:
                        pass
            except:
                pass
        return response

    bot_token = get_setting('telegram_bottoken')
    siteurl = get_setting('telegram_siteurl')

    from django.core.cache import cache
    from application.survey.models import TasksExecution, StoreTask, TasksExecutionImage
    from application.telegram.models import String, Channel

    if cache.get('celery_send_telegram_channels_process'):
        return 'OTHER TASK EXECUTION NOW'
    cache.set('celery_send_telegram_channels_process', 1)

    te = TasksExecution.objects.filter(telegram_channel_status=1).order_by('date_start')[:5]

    count = 0
    sent_count = 0

    s = String.get_string('msg_telegram_channel_photo_before')

    for i in te:

        try:
            st = StoreTask.objects.get(store=i.store, task=i.task)
        except:
            i.telegram_channel_status = 0
            i.save(update_fields=['telegram_channel_status'])
            continue

        telegram_id = st.telegram_channel_id
        if not telegram_id:
            i.telegram_channel_status = 0
            i.save(update_fields=['telegram_channel_status'])
            continue

        try:
            Channel.objects.get(telegram_id=telegram_id, is_public=True)
        except:
            i.telegram_channel_status = 0
            i.save(update_fields=['telegram_channel_status'])
            continue

        i.telegram_channel_status = 2
        i.save(update_fields=['telegram_channel_status'])

    transaction.commit()

    for i in te:

        count += 1

        if i.telegram_channel_status == 0:
            continue

        sent_count += 1

        url = 'https://api.telegram.org/bot{token}/sendMessage'.format(
            token=bot_token,
        )

        email = '' if i.user.email is None else i.user.email
        data = {
            'chat_id': telegram_id,
            'text': s.format(
                task=i.task.name,
                user='[%s](tg://user?id=%s)' % (i.user, i.user.telegram_id),
                email=email.replace('_', '\\_'),
                store=i.store,
                comments=i.comments,
                date=i.date_end_user.strftime('%d.%m.%Y %H:%M:%S'),
            ),
            'parse_mode': 'Markdown'
        }

        # proxy = {
        #     'https': "socks5://sockuser:sockpass@95.216.140.252:1080",
        #     'http': "socks5://sockuser:sockpass@95.216.140.252:1080"
        # }
        # requests.get(url, data=data, proxies=proxy)

        # proxy = {
        #     'https': "socks5://sockuser:sockpass@engine2.ru:1090",
        #     'http': "socks5://sockuser:sockpass@engine2.ru:1090"
        # }

        r = send_message_delay(url, data=data)

        try:
            logger = get_task_logger(__name__)
            if r.status_code != 200:
                logger.error(r.text)
                logger.error(data)
            else:
                #logger.info('Sent telegram channel %s %s' % (telegram_id, i.id))
                pass
        except:
            pass

        url = 'https://api.telegram.org/bot{token}/sendMediaGroup'.format(
            token=bot_token,
        )

        if st.task.new_task:

            # Photo
            media = []
            c = 0
            for p in TasksExecutionImage.objects.filter(task=i)[:9]:
                media_str = '%s%s' % (siteurl, p.image.url)
                if p.telegram_id:
                    media_str = p.telegram_id
                c += 1
                media.append({
                    'type': 'photo',
                    'media': media_str,
                    'caption': p.constructor_step_name,
                })
            data = {
                'chat_id': telegram_id,
                'media': json.dumps(media),
            }

            r = send_message_delay(url, data=data)

            try:
                logger = get_task_logger(__name__)
                if r.status_code != 200:
                    logger.error(r.text)
                    logger.error(data)
            except:
                pass
        else:
            # Photo before
            media = []
            c = 0
            for p in TasksExecutionImage.objects.filter(task=i, type='before')[:9]:
                media_str = '%s%s' % (siteurl, p.image.url)
                if p.telegram_id:
                    media_str = p.telegram_id
                c += 1
                media.append({
                    'type': 'photo',
                    'media': media_str,
                    'caption': 'Фото до работы %s' % c,
                })
            data = {
                'chat_id': telegram_id,
                'media': json.dumps(media),
            }
            # r = requests.post(url, data=data, proxies=proxy)

            r = send_message_delay(url, data=data)

            try:
                logger = get_task_logger(__name__)
                if r.status_code != 200:
                    logger.error(r.text)
                    logger.error(data)
            except:
                pass

            # Photo after
            media = []
            c = 0
            for p in TasksExecutionImage.objects.filter(task=i, type='after')[:9]:
                c += 1
                media_str = '%s%s' % (siteurl, p.image.url)
                if p.telegram_id:
                    media_str = p.telegram_id
                media.append({
                    'type': 'photo',
                    'media': media_str,
                    'caption': 'Фото после работы %s' % c,
                })
            data = {
                'chat_id': telegram_id,
                'media': json.dumps(media),
            }
            # r = requests.post(url, data=data, proxies=proxy)

            r = send_message_delay(url, data=data)

            try:
                logger = get_task_logger(__name__)
                if r.status_code != 200:
                    logger.error(r.text)
                    logger.error(data)
            except:
                pass

    cache.delete('celery_send_telegram_channels_process')
    return 'Sent to telegram channel %s of  %s' % (sent_count, count)


@task(name='send_messages_group')
def send_messages_group(text, file, excel_file):

    from application.survey.utils import get_send_message_data

    data = get_send_message_data(excel_file)

    count = 0

    for i in data:
        user = i['obj']

        if user and user.telegram_id:

            current_text = text

            fields = {
                'fio': escape(str(user.fio or '')),
                'username': escape(str(user.username or '')),
            }

            field_num = 0
            for field in i['data']:
                fields[f'field_{field_num}'] = field.value
                field_num += 1

            for key, value in fields.items():
                current_text = current_text.replace('{%s}' % key, str(value))

            count += 1
            send_message.delay(user.telegram_id, current_text)
            if file:
                send_file.delay(user.telegram_id, file)

    return 'Send message to %s users' % count


@task(name='send_messages_stores')
def send_messages_stores(text, file, excel_file, is_order_button):

    from application.survey.utils import get_send_message_data_stores
    from application.telegram.models import String

    data = get_send_message_data_stores(excel_file)

    count = 0

    for i in data:

        user = None
        if i['obj']:
            user = i['obj'].user

        if user and user.telegram_id:

            current_text = text

            fields = {
                'user_name': escape(str(user.fio or '-')),
                'name': escape(str(i['obj'].name)),
                'address': escape(str(i['obj'].address)),
                'inn': escape(str(i['obj'].inn or '-')),
                'agent': escape(str(i['obj'].agent or '-')),
                'loyalty_plan': escape(str(i['obj'].loyalty_plan or '0')),
                'loyalty_fact': escape(str(i['obj'].loyalty_fact or '0')),
                'loyalty_cashback': escape(str(i['obj'].loyalty_cashback or '0')),
                'loyalty_sumcashback': escape(str(i['obj'].loyalty_sumcashback or '0')),
                'loyalty_debt': escape(str(i['obj'].loyalty_debt or '0')),
                'loyalty_overdue_debt': escape(str(i['obj'].loyalty_overdue_debt or '0')),
                'loyalty_plan_reach': (i['obj'].loyalty_plan-i['obj'].loyalty_fact) or '0',
                'loyalty_cashback_payed': escape(str(i['obj'].loyalty_cashback_payed or '0')),
                'loyalty_cashback_to_pay': escape(str(i['obj'].loyalty_cashback_to_pay or '0')),
                'promo_code': escape(str(i['obj'].promo_code or '-')),
            }

            field_num = 0
            for field in i['data']:
                field_num += 1
                fields[f'field_{field_num}'] = field.value

            for key, value in fields.items():
                current_text = current_text.replace('{%s}' % key, str(value))

            count += 1
            if not is_order_button:
                send_message.delay(user.telegram_id, current_text)
            else:
                keyboard = {'inline_keyboard': [
                    [
                        {
                            'text': String.get_string('btn_agent_order'),
                            'callback_data': 'agent_order_%s' % i['obj'].id
                        },
                    ],
                ], 'resize_keyboard': True}
                send_message_keyboard.delay(user.telegram_id, current_text, keyboard)
            if file:
                send_file.delay(user.telegram_id, file)

    return 'Send message to %s users' % count
