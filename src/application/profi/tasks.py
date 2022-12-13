import requests

from celery.task import task
from preferences.utils import get_setting

from .utils import escape


@task(name='profi_send_message_all')
def send_message_all(text, field_filter=None):
    """
    Рассылка сообщений по всей базе
    :param text: Текст сообщения
    :param field_filter: Фильтрация пользователей, если нужно
    :return: Результат работы задания
    """

    from application.profi.models import User

    users = User.objects.all()
    if field_filter is not None:
        users = users.filter(**{field_filter: True})

    count = 0
    count_all = 0

    bot_token = get_setting('profi_bottoken')

    for user in users:

        count_all += 1

        if user.telegram_id is None:
            continue

        try:
            current_text = text

            fio = escape(str(user.fio or ''))
            username = escape(str(user.username or ''))

            current_text = current_text.replace('{{name}}', fio).replace('{{username}}', username)

            url = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown'.\
                format(
                    token=bot_token,
                    chat_id=user.telegram_id,
                    text=current_text
                )
            requests.get(url)

            count += 1
        except:
            continue

    return 'Sent messages {count} from {count_all}'.format(count=count, count_all=count_all)


@task(name='profi_send_message')
def send_message(chat_id, text):
    """
    Отправка одного сообщения
    :param chat_id: Индентификатор пользователя телеграм
    :param text: тексто сообщения
    :return: Результат работы задания
    """

    bot_token = get_setting('profi_bottoken')

    url = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown'. \
        format(
            token=bot_token,
            chat_id=chat_id,
            text=text
        )
    requests.get(url)

    return 'OK'
