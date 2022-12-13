import datetime
import requests

from celery import shared_task
from django.db import transaction
from django.db.models import Q


@shared_task(name='ai_create_report')
def ai_create_report():

    from application.survey.models import TasksExecution, TasksExecutionImage

    objects = TasksExecution.objects.filter(
        inspector_status='wait', task_id=53
    ).filter(~Q(status=1)).order_by('-date_start')[:5]

    s = ''

    for i in objects:
        i.inspector_status = 'ai'
        i.save(update_fields=['inspector_status'])
    transaction.commit()

    for i in objects:

        s += f'{i.id}; '

        images = TasksExecutionImage.objects.filter(task=i).filter(
            Q(type='after') | Q(constructor_step_name__iexact='Фото ПОСЛЕ работы')
        )

        data = []
        for image in images:
            data.append(('images[]', f'https://admin.shop-survey.ru/media/{image.image}'))

        if data:
            try:
                response = requests.post(
                    'https://ai.shop-survey.ru/api/v1/reports/create/?api_key=8339880fd4f64f47b66f36b67f2c549b',
                    data=data
                )
                report_id = response.json()['id']
            except:
                pass

    return f'AI report create: {s}'


def inspector_alert_success(te_obj):

    from application.telegram.models import String
    from application.telegram.tasks import send_message_keyboard

    te_obj.inspector_is_alert = False
    te_obj.save(update_fields=['inspector_is_alert'])
    transaction.commit()

    s_success = String.get_string('msg_inspector_alert_success')
    menu = {'inline_keyboard': [
        [
            {'text': 'ОК', 'callback_data': 'te_ok_%s' % te_obj.id},
        ],
    ], 'resize_keyboard': True}

    send_message_keyboard.delay(te_obj.user.telegram_id, s_success, keyboard=menu)


@shared_task(name='ai_upload')
def ai_upload():

    from application.survey.models import TasksExecutionInspector
    from application.ai.classes import Ai

    ai = Ai()

    old_date = datetime.datetime.now() - datetime.timedelta(hours=10)
    new_date = datetime.datetime.now() - datetime.timedelta(seconds=10)

    objects = TasksExecutionInspector.objects.filter(
        inspector_status='wait',
        date_start__range=(old_date, new_date)
    ).order_by('-date_start')[:50]

    for i in objects:
        try:
            i.inspector_status = 'upload_wait'
            i.save(update_fields=['inspector_status'])
            transaction.commit()
        except:
            pass

    s = ''
    for i in objects:
        try:
            ai.parse_constructor(i)
            s += str(i.task.id) + '; '
            if i.inspector_status == 'upload_error' or i.inspector_status == 'parse_error' or \
                    i.inspector_status == 'report_error':
                raise Exception(i.inspector_status)
        except Exception as e:
            try:
                if not i.inspector_is_alert:
                    inspector_alert_success(i.task)
                i.inspector_status = 'error'
                i.inspector_error = str(e)
                i.inspector_is_alert = True
                i.save(update_fields=['inspector_status', 'inspector_error', 'inspector_is_alert'])
            except:
                pass
        i.save_to_te()

    return s


@shared_task(name='ai_report')
def ai_report():

    from application.survey.models import TasksExecutionInspector
    from application.ai.classes import Ai

    old_date = datetime.datetime.now() - datetime.timedelta(hours=10)
    new_date = datetime.datetime.now() - datetime.timedelta(seconds=10)

    ai = Ai()

    objects = TasksExecutionInspector.objects.filter(
        inspector_status='report_wait',
        date_start__range=(old_date, new_date),
    ).order_by('-date_start')[:100]

    for i in objects:
        try:
            i.inspector_status = 'report_process'
            i.save(update_fields=['inspector_status'])
            transaction.commit()
        except Exception as e:
            pass

    s = ''
    ss = ''

    for i in objects:

        try:
            ss += str(i.task.id) + ' '
            ai.report_constructor(i)
            if i.inspector_status == 'upload_error' or i.inspector_status == 'parse_error' or \
                    i.inspector_status == 'report_error':
                raise Exception(i.inspector_status)
        except Exception as e:
            try:
                if not i.inspector_is_alert:
                    inspector_alert_success(i.task)
                i.inspector_status = 'error'
                i.inspector_error = str(e)
                i.inspector_is_alert = True
                i.save(update_fields=['inspector_status', 'inspector_error', 'inspector_is_alert'])
            except Exception as e:
                print(f'ai_report report error: id inspector {i.id}')

        i.save_to_te()

    return ss + '; ' + s


@shared_task(name='ai_fix')
def ai_fix():

    from application.survey.models import TasksExecutionInspector

    old_date = datetime.datetime.now() - datetime.timedelta(hours=10)
    new_date = datetime.datetime.now() - datetime.timedelta(seconds=120)

    s = ''
    ss = ''

    objects = TasksExecutionInspector.objects.filter(
        inspector_status='upload_wait',
        date_start__range=(old_date, new_date),
    ).order_by('-date_start')[:100]

    for i in objects:
        try:
            ss += str(i.task.id) + ' '
            i.inspector_status = 'wait'
            i.save(update_fields=['inspector_status'])
            transaction.commit()
        except Exception as e:
            pass

    objects = TasksExecutionInspector.objects.filter(
        inspector_status='report_process',
        date_start__range=(old_date, new_date),
    ).order_by('-date_start')[:100]

    for i in objects:
        try:
            ss += str(i.task.id) + ' '
            i.inspector_status = 'report_wait'
            i.save(update_fields=['inspector_status'])
            transaction.commit()
        except Exception as e:
            pass

    return ss + '; ' + s


@shared_task(name='ai_problem')
def ai_problem():

    from application.ai.classes import Ai
    from application.ai.models import AIProblem
    from application.survey.models import TasksExecution, TasksExecutionOutReason, TaskStep, TasksExecutionInspector

    objects = AIProblem.objects.all()

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

    for ai_obj in objects:

        # Получаем выполненную задачу
        try:
            te_obj = TasksExecution.objects.get(id=ai_obj.te_id)
        except TasksExecution.DoesNotExist:
            ai_obj.delete()
            continue

        # Если задача не выполнена и была еще вчера
        if te_obj.date_start < yesterday:
            ai_obj.delete()
            continue

        if te_obj.status == 1:
            continue

        # Ищем шаг с причинами
        step = TaskStep.objects.filter(task=te_obj.task, photo_out_reason=True).first()
        if step is None:
            continue

        # Ищем отчет
        inspector = TasksExecutionInspector.objects.filter(task=te_obj, constructor_step_name=step.name).first()
        if inspector is None:
            continue

        if inspector.inspector_status != 'success':
            continue

        # Отправляем проблему
        goods = TasksExecutionOutReason.objects.filter(task=te_obj, out_reason__is_report=True).values_list(
            'good__code', flat=True)
        if len(goods) > 0:
            ai = Ai()
            ai.problem(inspector.inspector_report_id, goods)
        ai_obj.delete()

    return 'OK'
