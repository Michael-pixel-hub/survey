from celery import shared_task

from datetime import datetime, date


@shared_task(name='supervisor_make_users_schedules')
def supervisor_make_users_schedules():

    from application.supervisor.models import UserSchedule, UserScheduleTaskExecution
    from application.survey.models import StoreTaskAvail, User, Task, TasksExecution
    from application.iceman.models import StoreTask, StoreTaskSchedule, Store

    if datetime.now().hour not in range(5, 24):
        return 'Skip this hour'

    today = date.today()

    sta_items = StoreTaskAvail.objects.filter(only_user_id__isnull=False)

    for sta_item in sta_items:

        # Расписание пользователя
        try:
            user_schedule = UserSchedule.objects.get(user_id=sta_item.only_user_id, date=today)
        except UserSchedule.DoesNotExist:
            try:
                user = User.objects.get(id=sta_item.only_user_id)
            except User.DoesNotExist:
                continue
            user_schedule = UserSchedule(user=user, date=today, route='' if user.route is None else user.route)
            user_schedule.save()

        # Задача пользователя
        try:
            obj = UserScheduleTaskExecution.objects.get(schedule=user_schedule, task_id=sta_item.task_id,
                                                        store_id=sta_item.store_id)
        except UserScheduleTaskExecution.DoesNotExist:
            try:
                task = Task.objects.get(id=sta_item.task_id)
            except Task.DoesNotExist:
                continue
            obj = UserScheduleTaskExecution(
                schedule=user_schedule,
                task_id=sta_item.task_id,
                store_id=sta_item.store_id,
                store_code=sta_item.store_code,
                store_client_name=sta_item.store_client_name,
                store_category_name=sta_item.store_category_name,
                store_address=sta_item.store_address,
                task_name=task.name
            )
            obj.save()

        # Выполнение задачи
        te = TasksExecution.objects.filter(user=user_schedule.user, date_start__date=today, task_id=obj.task_id,
                                           store_id=obj.store_id).first()
        if te is not None and obj.te_id != te.id:
            obj.te = te
            obj.save()

        if te is None and obj.te is not None:
            obj.te = None
            obj.save()


    # Блок для "Айсмана"

    ice_sta_items = StoreTask.objects.filter(only_user_id__isnull=False)
    for ice_sta_item in ice_sta_items:

        if (ice_sta_item.days_of_week and str(
            today.weekday()+1).strip() in ice_sta_item.days_of_week) or not ice_sta_item.days_of_week:

            try:
                user_schedule = UserSchedule.objects.get(user_id=ice_sta_item.only_user_id, date=today)
            except UserSchedule.DoesNotExist:
                try:
                    user = User.objects.get(id=ice_sta_item.only_user_id)
                except User.DoesNotExist:
                    continue
                user_schedule = UserSchedule(user=user, date=today)
                user_schedule.save()

            # Задача пользователя
            try:
                obj = UserScheduleTaskExecution.objects.get(schedule=user_schedule,
                                                            task_id=ice_sta_item.task_id,
                                                            store_id=ice_sta_item.store_id)
            except UserScheduleTaskExecution.DoesNotExist:
                try:
                    task = Task.objects.get(id=ice_sta_item.task_id)
                except Task.DoesNotExist:
                    continue

                obj = UserScheduleTaskExecution(
                    schedule=user_schedule,
                    task_id=ice_sta_item.task_id,
                    store_id=ice_sta_item.store_id,
                    store_code=(ice_sta_item.store.code if ice_sta_item.store.code is not None else ''),
                    store_client_name=ice_sta_item.store.name,
                    store_category_name=ice_sta_item.store.type,
                    store_address=ice_sta_item.store.address,
                    task_name=task.name
                )
                obj.save()

            # Выполнение задачи
            te = TasksExecution.objects.filter(user=user_schedule.user, date_start__date=today, task__id=obj.task_id,
                                               store_iceman__id=obj.store_id).first()
            if te is not None and obj.te_id != te.id:
                obj.te = te
                obj.save()

            if te is None and obj.te is not None:
                obj.te = None
                obj.save()

    return 'Ok'
