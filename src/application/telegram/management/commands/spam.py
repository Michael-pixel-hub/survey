import requests

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Telegram spam to unregistered users'

    def handle(self, *args, **options):

        from application.survey.models import User

        print('Start spaming...')

        users = User.objects.filter(telegram_id__isnull=False, is_register=False, is_banned=False)

        print('Users count %s' % users.count())

        count = 0

        for i in users:

            count += 1

            # if i.telegram_id != 240629525:
            #     continue

            print('Sending to user %s - %s of %s' % (i.telegram_id, count, users.count()))

            try:
                url = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown'.format(
                    token='460283239:AAHigWtgKTfJceT97wBv_fAlQZVj5A-Gz74',
                    chat_id=i.telegram_id,
                    text='''
Добрый день!

Вы не смогли зарегистрироваться в нашем приложении для дополнительного заработка @Serveyor\_bot ?

Вы можете позвонить нам для помощи в регистрации:

Москва - Михаил тел. 89684400150
Моск.область - Сергей тел. 89191033720
Санкт-Петербург и Лен.область - Мария тел. 89811889966

Также вы можете написать нам в Телеграм любые вопросы @Serveyor\_bot
                    '''
                )
                r = requests.get(url, timeout=5)
                print(r)

            except Exception as e:

                print('Error: %s' % e)

        print('Done!')
