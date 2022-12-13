from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

from datetime import timedelta

app = Celery('application')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if settings.DEBUG:

    app.conf.beat_schedule = {
    }

else:

    app.conf.beat_schedule = {
        'upload-image-compare': {
            'task': 'upload_image_compare',
            'schedule': timedelta(minutes=1),
        },
        'solar-staff-pay-queue': {
            'task': 'solar_staff_pay_queue',
            'schedule': timedelta(seconds=10),
        },
        'solar-staff-pay-queue-orders': {
            'task': 'solar_staff_pay_queue_orders',
            'schedule': timedelta(minutes=1),
        },
        'solar-staff-user-reg': {
            'task': 'solar_staff_user_reg',
            'schedule': timedelta(minutes=2),
        },
        'make-map-data-osm': {
            'task': 'make_map_data_osm',
            'schedule': timedelta(minutes=10),
        },
        'make-map-data-smoroza': {
            'task': 'make_map_data_smoroza',
            'schedule': timedelta(minutes=5),
        },
        # 'inspector-upload': {
        #     'task': 'inspector_upload',
        #     'schedule': timedelta(seconds=15),
        # },
        # 'inspector-upload-constructor': {
        #     'task': 'inspector_upload_constructor',
        #     'schedule': timedelta(seconds=15),
        # },
        # 'inspector-report': {
        #     'task': 'inspector_report',
        #     'schedule': timedelta(seconds=15),
        # },
        # 'inspector-report-constructor': {
        #     'task': 'inspector_report_constructor',
        #     'schedule': timedelta(seconds=15),
        # },
        # 'inspector-upload-before': {
        #     'task': 'inspector_upload_before',
        #     'schedule': timedelta(seconds=60),
        # },
        # 'inspector-report-before': {
        #     'task': 'inspector_report_before',
        #     'schedule': timedelta(seconds=60),
        # },
        # 'inspector-alert': {
        #     'task': 'inspector_alert',
        #     'schedule': timedelta(seconds=15),
        # },
        'inspector-alert-constructor': {
            'task': 'inspector_alert_constructor',
            'schedule': timedelta(seconds=5),
        },
        # 'inspector-fix': {
        #     'task': 'inspector_fix',
        #     'schedule': timedelta(minutes=1),
        # },
        # 'inspector-fix-constructor': {
        #     'task': 'inspector_fix_constructor',
        #     'schedule': timedelta(minutes=1),
        # },
        'auto-status': {
            'task': 'auto_status',
            'schedule': timedelta(minutes=1),
        },
        # 'send-telegram-channels': {
        #     'task': 'send_telegram_channels',
        #     'schedule': timedelta(minutes=1),
        # },
        'agent-send-telegram-channels': {
            'task': 'agent_send_telegram_channels',
            'schedule': timedelta(minutes=3),
        },
        'calc-ranks': {
            'task': 'calc_ranks',
            'schedule': crontab(hour=2, minute=1, day_of_month=1),
        },
        'dump': {
            'task': 'dump',
            'schedule': crontab(hour=0, minute=10, day_of_month=1),
        },
        'add-value': {
            'task': 'add_value',
            'schedule': crontab(hour=1, minute=1),
        },
        'clear-upload-dir': {
            'task': 'clear_upload_dir',
            'schedule': crontab(hour=2, minute=20),
        },
        'request-process': {
            'task': 'request_process',
            'schedule': timedelta(minutes=1),
        },
        'external-request-process': {
            'task': 'external_request_process',
            'schedule': timedelta(seconds=5),
        },
        # 'clear-store-tasks': {
        #     'task': 'clear_store_tasks',
        #     'schedule': timedelta(minutes=5),
        # },
        'archive-create-tables': {
            'task': 'archive_create_tables',
            'schedule': crontab(hour=1, minute=0, day_of_month=1, month_of_year=11),
        },
        'taxpayer-acts-alerts': {
            'task': 'taxpayer_acts_alerts',
            'schedule': timedelta(minutes=2),
        },
        # 'calc-cashback': {
        #     'task': 'calc_cashback',
        #     'schedule': timedelta(minutes=10),
        # },
        'stores-tasks-refresh': {
            'task': 'stores_tasks_refresh',
            'schedule': timedelta(minutes=4),
        },
        'stores-tasks-renew': {
            'task': 'stores_tasks_renew',
            'schedule': crontab(hour=0, minute=30),
        },
        'solar-staff-pay-queue-payments': {
            'task': 'solar_staff_pay_queue_payments',
            'schedule': timedelta(minutes=1),
        },
        'mobile-push': {
            'task': 'mobile_push',
            'schedule': timedelta(seconds=30),
        },
        'mobile-push-iceman': {
            'task': 'mobile_push_iceman',
            'schedule': timedelta(seconds=30),
        },
        'iceman-fill-stores-tasks': {
            'task': 'iceman_fill_stores_tasks',
            'schedule': crontab(hour=0, minute=0),
        },
        'ai-upload': {
            'task': 'ai_upload',
            'schedule': timedelta(seconds=5),
        },
        'ai-report': {
            'task': 'ai_report',
            'schedule': timedelta(seconds=5),
        },
        'ai-problem': {
            'task': 'ai_problem',
            'schedule': timedelta(minutes=2),
        },
        'ai-fix': {
            'task': 'ai_fix',
            'schedule': timedelta(seconds=20),
        },
        'iceman-stores-dadata': {
            'task': 'iceman_stores_dadata',
            'schedule': timedelta(minutes=2),
        },
        'iceman-orders-send-mail': {
            'task': 'iceman_orders_send_mail',
            'schedule': timedelta(minutes=1),
        },
        'iceman-tasks-apply': {
            'task': 'iceman_tasks_apply',
            'schedule': timedelta(minutes=5),
        },
        'iceman-send-telegram-channels': {
            'task': 'iceman_send_telegram_channels',
            'schedule': timedelta(minutes=3),
        },
        'iceman-fill-tasks-statuses': {
            'task': 'iceman_fill_tasks_statuses',
            'schedule': timedelta(minutes=10),
        },
        'delete-account-notifications': {
            'task': 'delete_account_notifications',
            'schedule': timedelta(days=1),
        },
        'supervisor-make-users-schedules': {
            'task': 'supervisor_make_users_schedules',
            'schedule': timedelta(minutes=5),
        },
    }
