import datetime
import traceback

from celery import shared_task
from django.db.models import Q
from django.db import transaction


def inspector_alert_success(te_obj):

    from application.telegram.models import String
    from application.telegram.tasks import send_message_keyboard

    te_obj.inspector_is_alert = False
    te_obj.save()

    s_success = String.get_string('msg_inspector_alert_success')
    menu = {'inline_keyboard': [
        [
            {'text': 'ОК', 'callback_data': 'te_ok_%s' % te_obj.id},
        ],
    ], 'resize_keyboard': True}

    send_message_keyboard.delay(te_obj.user.telegram_id, s_success, keyboard=menu)


@shared_task(name='inspector_upload_constructor')
def inspector_upload_constructor():

    from application.survey.models import TasksExecutionInspector
    from application.inspector.classes import Inspector

    inspector = Inspector()

    objects = TasksExecutionInspector.objects.filter(
        inspector_status='wait',
    #).filter(Q(task__source='telegram') | ~Q(task__status=1)).order_by('-task__date_start')[:5]
    ).order_by('-date_start')[:5]

    for i in objects:
        i.inspector_status = 'upload_wait'
    transaction.commit()

    s = ''
    for i in objects:
        try:
            inspector.parse_constructor(i)
            s += str(i.task.id) + '; '
            if i.inspector_status == 'upload_error' or i.inspector_status == 'parse_error' or \
                    i.inspector_status == 'report_error':
                raise Exception(i.inspector_status)
        except Exception as e:
            if not i.inspector_is_alert:
                inspector_alert_success(i.task)
            i.inspector_status = 'error'
            i.inspector_error = str(e)
            i.inspector_is_alert = True
            i.save()
        i.save_to_te()

    return s


@shared_task(name='inspector_upload')
def inspector_upload():

    from application.survey.models import TasksExecution
    from application.inspector.classes import Inspector
    from application.telegram.models import String
    from application.telegram.tasks import send_message_keyboard

    obj = Inspector()

    old_date = datetime.datetime.now() - datetime.timedelta(hours=10)
    new_date = datetime.datetime.now() - datetime.timedelta(seconds=10)

    objects = TasksExecution.objects.filter(Q(status=1) | Q(inspector_re_work=True)).filter(
        inspector_status='wait', task__is_parse=True, step='uploaded', inspector_is_work=True,
        date_end_user__range=(old_date, new_date), task__new_task=False
    ).order_by('-date_start')[:5]

    for i in objects:
        i.inspector_status = 'upload_wait'
    transaction.commit()

    s = ''

    for i in objects:
        try:
            obj.parse(i)
            s += str(i.id) + '; '
            if i.inspector_status == 'upload_error' or i.inspector_status == 'parse_error' or \
                    i.inspector_status == 'report_error':
                raise Exception(i.inspector_status)
        except Exception as e:
            i.inspector_status = 'error'
            i.inspector_error = str(e)
            i.inspector_is_alert = True
            i.save()

            s_success = String.get_string('msg_inspector_alert_success')
            menu = {'keyboard': [
                [
                    [String.get_string('btn_task_finish'), String.get_string('btn_task_info'),
                     String.get_string('btn_task_instruction'),
                     String.get_string('btn_task_assortment'), String.get_string('btn_task_cancel'),
                     String.get_string('btn_main_menu')]
                ],
            ], 'resize_keyboard': True}

            send_message_keyboard.delay(i.user.telegram_id, s_success, keyboard=menu)

    return s


@shared_task(name='inspector_upload_before')
def inspector_upload_before():

    from application.survey.models import TasksExecution
    from application.inspector.classes import Inspector

    obj = Inspector()

    old_date = datetime.datetime.now() - datetime.timedelta(hours=10)
    new_date = datetime.datetime.now() - datetime.timedelta(minutes=10)

    objects = TasksExecution.objects.filter(
        task__is_parse=True, step='uploaded', inspector_is_work=True, inspector_status_before='wait',
        date_end_user__range=(old_date, new_date), task__new_task=False
    ).order_by('-date_start')[:15]

    for i in objects:
        i.inspector_status_before = 'upload_wait'
    transaction.commit()

    for i in objects:
        try:
            obj.parse_before(i)
        except Exception:
            i.inspector_status_before = 'error'
            i.save()


@shared_task(name='inspector_report_constructor')
def inspector_report_constructor():

    from application.survey.models import TasksExecutionInspector
    from application.inspector.classes import Inspector

    inspector = Inspector()

    objects = TasksExecutionInspector.objects.filter(
        inspector_status='report_wait'
    ).order_by('-date_start')[:5]

    for i in objects:
        i.inspector_status = 'report_process'
    transaction.commit()

    s = ''
    ss = ''

    for i in objects:

        ss += str(i.task.id) + ' '

        try:
            inspector.report_constructor(i)
            if i.inspector_status == 'upload_error' or i.inspector_status == 'parse_error' or \
                    i.inspector_status == 'report_error':
                raise Exception(i.inspector_status)
        except:
            if not i.inspector_is_alert:
                inspector_alert_success(i.task)
            i.inspector_status = 'error'
            var = traceback.format_exc()
            i.inspector_error = var
            i.inspector_is_alert = True
            i.save()

        i.save_to_te()

    return ss + '; ' + s


@shared_task(name='inspector_report')
def inspector_report():

    from application.survey.models import TasksExecution
    from application.inspector.classes import Inspector
    from application.telegram.models import String
    from application.telegram.tasks import send_message_keyboard

    old_date = datetime.datetime.now() - datetime.timedelta(hours=6)

    obj = Inspector()

    objects = TasksExecution.objects.filter(
        inspector_status='report_wait', date_end_user__gt=old_date, task__new_task=False
    ).order_by('-date_start')[:5]

    for i in objects:
        i.inspector_status = 'report_process'
    transaction.commit()

    s = ''
    ss = ''

    for i in objects:

        ss += str(i.id) + ' '

        try:
            obj.report(i)
            if i.inspector_status == 'upload_error' or i.inspector_status == 'parse_error' or \
                    i.inspector_status == 'report_error':
                raise Exception(i.inspector_status)
        except Exception as e:
            i.inspector_status = 'error'
            var = traceback.format_exc()
            i.inspector_error = var
            i.inspector_is_alert = True
            i.save()

            s_success = String.get_string('msg_inspector_alert_success')
            menu = {'keyboard': [
                [
                    [String.get_string('btn_task_finish'), String.get_string('btn_task_info'),
                     String.get_string('btn_task_instruction'),
                     String.get_string('btn_task_assortment'), String.get_string('btn_task_cancel'),
                     String.get_string('btn_main_menu')]
                ],
            ], 'resize_keyboard': True}

            send_message_keyboard.delay(i.user.telegram_id, s_success, keyboard=menu)

    return ss + '; ' + s


@shared_task(name='inspector_report_before')
def inspector_report_before():

    from application.survey.models import TasksExecution
    from application.inspector.classes import Inspector

    obj = Inspector()

    old_date = datetime.datetime.now() - datetime.timedelta(hours=6)

    objects = TasksExecution.objects.filter(
        inspector_status_before='report_wait', date_end_user__gt=old_date, task__new_task=False
    ).order_by('-date_start')[:15]

    for i in objects:
        i.inspector_status_before = 'report_process'
    transaction.commit()

    for i in objects:
        try:
            obj.report_before(i)
        except Exception:
            i.inspector_status_before = 'error'
            i.save()


@shared_task(name='inspector_alert')
def inspector_alert():

    from application.survey.models import TasksExecution, TasksExecutionAssortment, Assortment
    from application.telegram.tasks import send_message_keyboard
    from application.telegram.models import String

    s_less = String.get_string('msg_inspector_alert_less')
    s_no = String.get_string('msg_inspector_alert_no')
    s = String.get_string('msg_inspector_alert')
    s_success = String.get_string('msg_inspector_alert_success')

    objects = TasksExecution.objects.filter(
        status=1, inspector_status='success', inspector_is_alert=False, step='uploaded', task__is_parse=True,
        inspector_is_work=True, task__new_task=False
    ).order_by('date_start')[:5]

    for i in objects:
        i.inspector_is_alert = True
    transaction.commit()

    objects = list(objects)

    s1 = ''

    for i in objects:

        i.inspector_is_alert = True
        i.save()
        transaction.commit()

        s1 += str(i.id) + '; '

        te_last = TasksExecution.objects.filter(
            task=i.task, date_start__lte=i.date_start, status__in=[3, 6, 4, 7], store=i.store, step='uploaded',
            inspector_status='success'
        ).order_by('date_start').last()
        if not te_last:
            menu = {'inline_keyboard': [
                [
                    {'text': 'ОК', 'callback_data': 'te_ok_%s' % i.id},
                ],
            ], 'resize_keyboard': True}

            s1 += send_message_keyboard(i.user.telegram_id, s_success, keyboard=menu) + '; '
            continue

        te_new_as = list(TasksExecutionAssortment.objects.filter(task=i))
        te_last_as = list(TasksExecutionAssortment.objects.filter(task=te_last))
        te_exists_as = list(Assortment.objects.filter(store=i.store, task=i.task))
        if not te_exists_as:
            te_exists_as = list(Assortment.objects.filter(store=i.store, task__isnull=True))

        # Less count
        last_count = 0
        for g in te_last_as:
            last_count += g.avail
        now_count = 0
        for g in te_new_as:
            now_count += g.avail
        less_count = last_count - now_count

        less_count = 0

        # No items
        no_goods = []
        for g in te_exists_as:
            exists = False
            for n in te_new_as:
                if (g.good.name and g.good.name == n.good.name) or (g.good.code and g.good.code == n.good.code):
                    exists = True
            if not exists:
                no_goods.append(g.good.name)

        if less_count > 0 or no_goods:

            if i.user.telegram_id:

                less_count = round(less_count, 2)
                if less_count <= 0:
                    s_less_s = ''
                else:
                    s_less_s = '`' + s_less.format(faces=less_count) + '`\n'

                if no_goods:
                    faces = ''
                    for sa in no_goods:
                        faces += '`' + str(sa) + '`\n'
                    s_no_s = s_no.format(faces=faces, count=len(no_goods))
                else:
                    s_no_s = ''

                menu = {'inline_keyboard': [
                    [
                        {'text': 'Да', 'callback_data': 'te_yes_%s' % i.id},
                        {'text': 'Нет', 'callback_data': 'te_no_%s' % i.id}
                    ],
                ], 'resize_keyboard': True}

                s1 += send_message_keyboard(i.user.telegram_id, s.format(less_faces=s_less_s, no_faces=s_no_s), keyboard=menu) + '; '

        else:

            menu = {'inline_keyboard': [
                [
                    {'text': 'ОК', 'callback_data': 'te_ok_%s' % i.id},
                ],
            ], 'resize_keyboard': True}

            s1 += send_message_keyboard(i.user.telegram_id, s_success, keyboard=menu) + '; '

    return s1


@shared_task(name='inspector_fix_constructor')
def inspector_fix_constructor():

    from application.survey.models import TasksExecutionInspector

    start_date = datetime.datetime.now() - datetime.timedelta(hours=24)
    end_date = datetime.datetime.now() - datetime.timedelta(minutes=3)

    objects = TasksExecutionInspector.objects.filter(
        inspector_status='upload_wait', date_start__range=(start_date, end_date)
    ).order_by('-date_start')[:20]

    s = ''

    for i in objects:

        i.inspector_status = 'wait'
        i.save()

        s += 'FIXED CONSTRUCTOR ' + str(i.task.id) + '; '

    end_date = datetime.datetime.now() - datetime.timedelta(minutes=5)

    objects = TasksExecutionInspector.objects.filter(
        inspector_status='report_process', date_start__range=(start_date, end_date)
    ).order_by('-date_start')[:20]

    for i in objects:

        i.inspector_status = 'report_wait'
        i.save()

        s += 'FIXED CONSTRUCTOR REPORT ' + str(i.task.id) + '; '

    end_date = datetime.datetime.now() - datetime.timedelta(minutes=4)
    objects = TasksExecutionInspector.objects.filter(
        inspector_status='report_wait', date_start__range=(start_date, end_date), task__inspector_is_alert=True
    ).order_by('-date_start')[:10]
    for i in objects:

        if not i.inspector_is_alert:
            inspector_alert_success(i.task)
        i.inspector_is_alert = True
        i.save()

        s += 'FIXED CONSTRUCTOR INSPECTOR NOT WORK ' + str(i.task.id) + '; '

    # end_date = datetime.datetime.now() - datetime.timedelta(minutes=10)
    # objects = TasksExecutionInspector.objects.filter(
    #     inspector_status='report_wait', date_start__range=(start_date, end_date)
    # ).order_by('-date_start')[:10]
    #
    # for i in objects:
    #
    #     if not i.inspector_is_alert:
    #         inspector_alert_success(i.task)
    #     i.inspector_status = 'error'
    #     i.inspector_error = 'Inspector not working!'
    #     i.inspector_is_alert = True
    #     i.save()
    #
    #     s += 'FIXED CONSTRUCTOR INSPECTOR NOT WORK ' + str(i.task.id) + '; '

    return s


@shared_task(name='inspector_fix')
def inspector_fix():

    from application.survey.models import TasksExecution

    start_date = datetime.datetime.now() - datetime.timedelta(hours=10)
    end_date = datetime.datetime.now() - datetime.timedelta(minutes=3)

    objects = TasksExecution.objects.filter(Q(status=1) | Q(inspector_re_work=True)).filter(
        inspector_status='upload_wait', task__is_parse=True, step='uploaded', inspector_is_work=True,
        date_end_user__range=(start_date, end_date), task__new_task=False
    ).order_by('-date_start')[:20]

    s = ''

    for i in objects:

        i.inspector_status = 'wait'
        i.save()

        s += 'FIXED ' + str(i.id) + '; '

    objects = TasksExecution.objects.filter(
        task__is_parse=True, step='uploaded', inspector_is_work=True, inspector_status_before='upload_wait',
        date_end_user__range=(start_date, end_date), task__new_task=False
    ).order_by('-date_start')[:20]

    for i in objects:

        i.inspector_status_before = 'wait'
        i.save()

        s += 'FIXED BEFORE ' + str(i.id) + '; '

    end_date = datetime.datetime.now() - datetime.timedelta(minutes=15)

    objects = TasksExecution.objects.filter(
        task__is_parse=True, step='uploaded', inspector_is_work=True, inspector_status='report_process',
        date_end_user__range=(start_date, end_date), task__new_task=False
    ).order_by('-date_start')[:20]

    for i in objects:

        i.inspector_status = 'report_wait'
        i.save()

        s += 'FIXED REPORT ' + str(i.id) + '; '

    end_date = datetime.datetime.now() - datetime.timedelta(minutes=20)

    objects = TasksExecution.objects.filter(
        task__is_parse=True, step='uploaded', inspector_is_work=True, inspector_status_before='report_process',
        date_end_user__range=(start_date, end_date), task__new_task=False
    ).order_by('-date_start')[:20]

    for i in objects:

        i.inspector_status_before = 'report_wait'
        i.save()

        s += 'FIXED REPORT BEFORE ' + str(i.id) + '; '

    # Inspector not working
    end_date = datetime.datetime.now() - datetime.timedelta(minutes=20)
    objects = TasksExecution.objects.filter(
        task__is_parse=True, step='uploaded', inspector_is_work=True, inspector_status='report_wait',
        date_end_user__range=(start_date, end_date), task__new_task=False
    ).order_by('-date_start')[:20]

    for i in objects:

        inspector_alert_success(i)

        s += 'FIXED INSPECTOR NOT WORK ' + str(i.id) + '; '

    return s


@shared_task(name='inspector_alert_constructor')
def inspector_alert_constructor():

    from application.survey.models import TasksExecutionInspector, TasksExecutionAssortment, Assortment, TasksExecution
    from application.telegram.tasks import send_message_keyboard
    from application.telegram.models import String

    s_less = String.get_string('msg_inspector_alert_less')
    s_no = String.get_string('msg_inspector_alert_no')
    s = String.get_string('msg_inspector_alert')
    s_success = String.get_string('msg_inspector_alert_success')

    ai_start_date = datetime.datetime(2022, 2, 1)

    objects = TasksExecutionInspector.objects.filter(
        inspector_status='error', inspector_is_alert=True
    ).order_by('date_start')[:30]
    for i in objects:
        try:
            i.inspector_is_alert = False
            i.save(update_fields=['inspector_is_alert'])
            i.task.inspector_is_alert = True
            i.task.save(update_fields=['inspector_is_alert'])
            i.task.inspector_positions_text = 'Ошибка распознавания. Отправьте отчет заново.'
            i.task.save(update_fields=['inspector_positions_text'])
            transaction.commit()
        except Exception as e:
            pass

    objects = TasksExecutionInspector.objects.filter(
        inspector_status='success', inspector_is_alert=True
    ).order_by('date_start')[:30]

    for i in objects:
        try:
            i.inspector_is_alert = False
            i.save(update_fields=['inspector_is_alert'])
            i.task.inspector_is_alert = True
            i.task.save(update_fields=['inspector_is_alert'])
            transaction.commit()
        except Exception as e:
            pass

    objects = list(objects)

    s1 = ''

    for i in objects:

        try:
            i.inspector_is_alert = False
            i.save(update_fields=['inspector_is_alert'])
            i.task.inspector_is_alert = True
            i.task.save(update_fields=['inspector_is_alert'])
            transaction.commit()

            s1 += str(i.task.id) + '; '

            te_last = TasksExecution.objects.filter(
                task=i.task.task, date_start__lte=i.date_start, date_start__gte=ai_start_date,
                status__in=[3, 6, 4, 7], store=i.task.store
            ).order_by('date_start').last()

            te_new_as = list(TasksExecutionAssortment.objects.filter(task=i.task))
            if te_last:
                te_last_as = list(TasksExecutionAssortment.objects.filter(task=te_last))
            else:
                te_last_as = []
            te_exists_as = list(Assortment.objects.filter(store=i.task.store, task=i.task.task))
            if not te_exists_as:
                te_exists_as = list(Assortment.objects.filter(store=i.task.store, task__isnull=True))

            # Less count
            if te_last:
                last_count = 0
                for g in te_last_as:
                    last_count += g.avail
                now_count = 0
                for g in te_new_as:
                    now_count += g.avail
                less_count = last_count - now_count
            else:
                less_count = 0

            less_count = 0

            # No items
            no_goods = []
            for g in te_exists_as:
                exists = False
                for n in te_new_as:
                    if g.good.name == n.good.name or g.good.code == n.good.code:
                        exists = True
                if not exists:
                    no_goods.append(g.good.name)

            if less_count > 0 or no_goods:

                less_count = round(less_count, 2)
                if less_count <= 0:
                    s_less_s = ''
                else:
                    s_less_s = '`' + s_less.format(faces=less_count) + '`\n'

                if no_goods:
                    faces = ''
                    for sa in no_goods:
                        faces += '`' + str(sa) + '`\n'
                    s_no_s = s_no.format(faces=faces, count=len(no_goods))
                else:
                    s_no_s = ''

                menu = {'inline_keyboard': [
                    [
                        {'text': 'Да', 'callback_data': 'te_yes_%s' % i.task.id},
                        {'text': 'Нет', 'callback_data': 'te_no_%s' % i.task.id}
                    ],
                ], 'resize_keyboard': True}

                if i.task.source == 'telegram':
                    if i.task.user.telegram_id:
                        s1 += send_message_keyboard(
                            i.task.user.telegram_id, s.format(less_faces=s_less_s, no_faces=s_no_s), keyboard=menu) + '; '
                else:
                    s1 += str(2) + '; '
                    i.task.inspector_positions_text = s.format(less_faces=s_less_s, no_faces=s_no_s) + \
                                                      '\r\n' + \
                                                      '*Вы можете вернуться назад в задаче и исправить выкладку.*'
                    i.task.save(update_fields=['inspector_positions_text'])
                    transaction.commit()

            else:

                menu = {'inline_keyboard': [
                    [
                        {'text': 'ОК', 'callback_data': 'te_ok_%s' % i.task.id},
                    ],
                ], 'resize_keyboard': True}

                if i.task.source == 'telegram':
                    if i.task.user.telegram_id:
                        s1 += send_message_keyboard(i.task.user.telegram_id, s_success, keyboard=menu) + '; '
                else:
                    s1 += str(3) + '; '
                    i.task.inspector_positions_text = s_success
                    i.task.save(update_fields=['inspector_positions_text'])
                    transaction.commit()
        except Exception as e:
            pass

    return s1


# @shared_task(name='inspector_alert_constructor')
# def inspector_alert_constructor():
#
#     from application.survey.models import TasksExecutionInspector, TasksExecutionAssortment, Assortment, TasksExecution
#     from application.telegram.tasks import send_message_keyboard
#     from application.telegram.models import String
#
#     s_less = String.get_string('msg_inspector_alert_less')
#     s_no = String.get_string('msg_inspector_alert_no')
#     s = String.get_string('msg_inspector_alert')
#     s_success = String.get_string('msg_inspector_alert_success')
#
#     objects = TasksExecutionInspector.objects.filter(
#         inspector_status='success', inspector_is_alert=True
#     ).order_by('date_start')[:10]
#
#     for i in objects:
#         i.inspector_is_alert = False
#         i.save(update_fields=['inspector_is_alert'])
#         i.task.inspector_is_alert = True
#         i.task.save(update_fields=['inspector_is_alert'])
#         transaction.commit()
#
#     objects = list(objects)
#
#     s1 = ''
#
#     for i in objects:
#
#         # i.inspector_is_alert = False
#         # i.task.inspector_is_alert = True
#         # i.save()
#         # transaction.commit()
#
#         i.inspector_is_alert = False
#         i.save(update_fields=['inspector_is_alert'])
#         i.task.inspector_is_alert = True
#         i.task.save(update_fields=['inspector_is_alert'])
#         transaction.commit()
#
#         s1 += str(i.task.id) + '; '
#
#         te_last = TasksExecution.objects.filter(
#             task=i.task.task, date_start__lte=i.date_start, status__in=[3, 6, 4, 7], store=i.task.store
#         ).order_by('date_start').last()
#
#         if not te_last:
#             menu = {'inline_keyboard': [
#                 [
#                     {'text': 'ОК', 'callback_data': 'te_ok_%s' % i.task.id},
#                 ],
#             ], 'resize_keyboard': True}
#
#             if i.task.source == 'telegram':
#                 if i.task.user.telegram_id:
#                     s1 += send_message_keyboard(i.task.user.telegram_id, s_success, keyboard=menu) + '; '
#             else:
#                 i.task.inspector_positions_text = s_success
#                 i.task.save(update_fields=['inspector_positions_text'])
#                 s1 += str(1) + '; '
#                 transaction.commit()
#             continue
#
#         te_new_as = list(TasksExecutionAssortment.objects.filter(task=i.task))
#         te_last_as = list(TasksExecutionAssortment.objects.filter(task=te_last))
#         te_exists_as = list(Assortment.objects.filter(store=i.task.store, task=i.task.task))
#         if not te_exists_as:
#             te_exists_as = list(Assortment.objects.filter(store=i.task.store))
#
#         # Less count
#         last_count = 0
#         for g in te_last_as:
#             last_count += g.avail
#         now_count = 0
#         for g in te_new_as:
#             now_count += g.avail
#         less_count = last_count - now_count
#
#         # No items
#         no_goods = []
#         for g in te_exists_as:
#             exists = False
#             for n in te_new_as:
#                 if g.good.name == n.good.name or g.good.code == n.good.code:
#                     exists = True
#             if not exists:
#                 no_goods.append(g.good.name)
#
#         if less_count > 0 or no_goods:
#
#             less_count = round(less_count, 2)
#             if less_count <= 0:
#                 s_less_s = ''
#             else:
#                 s_less_s = '`' + s_less.format(faces=less_count) + '`\n'
#
#             if no_goods:
#                 faces = ''
#                 for sa in no_goods:
#                     faces += '`' + str(sa) + '`\n'
#                 s_no_s = s_no.format(faces=faces, count=len(no_goods))
#             else:
#                 s_no_s = ''
#
#             menu = {'inline_keyboard': [
#                 [
#                     {'text': 'Да', 'callback_data': 'te_yes_%s' % i.task.id},
#                     {'text': 'Нет', 'callback_data': 'te_no_%s' % i.task.id}
#                 ],
#             ], 'resize_keyboard': True}
#
#             if i.task.source == 'telegram':
#                 if i.task.user.telegram_id:
#                     s1 += send_message_keyboard(
#                         i.task.user.telegram_id, s.format(less_faces=s_less_s, no_faces=s_no_s), keyboard=menu) + '; '
#             else:
#                 s1 += str(2) + '; '
#                 i.task.inspector_positions_text = s.format(less_faces=s_less_s, no_faces=s_no_s) + \
#                                                   '\r\n' + \
#                                                   '*Вы можете вернуться назад в задаче и исправить выкладку.*'
#                 i.task.save(update_fields=['inspector_positions_text'])
#                 transaction.commit()
#
#         else:
#
#             i.task.inspector_is_alert = False
#             i.task.save()
#
#             menu = {'inline_keyboard': [
#                 [
#                     {'text': 'ОК', 'callback_data': 'te_ok_%s' % i.task.id},
#                 ],
#             ], 'resize_keyboard': True}
#
#             if i.task.source == 'telegram':
#                 if i.task.user.telegram_id:
#                     s1 += send_message_keyboard(i.task.user.telegram_id, s_success, keyboard=menu) + '; '
#             else:
#                 s1 += str(3) + '; '
#                 i.task.inspector_positions_text = s_success
#                 i.task.save(update_fields=['inspector_positions_text'])
#                 transaction.commit()
#
#     return s1
