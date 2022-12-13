import psycopg2.extras

from application.survey.models import Task, Store, Good, TasksExecution
from application.archive.models import ArchiveTasksExecution, ArchiveTasksExecutionImage, \
    ArchiveTasksExecutionAssortmentBefore, ArchiveTasksExecutionAssortment, ArchiveTasksExecutionQuestionnaire


def load_te():

    conn = psycopg2.connect(dbname='shop_survey_1', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cursor.execute('SELECT * FROM chl_tasks_executions order by id')

    records = cursor.fetchall()

    for i in records:

        try:
            te = ArchiveTasksExecution.objects.get(id=i.id)
        except ArchiveTasksExecution.DoesNotExist:
            te = None

        if not te:

            try:

                try:
                    task = Task.objects.get(id=i.task_id)
                except Task.DoesNotExist:
                    task = None

                try:
                    store = Store.objects.get(id=i.store_id)
                except Store.DoesNotExist:
                    store = None

                obj = ArchiveTasksExecution()
                obj.id = i.id
                obj.user_id = i.user_id
                obj.task = task
                obj.money = i.money
                try:
                    obj.money_source = i.money_source
                except:
                    obj.money_source = 0
                obj.date_start = i.date_start
                obj.date_end = i.date_end
                try:
                    obj.date_end_user = i.date_end_user
                except:
                    obj.date_end_user = i.date_end
                try:
                    obj.source = i.source
                except:
                    pass
                obj.status = i.status
                obj.store = store
                obj.comments = i.comments
                obj.comments_status = i.comments_status
                obj.comments_internal = i.comments_internal
                obj.longitude = i.longitude
                obj.latitude = i.latitude
                obj.distance = i.distance
                obj.step = i.step
                obj.check_type = i.check_type
                obj.set_check_verified = i.set_check_verified
                obj.set_check_not_verified = i.set_check_not_verified
                obj.is_auditor = i.is_auditor
                obj.check_user_id = i.check_user_id
                obj.inspector_upload_images_text = i.inspector_upload_images_text
                obj.inspector_error = i.inspector_error
                obj.inspector_recognize_text = i.inspector_recognize_text
                obj.inspector_report_text = i.inspector_report_text
                obj.inspector_positions_text = i.inspector_positions_text
                obj.inspector_status = i.inspector_status
                obj.inspector_report_id = i.inspector_report_id
                obj.inspector_report_id_before = i.inspector_report_id_before
                obj.inspector_status_before = i.inspector_status_before
                obj.inspector_is_alert = i.inspector_is_alert
                obj.inspector_re_work = i.inspector_re_work
                obj.inspector_is_work = i.inspector_is_work
                obj.telegram_channel_status = i.telegram_channel_status
                obj.constructor_step_id = i.constructor_step_id
                obj.save()
            except Exception as e:
                print(e)

    cursor.close()
    conn.close()


def load_te_images():

    conn = psycopg2.connect(dbname='shop_survey_1', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cursor.execute('SELECT * FROM chl_tasks_executions_images order by id')

    records = cursor.fetchall()

    for i in records:

        try:
            te = ArchiveTasksExecution.objects.get(id=i.task_id)
        except ArchiveTasksExecution.DoesNotExist:
            te = None

        if te is None:
            print(f'Skip TE id {i.task_id}')
            continue

        try:
            tei = ArchiveTasksExecutionImage.objects.get(id=i.id)
        except ArchiveTasksExecutionImage.DoesNotExist:
            tei = None

        if tei:
            continue

        obj = ArchiveTasksExecutionImage()
        obj.id = i.id
        obj.image = i.image
        obj.status = i.status
        obj.md5 = i.md5
        obj.type = i.type
        obj.telegram_id = i.telegram_id
        obj.task_id = te.id
        obj.date_start = te.date_start
        obj.constructor_step_name = i.constructor_step_name
        obj.constructor_check = i.constructor_check
        obj.save()

def load_te_assortment_before():

    conn = psycopg2.connect(dbname='shop_survey_1', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cursor.execute('SELECT * FROM chl_tasks_executions_assortment_before order by id LIMIT 10')

    records = cursor.fetchall()

    for i in records:

        try:
            te = ArchiveTasksExecution.objects.get(id=i.task_id)
        except ArchiveTasksExecution.DoesNotExist:
            te = None

        if te is None:
            print(f'Skip TE id {i.task_id}')
            continue

        try:
            teab = ArchiveTasksExecutionAssortmentBefore.objects.get(id=i.id)
        except ArchiveTasksExecutionAssortmentBefore.DoesNotExist:
            teab = None

        if teab:
            continue

        try:
            good = Good.objects.get(id=i.good_id)
        except Task.DoesNotExist:
            good = None

        obj = ArchiveTasksExecutionAssortmentBefore()
        obj.id = i.id
        obj.avail = i.avail
        obj.good = good
        obj.task_id = te.id
        obj.date_start = te.date_start
        obj.save()


def load_te_assortment_before():

    conn = psycopg2.connect(dbname='shop_survey_1', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cursor.execute('SELECT * FROM chl_tasks_executions_assortment_before order by id LIMIT 10')

    records = cursor.fetchall()

    for i in records:

        try:
            te = ArchiveTasksExecution.objects.get(id=i.task_id)
        except ArchiveTasksExecution.DoesNotExist:
            te = None

        if te is None:
            print(f'Skip TE id {i.task_id}')
            continue

        try:
            teab = ArchiveTasksExecutionAssortmentBefore.objects.get(id=i.id)
        except ArchiveTasksExecutionAssortmentBefore.DoesNotExist:
            teab = None

        if teab:
            continue

        try:
            good = Good.objects.get(id=i.good_id)
        except Task.DoesNotExist:
            good = None

        obj = ArchiveTasksExecutionAssortmentBefore()
        obj.id = i.id
        obj.avail = i.avail
        obj.good = good
        obj.task_id = te.id
        obj.date_start = te.date_start
        obj.save()


def load_te_assortment():

    conn = psycopg2.connect(dbname='shop_survey_1', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cursor.execute('SELECT * FROM chl_tasks_executions_assortment order by id LIMIT 10')

    records = cursor.fetchall()

    for i in records:

        try:
            te = ArchiveTasksExecution.objects.get(id=i.task_id)
        except ArchiveTasksExecution.DoesNotExist:
            te = None

        if te is None:
            print(f'Skip TE id {i.task_id}')
            continue

        try:
            tea = ArchiveTasksExecutionAssortment.objects.get(id=i.id)
        except ArchiveTasksExecutionAssortment.DoesNotExist:
            tea = None

        if tea:
            continue

        try:
            good = Good.objects.get(id=i.good_id)
        except Task.DoesNotExist:
            good = None

        obj = ArchiveTasksExecutionAssortment()
        obj.id = i.id
        obj.avail = i.avail
        obj.constructor_step_name = i.constructor_step_name
        obj.good = good
        obj.task_id = te.id
        obj.date_start = te.date_start
        obj.save()


def make_archive(start_date):

    # Task executions
    items = TasksExecution.objects.filter(date_start__lt=start_date).order_by('id')
    for i in items:

        try:
            record = i.__dict__.copy()
            del record['_state']
            del record['_TasksExecution__original_status']
            item = ArchiveTasksExecution(**record)
            item.save()
        except Exception as e:
            print(e)

    # DB
    conn = psycopg2.connect(dbname='shop_survey', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    start_date = start_date.strftime('%Y-%m-%d')

    # Images
    cursor.execute(f"select e.*, cte.date_start from chl_tasks_executions_images e "
                   f"left join chl_tasks_executions cte on e.task_id = cte.id "
                   f"where cte.date_start < '{start_date}' order by e.id")
    items = cursor.fetchall()

    for i in items:
        try:
            item = ArchiveTasksExecutionImage()
            item.id = i.id
            item.image = i.image
            item.status = i.status
            item.md5 = i.md5
            item.type = i.type
            item.task_id = i.task_id
            item.date_start = i.date_start
            item.telegram_id = i.telegram_id
            item.constructor_step_name = i.constructor_step_name
            item.constructor_check = i.constructor_check
            item.save()
        except Exception as e:
            print(e)

    # Assortment
    cursor.execute(f"select e.*, cte.date_start from shop_survey.public.chl_tasks_executions_assortment e "
                   f"left join chl_tasks_executions cte on e.task_id = cte.id "
                   f"where cte.date_start < '{start_date}' order by e.id")
    items = cursor.fetchall()

    for i in items:
        try:
            item = ArchiveTasksExecutionAssortment()
            item.id = i.id
            item.avail = i.avail
            item.good_id = i.good_id
            item.task_id = i.task_id
            item.date_start = i.date_start
            item.constructor_step_name = i.constructor_step_name
            item.save()
        except Exception as e:
            print(e)

    # Assortment before
    cursor.execute(f"select e.*, cte.date_start from shop_survey.public.chl_tasks_executions_assortment_before e "
                   f"left join chl_tasks_executions cte on e.task_id = cte.id "
                   f"where cte.date_start < '{start_date}' order by e.id")
    items = cursor.fetchall()

    for i in items:
        try:
            item = ArchiveTasksExecutionAssortmentBefore()
            item.id = i.id
            item.avail = i.avail
            item.good_id = i.good_id
            item.task_id = i.task_id
            item.date_start = i.date_start
            item.save()
        except Exception as e:
            print(e)

    # Questionnaire
    cursor.execute(f"select e.*, cte.date_start from shop_survey.public.chl_tasks_executions_questionnaires e "
                   f"left join chl_tasks_executions cte on e.task_id = cte.id "
                   f"where cte.date_start < '{start_date}' order by e.id")
    items = cursor.fetchall()

    for i in items:
        try:
            item = ArchiveTasksExecutionQuestionnaire()
            item.id = i.id
            item.task_id = i.task_id
            item.date_start = i.date_start
            item.constructor_step_name = i.constructor_step_name
            item.name = i.name
            item.question = i.question
            item.answer = i.answer
            item.save()
        except Exception as e:
            print(e)
