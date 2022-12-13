Установка на сервер


1. Для начала нужно утсановить следующее ПО:
* Postgres (пароль для рута можно поставить любой, но у меня в install.sh и в настройках settings.py используется пароль "postgres", это надо будет изменить)
* nginx
* supervisor

После установки supervisor нужно добавить его в автозапуск:
systemctl enable supervisor
systemctl start supervisor

* letsencrypt

mkdir /var/letsencrypt
cd /var/letsencrypt
wget https://dl.eff.org/certbot-auto
chmod a+x certbot-auto
./certbot-auto certonly --standalone

Для автообновления в crontab нужно добавить что-то вроде:

0 3 1 * * /var/letsencrypt/certbot-auto renew --standalone --pre-hook "service nginx stop" --post-hook "service nginx start" >> /var/log/letsencrypt-renew.log

При установке сертификат предлагает сгенерировать для домена/поддомена, чтобы сгенерировать его с консоли нужно выполнить: 

/var/letsencrypt/certbot-auto certonly --standalone --pre-hook "service nginx stop" --post-hook "service nginx start"

2. Скопировать из git. Конфиги написаны на папку /var/telegram/{PROJECT}, но можно выбрать любой каталог, единственное что придется править конфиги.
3. Запустить ./install.sh

Что он делает:
* устанавливает системные библиотеки
* создает виртуально окружение питон virtualenv
* устанавливает в него нужные пакеты питона, Джанго, и т.д.
* создает базу и выполняет migrate, collectstatics
* устанавливает тестовые данные

4. Создать файл локальных настроек, туда можно вписать доступ к postgres и т.д.

Пример лежит тут: {PROJECT}/src/application/settings_production_sample.py
Сам файл должн называться: settings_production.py в этой же папке

5. Скопировать куда-нибудь конфиг файлы, чтобы их править

Конфиг файлы лежать в папке conf/
* Конфиг для uwsgi - conf/sample.uwsgi.ini

В нем нужно исправить только пути. Путь к socket можно вполне оставить без изменений. 

* Конфиги для supervisor

conf/sample.supervisor.conf и conf/sample.celery.supervisor.conf
Один запускает вебсервер, второй запускает планировщик заданий.

В них тоже можно исправить только пути.

* Конфиг для nginx - conf/sample.nginx.conf

Тут нужно везде заменить домен на свойи пути тоже.

6. После того как скопированы и изменены конфигов добавить их нужно 

* для nginx: /etc/nginx/sites-enabled/
Перезапустить /etc/init.d./nginx restart

* для супервизора: /etc/supervisor/conf.d/
Перезапустить: supervisorctl update
Сервер сразу запустится, если нет ошибок.

7. После перезапуска по url домена или поддомена будет админка
В тестовых данных доступ: mail@engine2.ru и пароль admin

8. Нужно изменить настройки:
По адресу /preferences/setting/

Url сайта - указать ваш домен, только не завершать слешем, например https://dot.domain.ru
App Metrica Api key - указать если вы хотите вести статистику appmetrika
Имя бота - Имя вшего бота без @, например dvp_bot
Токен бота - API ключ бота который вам дал @BotFather, после его ввода сервер мягко рестартится.
