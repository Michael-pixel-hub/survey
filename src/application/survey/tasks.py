import datetime
import json
import os
import time
import traceback

from celery import shared_task

from django.core.cache import cache
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import transaction, models
from django.db.models import Q, Count, Subquery, OuterRef, Exists, F
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


@shared_task(name='import_data_from_file')
def import_data(file, file_name, delete_assortment, assortment_type, user=None):

    from application.survey.utils import import_data_from_file

    import_data_from_file(file, file_name, delete_assortment, assortment_type, user=user)

    return 'OK'


@shared_task(name='upload_image_compare')
def upload_image_compare():

    from application.survey.models import TasksExecutionImage, TasksExecution

    default_status = TasksExecutionImage._meta.get_field('status').default

    content_type = ContentType.objects.get_for_model(TasksExecution)

    images = TasksExecutionImage.objects.filter(status=default_status)[:200]
    for i in images:

        if not i.md5:
            i.save()

        if not i.md5:
            i.status = _('<span style="color: red">Bad image</span>')
            i.save()
            continue

        duplicates = TasksExecutionImage.objects.filter(md5=i.md5).exclude(id=i.id)
        found_duplicates = False
        found_duplicates_id = None
        found_duplicates_task = None

        for d in duplicates:

            if d.task.id != i.task.id:
                found_duplicates = True
                found_duplicates_id = d.task.id
                found_duplicates_task = d.task
                break

        if not found_duplicates:
            i.status = _('<span style="color: green">Unique image</span>')
        else:
            s = str(_('The picture is duplicated in task'))
            i.status = '<span style="color: red">{str} <a href="{url}">{name}</a></span>'.format(
                str=s,
                url=reverse('admin:%s_%s_change' % (content_type.app_label, content_type.model),
                            args=(found_duplicates_id,)),
                name=found_duplicates_task
            )

        i.save()

    return 'Compared %s images' % (images.count())


@shared_task(name='make_map_data_smoroza')
def make_map_data_smoroza():

    import datetime
    import json
    import os
    from django.db.models import OuterRef, Exists
    from application.survey.models import TasksExecution, StoreTask

    day_of_week = str(datetime.datetime.today().weekday() + 1)
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(1)
    today_start = datetime.datetime.combine(today, datetime.time())
    today_end = datetime.datetime.combine(tomorrow, datetime.time())
    today_end = today_end - datetime.timedelta(seconds=1)
    hour = datetime.datetime.now().hour

    month_start = datetime.datetime.combine(datetime.date(today.year, today.month, 1), datetime.time())
    if today.month == 12:
        month_end = datetime.datetime.combine(datetime.date(today.year + 1, 1, 1), datetime.time())
    else:
        month_end = datetime.datetime.combine(datetime.date(today.year, today.month + 1, 1), datetime.time())
    month_end = month_end - datetime.timedelta(seconds=1)

    week_start = today - datetime.timedelta(days=today.weekday())
    week_start = datetime.datetime.combine(week_start, datetime.time())
    week_end = week_start + datetime.timedelta(days=7) - datetime.timedelta(seconds=1)

    done_tasks = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_end__lte=today_end, date_end__gte=today_start
    ).filter(~Q(status=5)).values('id')

    done_tasks_anyday = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
    ).filter(~Q(status=5)).values('id')

    done_tasks_week = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_end__lte=week_end, date_end__gte=week_start
    ).filter(~Q(status=5)).values('task__id', 'store__id').annotate(count=Count('*')).order_by().values('count')

    done_tasks_month = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_end__lte=month_end, date_end__gte=month_start
    ).filter(~Q(status=5)).values('task__id', 'store__id').annotate(count=Count('*')).order_by().values('count')

    st = StoreTask.objects.filter(
        store__longitude__isnull=False, store__latitude__isnull=False, task__id=58, only_user__isnull=True
    ).annotate(
        done_task=Exists(done_tasks), done_tasks_anyday=Exists(done_tasks_anyday),
        done_tasks_week=Subquery(done_tasks_week, output_field=models.IntegerField()),
        done_tasks_month=Subquery(done_tasks_month, output_field=models.IntegerField())
    ).prefetch_related('task', 'store', 'store__category', 'store__client')

    data = {}
    categories = {}

    for i in st:

        category = i.store.category.id if i.store.category else 0
        if not categories.get(category):
            categories[category] = len(categories) + 1

        if i.done_tasks_week is None:
            i.done_tasks_week = 0
        if i.done_tasks_month is None:
            i.done_tasks_month = 0
        if i.done_task:
            continue
        if i.hours_start and i.hours_start > int(hour):
            continue
        if i.hours_end and i.hours_end < int(hour):
            continue
        if i.is_once and i.done_tasks_anyday:
            continue
        if i.days_of_week and day_of_week not in i.days_of_week:
            continue
        if i.per_week and i.done_tasks_week >= i.per_week:
            continue
        if i.per_month and i.done_tasks_month >= i.per_month:
            continue
        price = i.task.money
        if i.is_add_value and i.add_value:
            price = i.add_value
            if i.add_value > i.task.money:
                is_green = True
        s = '<p><b>%s</b> - %s</p>' % \
            (i.task.name,
             '<span style="color: red">Уже сделана</span>'
             if i.done_task else '<span style="color: green">Доступно</span>')

        color = 0
        if i.store.category:
            color = categories[i.store.category.id]

        if data.get(i.store.id):
            s = data[i.store.id]['tx'] + s

        data[i.store.id] = {
            'tx': s, 'sc': i.store.code, 'sa': i.store.address,
            'sct': i.store.category.name if i.store.category else '',
            'scn': i.store.client.name if i.store.client else '',
            'lg': i.store.longitude, 'lt': i.store.latitude, 'c': color
        }

    data_ar = []
    for key, value in data.items():
        data_ar.append(value)

    if settings.DEBUG:
        new_file_path = os.path.join(settings.BASE_DIR, 'static', 'map_osm', 'new_smoroza.json')
        file_path = os.path.join(settings.BASE_DIR, 'static', 'map_osm', 'data_smoroza.json')
    else:
        new_file_path = os.path.join(settings.STATIC_ROOT, 'map_osm', 'new_smoroza.json')
        file_path = os.path.join(settings.STATIC_ROOT, 'map_osm', 'data_smoroza.json')

    with open(new_file_path, 'w') as outfile:
        json.dump(data_ar, outfile)

    os.rename(new_file_path, file_path)

    return 'Done'


@shared_task(name='make_map_data_osm')
def make_map_data_osm():

    import datetime
    import json
    import os
    from django.db.models import OuterRef, Exists
    from application.survey.models import TasksExecution, StoreTask

    day_of_week = str(datetime.datetime.today().weekday() + 1)
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(1)
    today_start = datetime.datetime.combine(today, datetime.time())
    today_end = datetime.datetime.combine(tomorrow, datetime.time())
    today_end = today_end - datetime.timedelta(seconds=1)
    hour = datetime.datetime.now().hour

    month_start = datetime.datetime.combine(datetime.date(today.year, today.month, 1), datetime.time())
    if today.month == 12:
        month_end = datetime.datetime.combine(datetime.date(today.year + 1, 1, 1), datetime.time())
    else:
        month_end = datetime.datetime.combine(datetime.date(today.year, today.month + 1, 1), datetime.time())
    month_end = month_end - datetime.timedelta(seconds=1)

    week_start = today - datetime.timedelta(days=today.weekday())
    week_start = datetime.datetime.combine(week_start, datetime.time())
    week_end = week_start + datetime.timedelta(days=7) - datetime.timedelta(seconds=1)

    done_tasks = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_end__lte=today_end, date_end__gte=today_start
    ).filter(~Q(status=5)).values('id')

    done_tasks_anyday = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
    ).filter(~Q(status=5)).values('id')

    done_tasks_week = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_end__lte=week_end, date_end__gte=week_start
    ).filter(~Q(status=5)).values('task__id', 'store__id').annotate(count=Count('*')).order_by().values('count')

    done_tasks_month = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_end__lte=month_end, date_end__gte=month_start
    ).filter(~Q(status=5)).values('task__id', 'store__id').annotate(count=Count('*')).order_by().values('count')

    st = StoreTask.objects.filter(
        task__is_public=True, task__only_status__isnull=True, store__longitude__isnull=False,
        store__latitude__isnull=False, only_user__isnull=True
    ).annotate(
        done_task=Exists(done_tasks), done_tasks_anyday=Exists(done_tasks_anyday),
        done_tasks_week=Subquery(done_tasks_week, output_field=models.IntegerField()),
        done_tasks_month=Subquery(done_tasks_month, output_field=models.IntegerField())
    ).prefetch_related('task', 'store', 'store__category', 'store__client')

    data = {}

    for i in st:
        is_green = False
        if i.done_tasks_week is None:
            i.done_tasks_week = 0
        if i.done_tasks_month is None:
            i.done_tasks_month = 0
        if i.done_task:
            continue
        if i.hours_start and i.hours_start > int(hour):
            continue
        if i.hours_end and i.hours_end < int(hour):
            continue
        if i.is_once and i.done_tasks_anyday:
            continue
        if i.days_of_week and day_of_week not in i.days_of_week:
            continue
        if i.per_week and i.done_tasks_week >= i.per_week:
            continue
        if i.per_month and i.done_tasks_month >= i.per_month:
            continue
        price = i.task.money
        if i.is_add_value and i.add_value:
            price = i.add_value
            if i.add_value > i.task.money:
                is_green = True
        s = '<p><b>%s</b> (%s руб.) - %s</p>' % \
            (i.task.name, price,
             '<span style="color: red">Уже сделана</span>'
             if i.done_task else '<span style="color: green">Доступно</span>')

        color = 'b'
        if is_green:
            color = 'g'
        if data.get(i.store.id) and data[i.store.id]['c'] == 'g':
            color = 'g'

        if data.get(i.store.id):
            s = data[i.store.id]['tx'] + s

        data[i.store.id] = {
            'tx': s, 'sc': i.store.code, 'sa': i.store.address,
            'scn': i.store.client.name if i.store.client else '',
            'sct': i.store.category.name if i.store.category else '',
            'lg': i.store.longitude, 'lt': i.store.latitude, 'c': color
        }

    data_ar = []
    for key, value in data.items():
        data_ar.append(value)

    if settings.DEBUG:
        new_file_path = os.path.join(settings.BASE_DIR, 'static', 'map_osm', 'new.json')
        file_path = os.path.join(settings.BASE_DIR, 'static', 'map_osm', 'data.json')
    else:
        new_file_path = os.path.join(settings.STATIC_ROOT, 'map_osm', 'new.json')
        file_path = os.path.join(settings.STATIC_ROOT, 'map_osm', 'data.json')

    with open(new_file_path, 'w') as outfile:
        json.dump(data_ar, outfile)

    os.rename(new_file_path, file_path)

    return 'Done'


@shared_task(name='make_json_map_data')
def make_json_map_data():

    import datetime
    import json
    import os
    from django.db.models import OuterRef, Exists
    from application.survey.models import Store, TasksExecution, StoreTask

    day_of_week = str(datetime.datetime.today().weekday() + 1)
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(1)
    today_start = datetime.datetime.combine(today, datetime.time())
    today_end = datetime.datetime.combine(tomorrow, datetime.time())
    this_week = datetime.datetime.now().isocalendar()[1]
    hour = datetime.datetime.now().hour

    stores = Store.objects.filter(longitude__isnull=False, latitude__isnull=False, is_public=True).prefetch_related(
        'client', 'category').\
        extra(where=['exists (SELECT st.id FROM chl_stores_tasks as st WHERE st.store_id = chl_stores.id)'])

    data = []

    done_tasks = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_end__lte=today_end, date_end__gte=today_start
    ).filter(~Q(status=5)).values('id')

    done_tasks_anyday = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
    ).filter(~Q(status=5)).values('id')

    done_tasks_week = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_end__week=this_week
    ).filter(~Q(status=5)).values('id')

    st = list(StoreTask.objects.filter(task__is_public=True, task__only_status__isnull=True).annotate(
        done_task=Exists(done_tasks), done_tasks_anyday=Exists(done_tasks_anyday), done_tasks_week=Exists(done_tasks_week)
    ).prefetch_related('task'))
    for i in stores:
        tasks = []
        tasks_s = ''
        done_count = 0
        tasks_count = 0
        is_green = False
        for s in st:
            if s.store_id == i.id:

                if s.hours_start and s.hours_start > int(hour):
                    continue
                if s.hours_end and s.hours_end < int(hour):
                    continue

                if s.is_once and s.done_tasks_anyday:
                    continue

                if s.days_of_week and day_of_week not in s.days_of_week:
                    continue

                if s.per_week and s.done_tasks_week:
                    continue

                tasks_count += 1
                if s.done_task:
                    done_count += 1

                price = s.task.money
                if s.is_add_value and s.add_value:
                    price = s.add_value
                    if s.add_value > s.task.money:
                        is_green = True
                tasks_s += '<p>%s (%s руб.) - %s</p>' % (
                    s.task.name, price,
                    '<span style="color: red">Уже сделана</span>'
                    if s.done_task else '<span style="color: green">Доступно</span>')
                del s

        avail_count = tasks_count - done_count
        if tasks:
            tasks_s = '<b>Задачи:</b>%s' % tasks_s
        color = 'black'
        if done_count == tasks_count and tasks_count > 0:
            color = 'red'
        if done_count < tasks_count and tasks_count > 0:
            color = 'yellow'
        if done_count == 0 and tasks_count > 0:
            color = 'blue'
        if is_green:
            color = 'green'
        if color == 'blue' or color == 'yellow' or color == 'green':
            data.append({
                'type': 'Feature',
                'id': i.id,
                'geometry': {'type': 'Point', 'coordinates': [i.latitude, i.longitude]},
                'properties': {
                    'balloonContentHeader': i.client.name,
                    "balloonContentBody": '<p>Код магазина: %s</p><p>%s</p>%s' % (i.code, i.address, tasks_s),
                    "balloonContentFooter": i.category.name if i.category else '',
                    "clusterCaption": '%s - %s - %s <br> Доступно заданий %s из %s' % (
                    i.code, i.client.name, i.address, avail_count, tasks_count),
                    "hintContent": '%s - %s - %s <br> Доступно заданий %s из %s' % (
                    i.code, i.client.name, i.address, avail_count, tasks_count),

                },
                'options': {
                    'preset': 'islands#dotIcon',
                    'iconColor': color
                }
            })

    with open('/var/survey/shop-survey/static/map/new.json', 'w') as outfile:
        json.dump(data, outfile)

    os.rename('/var/survey/shop-survey/static/map/new.json', '/var/survey/shop-survey/static/map/data.json')


@shared_task(name='auto_status')
def auto_status():

    from application.survey.models import TasksExecutionImage, TasksExecution, TasksExecutionAssortment, \
        TasksExecutionAssortmentBefore, Assortment, TasksExecutionOutReason
    from application.telegram.models import String

    ten_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=10)
    day_ago = datetime.datetime.now() - datetime.timedelta(hours=24)

    out_reasons = TasksExecutionOutReason.objects.filter(task=OuterRef('pk'))
    objects = TasksExecution.objects.filter(
        date_end__lte=ten_minutes_ago, date_end__gte=day_ago, status=2).filter(inspector_status='success').filter(
        ~Q(check_type='not_verified')
    ).annotate(out_reasons_exist=Exists(out_reasons)).filter(out_reasons_exist=False)[:50]

    s = ''

    for i in objects:

        bad_te = False

        i.comments_status = ''

        # Step 1 Unique images
        if i.task.new_task:
            images = TasksExecutionImage.objects.filter(task=i)
        else:
            images = TasksExecutionImage.objects.filter(task=i, type='after')
        all_unique = True
        for j in images:
            if 'color: red' in j.status:
                all_unique = False

        if not all_unique:
            bad_te = True
            i.comments_status += String.get_string('message_auto_status_nu_image') + '\n\n'

        # Step 2 point so long
        if i.distance and i.distance > 1000:
            bad_te = True
            i.comments_status += String.get_string('message_auto_status_distance') + '\n\n'

        # Step 3 good check
        if i.check_type == 'false':
            bad_te = True
            i.comments_status += String.get_string('message_auto_status_bad_check') + '\n\n'

        # Step 4 faces count grow\
        if i.task.new_task:
            tea = TasksExecutionAssortment.objects.filter(task=i, constructor_step_name__icontains='после')
        else:
            tea = TasksExecutionAssortment.objects.filter(task=i)
        faces_count = 0
        for k in tea:
            faces_count += k.avail
        if i.task.new_task:
            tea = TasksExecutionAssortment.objects.filter(task=i, constructor_step_name__icontains='до')
        else:
            tea = TasksExecutionAssortmentBefore.objects.filter(task=i)
        faces_count_before = 0
        for k in tea:
            faces_count_before += k.avail
        if faces_count_before >= faces_count:
            bad_te = True
            i.comments_status += String.get_string('message_auto_status_faces_count') + '\n\n'

        # Step 5 faces count not null
        faces_count = TasksExecutionAssortment.objects.filter(task=i).count()
        if faces_count < 1:
            bad_te = True
            i.comments_status += String.get_string('message_auto_status_faces_empty') + '\n\n'

        #  Step 6 Проверяем ассортимент
        if i.store is not None and not bad_te:

            # Получаем ассортимент в магазине
            assortment = Assortment.objects.filter(store=i.store, task=i.task).exclude(good__name='')
            assortment_count = assortment.count()
            if assortment_count == 0:
                assortment = Assortment.objects.filter(store=i.store, task__isnull=True).exclude(good__name='')
            assortment = assortment.order_by('good__name', 'id')

            # Распознанные товары
            if i.task.new_task:
                tea = TasksExecutionAssortment.objects.filter(task=i, constructor_step_name__icontains='после')
            else:
                tea = TasksExecutionAssortment.objects.filter(task=i)

            # Сравниваем
            not_found_items = []
            for assortment_item in assortment:
                found = False
                for j in tea:
                    if (assortment_item.good.code and assortment_item.good.code == j.good.code) or \
                            (assortment_item.good.name and assortment_item.good.name == j.good.name):
                        found = True
                if not found:
                    not_found_items.append(assortment_item.good.name)

            # Причины отсутствия
            #out_reasons_count = TasksExecutionOutReason.objects.filter(task=i).count()

            # Отказ
            if not_found_items:
                bad_te = True
                # i.comments_status += 'Не найдены товары на фото:\n' + '\n'.join(not_found_items) + '\n'
                i.comments_status += String.get_string('message_auto_status_assortment_not_found') + '\n\n'
            #
            # # В случае если причины указаны, то ничего не делаем
            # if out_reasons_count > 0 and not_found_items:
            #     return

        # result
        if bad_te:
            i.comments_internal = 'Автоматически проставлен "отказ"'
            i.status = 8
            i.save()
        else:
            if i.money == 0:
                i.comments_internal = 'Автоматически проставлен "принято". ' \
                                      'Автоматически проставлен  "оплачено", потому что задача с нулевой стоимостью'
                i.status = 4
            else:
                i.comments_internal = 'Автоматически проставлен "принято"'
                i.status = 3
            i.save()

        s += f'; {i.id}'

    return 'Changed statuses: %s' % s


@shared_task(name='calc_ranks')
def calc_ranks():

    from application.survey.models import User, TasksExecution, Rank

    users = User.objects.filter(is_register=True, is_banned=False, is_fixed_rank=False)

    month_end = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    month_end = datetime.datetime(
        year=month_end.year, month=month_end.month, day=month_end.day, hour=23, minute=59, second=59
    )
    month_start = datetime.datetime(
        year=datetime.datetime.now().year, month=month_end.month, day=1, hour=0, minute=0, second=0
    )

    ranks = Rank.objects.order_by('-rate')
    try:
        rank_def = Rank.objects.filter(default=True).first()
    except:
        rank_def = None

    for i in users:
        te_first = TasksExecution.objects.filter(user=i, status__in=[3, 6, 4, 7]).last()

        if te_first:
            reg_days = (datetime.datetime.now() - te_first.date_start).days
        else:
            reg_days = 1

        te_month = TasksExecution.objects.filter(
            user=i, status__in=[3, 6, 4, 7], date_end__gte=month_start, date_end__lte=month_end
        )
        te = TasksExecution.objects.filter(
            user=i, status__in=[3, 6, 4, 7]
        )

        i.rank = rank_def

        for r in ranks:
            if r.work_days <= reg_days and r.tasks_month <= te_month.count() and r.tasks_count <= te.count():
                i.rank = r
                break

        i.save()

    return 'Ranks calculated %s users' % users.count()


@shared_task(name='add_value')
def add_value():

    from application.survey.models import StoreTask, TasksExecution

    st = StoreTask.objects.all().prefetch_related('task', 'store')

    is_normal = True

    for i in st:

        # ADD
        if i.task.is_add_money and i.task.add_money and i.task.add_days:

            de = datetime.datetime.now() - datetime.timedelta(days=i.task.add_days)

            te_count = TasksExecution.objects.filter(
                store=i.store, task=i.task, status__in=[2, 3, 6, 4, 7], date_end__gte=de
            ).count()

            if te_count < 1:
                is_normal = False
                i.is_add_value = True
                i.add_value = i.task.add_money
                i.save()

        # LESS
        if i.task.is_remove_money and i.task.remove_money and i.task.remove_days and i.task.remove_ppl:

            de = datetime.datetime.now() - datetime.timedelta(days=i.task.remove_days)

            te_count = TasksExecution.objects.filter(
                store=i.store, task=i.task, status__in=[2, 3, 6, 4, 7], date_end__gte=de
            ).values('user').order_by().annotate(Count('user')).count()

            if te_count >= i.task.remove_ppl:
                is_normal = False
                i.is_add_value = True
                i.add_value = i.task.remove_money
                i.save()

        # NORMAL
        if is_normal:
            if i.is_add_value:
                i.is_add_value = False
                i.add_value = None
                i.save()

    return 'Ok'


@shared_task(name='clear_upload_dir')
def clear_upload_dir():

    now = time.time()
    cutoff = now - (2 * 86400)  # 2 days

    count = 0

    for f in os.listdir(settings.UPLOAD_PATH):
        file_name = os.path.join(settings.UPLOAD_PATH, f)
        try:
            t = os.stat(file_name).st_mtime
            if t < cutoff:
                os.remove(file_name)
                count += 1
        except:
            pass

    for f in os.listdir(settings.DOWNLOAD_PATH):
        file_name = os.path.join(settings.UPLOAD_PATH, f)
        try:
            t = os.stat(file_name).st_mtime
            if t < cutoff:
                os.remove(file_name)
                count += 1
        except:
            pass

    return 'Delete %s files' % count


@shared_task(name='request_process')
def request_process():

    from application.survey.models import UploadRequests

    request = None
    result = 'Unknown data'

    tomorrow = datetime.datetime.now() - datetime.timedelta(days=1)

    try:

        request = UploadRequests.objects.filter(request_date__gte=tomorrow, processed=False).\
            order_by('request_date').first()

        if request is None:
            return 'No requests'

        request.processed = True
        request.save(update_fields=['processed'])
        transaction.commit()

        data = json.loads(request.request_text)

        if data.get('goods'):
            request.request_data_type = 'goods'
            request.request_data_count = len(data.get('goods'))
            from application.agent.utils import agent_1c_goods
            result = agent_1c_goods(data)

        if data.get('payment'):
            request.request_data_type = 'payment'
            request.request_data_count = len(data.get('payment'))
            from application.agent.utils import agent_1c_orders
            result = agent_1c_orders(data)

        if data.get('GO'):
            request.request_data_type = 'go [loyalty]'
            request.request_data_count = len(data.get('GO'))
            from application.loyalty.utils import loyalty_1c_stores
            result = loyalty_1c_stores(data)

        if data.get('goodsPrice'):
            request.request_data_type = 'goodsPrice'
            request.request_data_count = len(data.get('goodsPrice'))
            from application.agent.utils import agent_1c_goods_prices
            result = agent_1c_goods_prices(data)

        if data.get('act') or data.get('act') == []:
            request.request_data_type = 'act'
            request.request_data_count = len(data.get('act'))
            from application.survey.utils import survey_1c_acts
            result = survey_1c_acts(data)

        if data.get('sklad'):
            request.request_data_type = 'iceman_stocks'
            request.request_data_count = len(data.get('sklad'))
            from application.iceman.utils import sync_stocks
            result = sync_stocks(data, '1c')

        if data.get('Clients'):
            request.request_data_type = 'iceman_clients'
            request.request_data_count = len(data.get('Clients'))
            from application.iceman.utils import sync_stores
            result = sync_stores(data, '1c')

        if data.get('Clients_GO'):
            request.request_data_type = 'iceman_clients_go'
            request.request_data_count = len(data.get('Clients_GO'))
            from application.iceman.utils import sync_stores
            result = sync_stores(data, '1c', is_order_task=False, store_type='go', data_name='Clients_GO')

        if data.get('tovar'):
            request.request_data_type = 'iceman_goods'
            request.request_data_count = len(data.get('tovar'))
            from application.iceman.utils import sync_goods
            result = sync_goods(data, '1c')

        if data.get('cen'):
            request.request_data_type = 'iceman_prices'
            request.request_data_count = len(data.get('cen'))
            from application.iceman.utils import sync_prices
            result = sync_prices(data, '1c')

        if data.get('Ostatok'):
            request.request_data_type = 'iceman_stocks_goods'
            request.request_data_count = len(data.get('Ostatok'))
            from application.iceman.utils import sync_stocks_goods
            result = sync_stocks_goods(data, '1c')

        if data.get('zakaz'):
            request.request_data_type = 'iceman_orders'
            request.request_data_count = len(data.get('zakaz'))
            from application.iceman.utils import sync_orders
            result = sync_orders(data, '1c')

        if data.get('specification'):
            request.request_data_type = 'specification'
            request.request_data_count = len(data.get('specification'))
            from application.survey.utils import survey_1c_specification
            result = survey_1c_specification(data)

        if data.get('self_employers'):
            request.request_data_type = 'self_employers'
            request.request_data_count = len(data.get('self_employers'))
            from application.survey.utils import survey_1c_self_employers
            result = survey_1c_self_employers(data)

        if request.request_data_count is not None and request.request_data_count > 10000:
            request.request_text = 'Слишком большой текст для хранения'

        request.result = result
        request.save()

    except:

        if request:
            result = 'Error'
            request.result = traceback.format_exc()
            request.save()

    return result


@shared_task(name='clear_store_tasks')
def clear_store_tasks():

    from application.agent.models import Store
    from application.survey.models import StoreTask
    from django.db.models import OuterRef, Exists

    loyalty_stores = Store.objects.filter(
        loyalty_1c_code=OuterRef('store__code'),
        loyalty_program__isnull=False

    ).values('id')

    items = StoreTask.objects.filter(task__disable_loyalty=True).annotate(
        is_loyalty_story=Exists(loyalty_stores)).filter(is_loyalty_story=True)
    count = items.count()
    items.delete()

    return 'Delete {count} items'.format(count=count)


@shared_task(name='taxpayer_acts_alerts')
def taxpayer_acts_alerts():

    from application.mobile.models import Notification as NotificationShopSurvey
    from application.iceman.models import Notification as NotificationIceman
    from application.survey.models import Act
    from application.telegram.models import String
    from application.telegram.tasks import send_message

    acts = Act.objects.filter(check_type__in=['new', 'false'], is_sent_telegram=False,
                              user__isnull=False).select_related('user').order_by('number')[:10]

    sent_count = 0
    all_count = 0

    for act in acts:
        act.is_sent_telegram = True
        act.save(update_fields=['is_sent_telegram'])
    transaction.commit()

    acts = list(acts)

    for act in acts:

        all_count += 1

        act.is_sent_telegram = True
        act.save(update_fields=['is_sent_telegram'])

        r = '500'

        if act.check_type == 'new':
            r = send_message(act.user.telegram_id, String.get_string('message_taxpayer_act_new').format(
                number=act.number,
                date=act.date.strftime('%d.%m.%Y'),
                sum=act.sum,
            ))

            s = String.get_string('message_taxpayer_act_new_mobile').format(
                number=act.number,
                date=act.date.strftime('%d.%m.%Y'),
                sum=act.sum,
            )
            NotificationShopSurvey(user=act.user, title='Новый акт', message=s, category='act').save()
            NotificationIceman(user=act.user, title='Новый акт', message=s, category='act').save()

        if act.check_type == 'false':
            r = send_message(act.user.telegram_id, String.get_string('message_taxpayer_act_wrong_check').format(
                number=act.number,
                date=act.date.strftime('%d.%m.%Y'),
                sum=act.sum,
                comment_manager=act.comment_manager,
            ))

            s = String.get_string('message_taxpayer_act_wrong_check_mobile').format(
                number=act.number,
                date=act.date.strftime('%d.%m.%Y'),
                sum=act.sum,
                comment_manager=act.comment_manager,
            )
            NotificationShopSurvey(user=act.user, title='Чек к акту был отклонен', message=s, category='act').save()
            NotificationIceman(user=act.user, title='Чек к акту был отклонен', message=s, category='act').save()

        if r == '200':
            sent_count += 1

        transaction.commit()

    return f'Sent {sent_count} of {all_count} messages'


DENIED_ID = 5


@shared_task(name='stores_tasks_refresh')
def stores_tasks_refresh():

    from application.survey.models import StoreTask, TasksExecution, StoreTaskAvail

    if cache.get('celery_stores_tasks_refresh_process'):
        return 'OTHER TASK EXECUTION NOW'
    cache.set('celery_stores_tasks_refresh_process', 1)

    # Условия
    day_of_week = str(datetime.datetime.today().weekday() + 1)
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(1)
    today_start = datetime.datetime.combine(today, datetime.time())
    today_end = datetime.datetime.combine(tomorrow, datetime.time()) - datetime.timedelta(seconds=1)
    hour = datetime.datetime.now().hour
    week_start = today - datetime.timedelta(days=today.weekday())
    week_start = datetime.datetime.combine(week_start, datetime.time())
    week_end = week_start + datetime.timedelta(days=7) - datetime.timedelta(seconds=1)
    month_start = datetime.datetime.combine(datetime.date(today.year, today.month, 1), datetime.time())
    if today.month == 12:
        month_end = datetime.datetime.combine(datetime.date(today.year + 1, 1, 1), datetime.time())
    else:
        month_end = datetime.datetime.combine(datetime.date(today.year, today.month + 1, 1), datetime.time())
    month_end = month_end - datetime.timedelta(seconds=1)

    # Получаем записи
    items = StoreTask.objects.filter(
        store__is_public=True, store__category__is_public=True, store__client__is_public=True, task__is_public=True,
        task__new_task=True, task__is_sales=False, task__application='shop_survey'
    ).select_related(
        'store', 'task', 'store__category', 'store__client', 'store__region_o'
    )

    # Задача в магазине должна быть не выполнена сегодня
    te_today_done = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_start__lte=today_end, date_start__gte=today_start
    ).filter(~Q(status__in=[1, 5])).values('id')
    items = items.annotate(te_today_done=Exists(te_today_done)).filter(te_today_done=False)

    # Проверка на часы задачи
    items = items.filter(Q(hours_start__isnull=True) | Q(hours_start__lte=hour))
    items = items.filter(Q(hours_end__isnull=True) | Q(hours_end__gte=hour))

    # Проверка на выполнение единожды
    te_done = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store')
    ).filter(~Q(status__in=[1, 5])).values('id')
    items = items.annotate(te_done=Exists(te_done)).filter(Q(is_once=False) | Q(te_done=False))

    # Проверка на день недели
    items = items.filter(Q(days_of_week='') | Q(days_of_week__contains=day_of_week))

    # Ограничено кол-во в месяц
    te_month_done = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_start__lte=month_end, date_start__gte=month_start
    ).filter(~Q(status__in=[1, 5])).values('task__id', 'store__id').annotate(count=Count('*')).order_by().values('count')
    items = items.annotate(te_month_done=Subquery(te_month_done, output_field=models.IntegerField())).filter(
        Q(per_month__isnull=True) | Q(per_month=0) | Q(per_month__gt=F('te_month_done')) | Q(te_month_done__isnull=True)
    )

    # Ограничено кол-во в неделю
    te_week_done = TasksExecution.objects.filter(
        task=OuterRef('task'),
        store=OuterRef('store'),
        date_start__lte=week_end, date_start__gte=week_start
    ).filter(~Q(status__in=[1, 5])).values('task__id', 'store__id').annotate(count=Count('*')).order_by().values('count')
    items = items.annotate(te_week_done=Subquery(te_week_done, output_field=models.IntegerField())).filter(
        Q(per_week=0) | Q(per_week__gt=F('te_week_done')) | Q(te_week_done__isnull=True)
    )

    StoreTaskAvail.objects.all().update(is_delete=True)

    for i in items:

        try:
            sta = StoreTaskAvail.objects.get(store_task_id=i.id)
        except StoreTaskAvail.DoesNotExist:
            sta = StoreTaskAvail()
            sta.store_task_id = i.id
            sta.update_time = datetime.datetime.now()

        if sta.deleted:
            sta.update_time = datetime.datetime.now()
            sta.deleted = False
            sta.lock_user_id = None

        sta.task_id = i.task_id
        sta.store_id = i.store_id
        sta.store_code = i.store.code
        sta.store_client_name = i.store.client.name
        sta.store_category_name = i.store.category.name if i.store.category else ''
        sta.store_region_name = i.store.region_o.name if i.store.region_o else ''
        sta.store_region_id = i.store.region_o.id if i.store.region_o else None
        sta.store_address = i.store.address
        sta.store_longitude = i.store.longitude
        sta.store_latitude = i.store.latitude
        sta.only_user_id = i.only_user_id
        sta.is_add_value = i.is_add_value
        sta.add_value = i.add_value
        sta.is_delete = False
        sta.telegram_channel_id = i.telegram_channel_id
        sta.position = i.position
        sta.save()

    StoreTaskAvail.objects.filter(is_delete=True, deleted=False).update(
        is_delete=False, update_time=datetime.datetime.now(), deleted=True
    )

    transaction.commit()

    cache.delete('celery_stores_tasks_refresh_process')

    return f'Stores tasks updated'


@shared_task(name='stores_tasks_renew')
def stores_tasks_renew():

    from application.survey.models import StoreTaskAvail

    # Сбрасываем все локи в начале дня
    StoreTaskAvail.objects.filter(lock_user_id__isnull=False).update(
        lock_user_id=None, update_time=datetime.datetime.now()
    )

    StoreTaskAvail.objects.filter(deleted=True).delete()


@shared_task(name='external_request_process')
def external_request_process():

    from application.survey.models import ExternalRequests

    tomorrow = datetime.datetime.now() - datetime.timedelta(days=1)

    requests = ExternalRequests.objects.filter(request_date__gte=tomorrow, processed=False).\
        order_by('request_date')

    if requests is None:
        return 'No requests'

    for i in requests:

        i.processed = True
        i.save()
        transaction.commit()

        try:

            i.result = 'Unknown data'

            if not i.request_text:
                i.request_data_count = 0
                i.request_data_type = 'empty'
                i.result = ''
                i.save()
                continue

            data = json.loads(i.request_text)

            if data.get('TerminalKey'):
                i.request_data_type = 'tinkoff payment'
                i.request_data_count = 1
                from application.agent.utils import tinkoff_payment
                i.result = tinkoff_payment(data)

            i.save()

        except:

            i.result = traceback.format_exc()
            i.save()

    return 'OK'


@shared_task(name='survey_import_tasks')
def survey_import_tasks(file, file_name, user=None):

    from application.survey.utils import survey_import_tasks_from_file

    survey_import_tasks_from_file(file, file_name, user=user)

    return 'OK'


@shared_task(name='delete_account_notifications')
def delete_account_notifications():

    from application.iceman.models import Notification as IcemanNotification
    from application.mobile.models import Notification as SurveyNotification
    from application.survey.models import UserDelete

    title = 'Удаление аккаунта'
    message = 'Скоро ваш аккаунт "{phone}" ({email}) будет удален со всеми данными и выполненными задачами. ' \
              'Если вы передумали, то зайдите в раздел "Кабинет" / "Удалить пользователя" и отмените удаление.'

    date = datetime.datetime.now() - datetime.timedelta(days=1)

    users_delete = UserDelete.objects.filter(date_create__lt=date, notification_send=False)

    for user_delete in users_delete:
        IcemanNotification(user=user_delete.user, title=title, message=message.format(
            email=user_delete.user.email, phone=user_delete.user.phone)).save()
        SurveyNotification(user=user_delete.user, title=title, message=message.format(
            email=user_delete.user.email, phone=user_delete.user.phone)).save()

        user_delete.notification_date = datetime.datetime.now()
        user_delete.notification_send = True
        user_delete.save()

    return 'OK'
