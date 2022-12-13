import datetime
import os

from django.contrib.admin.models import LogEntry

from application.archive.utils import make_archive
from application.mobile.models import Notification
from application.iceman.models import Notification as NotificationIceman
from application.solar_staff.models import SolarStaffPayments
from application.survey.models import TasksExecution, Request, UploadRequests, Sms, UserDevice, UserDeviceIceman, \
    UserGeo

DUMP_DIR = '/var/survey/dumps/'
DB_NAME = 'shop_survey'
MONTH_COUNT = 3
IMAGES_YEAR_COUNT = 3
MEDIA_PATH = '/mnt/storage_10t/tasks/exec/'


def get_month(month):

    now = datetime.datetime.now()
    # now = datetime.datetime(2021, 7, 1, 15, 45)
    # print(now)

    year_l = now.year
    month_l = now.month - month
    if month_l < 1:
        year_l -= 1
        month_l = 12 + month_l

    return datetime.datetime(year_l, month_l, 1)


def dump():

    start_date = get_month(MONTH_COUNT)

    print('\033[92m\nMake archive...\033[0m')
    make_archive(start_date)
    print('Done!')

    print('\033[92m\nDumping base...\033[0m')
    os.environ['PGPASSWORD'] = 'postgres'
    os.system('pg_dump -h localhost -U postgres %s > /mnt/backup/%s%s_%s_%s.sql' %
              (DB_NAME, DUMP_DIR, DB_NAME, datetime.datetime.now().year, datetime.datetime.now().month))
    print('Done!')

    print('\033[92m\nClear base before %s ...\033[0m' % start_date)

    # Order.objects.filter(date_order__lt=start_date).delete()
    SolarStaffPayments.objects.filter(date_payed__lt=start_date).delete()
    LogEntry.objects.filter(action_time__lt=start_date).delete()
    TasksExecution.objects.filter(date_start__lt=start_date).delete()
    Request.objects.filter(date__lt=start_date).delete()
    UploadRequests.objects.filter(request_date__lt=start_date).delete()
    Sms.objects.filter(date__lt=start_date).delete()
    Notification.objects.filter(date_create__lt=start_date).delete()
    NotificationIceman.objects.filter(date_create__lt=start_date).delete()
    UserDevice.objects.filter(date_use__lt=start_date).delete()
    UserDeviceIceman.objects.filter(date_use__lt=start_date).delete()
    UserGeo.objects.filter(date__lt=start_date).delete()

    print('Done!')

    print('\033[92m\nClear images before %s ...\033[0m' % start_date)
    for i in range(1, 4):
        #start_date = get_month(MONTH_COUNT - 1 + i)
        m = str(start_date.month)
        if len(m) < 2:
            m = '0%s' % m
        path = MEDIA_PATH + str(start_date.year - IMAGES_YEAR_COUNT) + '/' + m + '/'
        print('Delete %s ...' % path)
        os.system('rm -rf %s' % path)

    print('Done!')
    return 'Done!'
