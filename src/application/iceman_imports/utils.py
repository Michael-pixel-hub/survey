import pandas as pd
import math
import os

from datetime import datetime
from django.core.cache import cache
from django.core.files import File
from django.db import transaction
from django.db.models import Q

from .models import ImportStores, ImportTasks, ImportProducts


def excel_get_string(val, max_length=None):

    if type(val) == float:
        val = str(val).replace('.0', '')

    if type(val) == int:
        val = str(val).replace('.', '')

    val = str(val)

    if max_length is not None:
        val = val[:max_length]

    if val == 'nan':
        return None

    return str(val)


def iceman_import_stores_from_file(file, file_name, user=None):

    import_obj = ImportStores(file_name=file_name, user_id=user)
    import_obj.save()
    transaction.commit()

    with open(file, 'rb') as fi:
        import_obj.file = File(fi, name=os.path.basename(fi.name))
        import_obj.save()
        transaction.commit()

    try:

        # Начало
        data = pd.read_excel(file, sheet_name=0, header=0)
        import_obj.rows_count = len(data)
        import_obj.save()
        transaction.commit()

        # Работа импорта
        iceman_import_stores_from_file_process(data, import_obj)

        # Завершение
        import_obj.rows_process = import_obj.rows_count
        import_obj.status = 2
        import_obj.date_end = datetime.now()
        import_obj.save()

    except Exception as e:
        import_obj.status = 4
        import_obj.report_text = e
        import_obj.save()
        return


@transaction.atomic
def iceman_import_stores_from_file_process(data, import_obj):

    from application.iceman.models import Source, Region, Stock, Store, StoreStock

    required_columns = ['Название', 'Источник', 'Код', 'Регион', 'Адрес', 'Склад']

    # Обязательные колонки
    for i in required_columns:
        if i not in data.columns:
            raise Exception(f'Колонка "{i}" не обнаружена в Excel-файле. '
                            f'Названия колонок должно быть в первой строке таблицы.')

    # Обработка
    sid = transaction.savepoint()
    for index, row in data.iterrows():

        if cache.get('iceman_import_stores_cancel'):
            transaction.savepoint_rollback(sid)
            cache.delete('iceman_import_stores_cancel')
            import_obj.status = 3
            import_obj.save()
            return

        # Источник
        source_name = excel_get_string(row['Источник'])
        source = Source.objects.filter(Q(name=source_name) | Q(sys_name=source_name)).first()
        if source is None:
            transaction.savepoint_rollback(sid)
            raise Exception(f'Источник "{source_name}" не найден.')

        # Регион
        region_name = excel_get_string(row['Регион'])
        region = Region.objects.filter(
            Q(name=region_name) | Q(short_name=region_name) | Q(short_name_2=region_name) | Q(name_1c=region_name)
            | Q(name_1c_2=region_name)).first()
        if region is None:
            transaction.savepoint_rollback(sid)
            raise Exception(f'Регион "{region_name}" не найден.')

        # Склад
        stock_name = excel_get_string(row['Склад'])
        if stock_name is None:
            transaction.savepoint_rollback(sid)
            raise Exception(f'Склад не может быть пустым.')
        stock = Stock.objects.filter(Q(name=stock_name) | Q(sys_name=stock_name)).first()
        if stock is None:
            transaction.savepoint_rollback(sid)
            raise Exception(f'Склад "{stock_name}" не найден.')

        # Добавляем магазин
        code = excel_get_string(row['Код'])
        if code is None:
            transaction.savepoint_rollback(sid)
            raise Exception(f'Код не может быть пустым.')
        try:
            store = Store.objects.get(code=code)
        except Store.DoesNotExist:
            store = Store(code=code)
        if not store.name:
            store.name = excel_get_string(row['Название'])
        store.source = source
        store.region = region
        store.stock = stock

        address = excel_get_string(row['Адрес'])
        if address is None:
            transaction.savepoint_rollback(sid)
            raise Exception(f'Адрес не может быть пустым.')
        if row.get('Долгота') and row.get('Широта') and not math.isnan(row['Долгота']) \
                and not math.isnan(row['Широта']):
            store.longitude = row['Долгота']
            store.latitude = row['Широта']
        else:
            if store.address != address:
                store.auto_coord = True
        store.address = address

        if row.get('ИНН') and excel_get_string(row['ИНН']) is not None:
            if excel_get_string(row['ИНН']) != store.inn:
                store.inn_auto = True
            store.inn = excel_get_string(row['ИНН'])

        if row.get('Договор') and excel_get_string(row['Договор']) == 'Да':
            store.is_agreement = True

        if row.get('Телефон') and excel_get_string(row['Телефон']) is not None:
            phone = excel_get_string(row['Телефон'])
            if phone.startswith('7'):
                phone = f'+{phone}'
            store.lpr_phone = phone

        if row.get('ФИО') and excel_get_string(row['ФИО']) is not None:
            store.lpr_fio = str(row['ФИО'])

        if row.get('Тип цены') and excel_get_string(row['Тип цены']) is not None:
            store.price_type = excel_get_string(row['Тип цены'])

        if row.get('Дни доставки') and excel_get_string(row['Дни доставки']) is not None:
            store.schedule = excel_get_string(row['Дни доставки']).replace('.', ',')

        if row.get('Отсрочка'):
            payment_days = row['Отсрочка']
            if not math.isnan(row['Отсрочка']):
                try:
                    payment_days = int(payment_days)
                    store.payment_days = payment_days
                except:
                    transaction.savepoint_rollback(sid)
                    raise Exception(f'Отсрочка "{payment_days}" должна быть числом кол-во дней.')

        if row.get('Задача продажи'):
            if excel_get_string(row['Задача продажи']) == 'Да':
                store.is_order_task = True
            else:
                store.is_order_task = False

        store.save()

        # Склад
        try:
            StoreStock.objects.get(store=store, stock=stock)
        except StoreStock.DoesNotExist:
            store_stock = StoreStock(store=store, stock=stock)
            store_stock.save()

        # Новая строка
        import_obj.rows_process = index
        import_obj.save()

    transaction.savepoint_commit(sid)


def iceman_import_tasks_from_file(file, file_name, user=None):

    import_obj = ImportTasks(file_name=file_name, user_id=user)
    import_obj.save()
    transaction.commit()

    with open(file, 'rb') as fi:
        import_obj.file = File(fi, name=os.path.basename(fi.name))
        import_obj.save()
        transaction.commit()

    try:

        # Начало
        data = pd.read_excel(file, sheet_name=0, header=0)
        import_obj.rows_count = len(data)
        import_obj.save()
        transaction.commit()

        # Работа импорта
        iceman_import_tasks_from_file_process(data, import_obj)

        # Завершение
        import_obj.rows_process = import_obj.rows_count
        import_obj.status = 2
        import_obj.date_end = datetime.now()
        import_obj.save()

    except Exception as e:
        import_obj.status = 4
        import_obj.report_text = e
        import_obj.save()
        return


@transaction.atomic
def iceman_import_tasks_from_file_process(data, import_obj):

    from application.iceman.models import Store, User, StoreTaskSchedule
    from application.survey.models import Task

    required_columns = ['Код магазина', 'Задача']

    # Обязательные колонки
    for i in required_columns:
        if i not in data.columns:
            raise Exception(f'Колонка "{i}" не обнаружена в Excel-файле. '
                            f'Названия колонок должно быть в первой строке таблицы.')

    # Обработка
    sid = transaction.savepoint()
    for index, row in data.iterrows():

        # Отмена
        if cache.get('iceman_import_tasks_cancel'):
            transaction.savepoint_rollback(sid)
            cache.delete('iceman_import_tasks_cancel')
            import_obj.status = 3
            import_obj.save()
            return

        # Магазин
        store_code = excel_get_string(row['Код магазина'], 100)
        store = Store.objects.filter(code=store_code).first()
        if store is None:
            transaction.savepoint_rollback(sid)
            raise Exception(f'Магазин с кодом "{store_code}" не найден.')

        # Задача
        task_name = excel_get_string(row['Задача'], 100)
        task = Task.objects.filter(name=task_name, application='iceman').first()
        if task is None:
            transaction.savepoint_rollback(sid)
            raise Exception(f'Задача "{task_name}" не найдена в списке задач Айсмена.')

        # Расписание
        schedule = None
        if row.get('Расписание'):
            schedule = excel_get_string(row['Расписание'], 100)

        # Пользователь
        user = None
        if row.get('Пользователь'):
            user_email = excel_get_string(row['Пользователь'], 100)
            if user_email is not None and user_email != '':
                user = User.objects.filter(email=user_email).first()

        # Удаляем расписание
        if schedule is None or schedule == '':

            try:
                sts_obj = StoreTaskSchedule.objects.get(store=store, task=task)
                if sts_obj is not None:
                    sts_obj.delete()
            except StoreTaskSchedule.DoesNotExist:
                pass

            import_obj.rows_process = index
            import_obj.save()
            continue

        # Делаем в расписании
        try:
            sts_obj = StoreTaskSchedule.objects.get(store=store, task=task)
        except StoreTaskSchedule.DoesNotExist:
            sts_obj = StoreTaskSchedule(store=store, task=task)

        if schedule == '*':
            sts_obj.is_once = True
            sts_obj.per_week = None
            sts_obj.per_month = None
            sts_obj.days_of_week = ''
        elif schedule.startswith('**'):
            try:
                months = int(schedule.replace('**', ''))
                sts_obj.per_month = months
                sts_obj.days_of_week = ''
                sts_obj.per_week = None
                sts_obj.is_once = False
            except:
                transaction.savepoint_rollback(sid)
                raise Exception(f'Неверное расписание: {schedule}')
        elif schedule.startswith('*'):
            try:
                days = int(schedule.replace('*', ''))
                sts_obj.per_week = days
                sts_obj.days_of_week = ''
                sts_obj.is_once = False
                sts_obj.per_month = None
            except:
                transaction.savepoint_rollback(sid)
                raise Exception(f'Неверное расписание: {schedule}')
        else:
            sts_obj.days_of_week = schedule.replace('.', ',')
            sts_obj.days_of_week = sts_obj.days_of_week.replace(',0', '')
            sts_obj.is_once = False
            sts_obj.per_week = None
            sts_obj.per_month = None

        sts_obj.only_user = user
        sts_obj.save()

        # Новая строка
        import_obj.rows_process = index
        import_obj.save()

    transaction.savepoint_commit(sid)


@transaction.atomic
def iceman_import_products_from_file(file, file_name, user=None):

    def save_error(s):
        import_obj.status = 4
        import_obj.report_text = s
        import_obj.save()

    from application.iceman.models import Source, Category, Brand, Stock, Product, SourceProduct, SourceProductPrice, \
        ProductStock

    import_obj = ImportProducts(file_name=file_name, user_id=user)
    import_obj.save()

    with open(file, 'rb') as fi:
        import_obj.file = File(fi, name=os.path.basename(fi.name))
        import_obj.save()

    required_columns = ['Название', 'Источник', 'Код', 'Раздел', 'Производитель', 'Ед. измерения', 'Кол-во в коробке',
                        'Минимальное кол-во', 'Цена', 'Штрихкод', 'Вес', 'Склад', 'Количество']

    try:
        # Начало
        data = pd.read_excel(file, sheet_name=0, header=0)
        import_obj.rows_count = len(data)
        import_obj.save()

        # Обязательные колонки
        for i in required_columns:
            if i not in data.columns:
                save_error(f'Колонка "{i}" не обнаружена в Excel-файле. '
                           f'Названия колонок должно быть в первой строке таблицы.')
                return

        # Обработка
        sources = []
        sid = transaction.savepoint()
        for index, row in data.iterrows():

            # Отмена
            if cache.get('iceman_import_products_cancel'):
                transaction.savepoint_rollback(sid)
                cache.delete('iceman_import_products_cancel')
                import_obj.status = 3
                import_obj.save()
                return

            # Источник
            source_name = excel_get_string(row['Источник'], 255)
            source = Source.objects.filter(Q(name=source_name) | Q(sys_name=source_name)).first()
            if source is None:
                transaction.savepoint_rollback(sid)
                save_error(f'Источник "{source_name}" не найден.')
                return
            if source not in sources:
                sources.append(source)
                SourceProduct.objects.filter(source=source).update(is_updated=False)

            # Название
            name = excel_get_string(row['Название'], 200)

            # Код
            code = excel_get_string(row['Код'], 100)

            # Раздел
            categories = []
            categories_name = excel_get_string(row['Раздел'], 200)
            categories_names = categories_name.split(',')
            for category_name in categories_names:
                category_name = category_name.strip()
                try:
                    category = Category.objects.get(name=category_name)
                except Category.DoesNotExist:
                    category = Category(name=category_name)
                    category.save()
                categories.append(category)

            # Производитель
            brand_name = excel_get_string(row['Производитель'], 200)
            try:
                brand = Brand.objects.get(name=brand_name)
            except Brand.DoesNotExist:
                brand = Brand(name=brand_name)
                brand.save()

            # Ед.измерения
            unit = excel_get_string(row['Ед. измерения'], 100)

            # Кол-во в коробке
            box_count = row['Кол-во в коробке']
            try:
                box_count = int(box_count)
            except:
                transaction.savepoint_rollback(sid)
                save_error(f'Кол-во в коробке "{box_count}" не является числом.')
                return

            # Минимальное кол-во
            min_count = row['Минимальное кол-во']
            try:
                min_count = int(min_count)
            except:
                transaction.savepoint_rollback(sid)
                save_error(f'Минимальное кол-во "{min_count}" не является числом.')
                return

            # Тип цены
            price_type = None
            if row.get('Тип цены'):
                price_type = excel_get_string(row['Тип цены'], 255)

            # Цена
            price = row['Цена']
            try:
                if type(price) == str:
                    price = float(price.replace(',', '.'))
                price = round(price, 2)
            except:
                transaction.savepoint_rollback(sid)
                save_error(f'Цена "{price}" не является числом.')
                return

            # Штрихкод
            barcode = excel_get_string(row['Штрихкод'])
            if len(barcode) > 15:
                transaction.savepoint_rollback(sid)
                save_error(f'Штрихкод "{barcode}" больше 15 символов.')
                return
            barcode = excel_get_string(barcode)

            # Вес
            weight = row['Вес']
            try:
                weight = int(weight)
            except:
                transaction.savepoint_rollback(sid)
                save_error(f'Вес "{weight}" не является числом.')
                return

            # Бонусный товар
            is_bonus = False
            if row.get('Бонус') == 'Да':
                is_bonus = True

            # Склад
            stock_name = excel_get_string(row['Склад'], 255)
            stock = Stock.objects.filter(Q(name=stock_name) | Q(sys_name=stock_name)).first()
            if stock is None:
                transaction.savepoint_rollback(sid)
                save_error(f'Склад "{stock_name}" не найден.')
                return

            # Количество
            count = row['Количество']
            try:
                count = int(count)
            except:
                transaction.savepoint_rollback(sid)
                save_error(f'Количество "{count}" не является числом.')
                return

            # Ищем и создаем товар
            try:
                product = Product.objects.get(barcode=barcode)
            except Product.DoesNotExist:
                product = Product()
                product.code = code
                product.name = name
                product.brand = brand
                product.unit = unit
                product.box_count = box_count
                product.min_count = min_count
                product.price = price
                product.barcode = barcode
                product.weight = weight
                product.save()
                for i in categories:
                    product.categories.add(i)
                product.save()

            # Товар в магазине
            try:
                sp = SourceProduct.objects.get(product=product, source=source)
            except SourceProduct.DoesNotExist:
                sp = SourceProduct(product=product, source=source)
            sp.is_updated = True
            sp.unit = unit
            sp.box_count = box_count
            sp.min_count = min_count
            if price_type is None:
                sp.price = price
            else:
                if sp.price == 0:
                    sp.price = price
            sp.is_bonus = is_bonus
            sp.save()

            # Тип цены
            if price_type is not None:
                try:
                    spp = SourceProductPrice.objects.get(product=sp, price_type=price_type)
                except:
                    spp = SourceProductPrice(product=sp, price_type=price_type)
                spp.price = price
                spp.save()

            # Товар на складе
            try:
                product_stock = ProductStock.objects.get(product=product, stock=stock)
            except ProductStock.DoesNotExist:
                product_stock = ProductStock(product=product, stock=stock)
            product_stock.count = count
            product_stock.save()

            try:
                ImportProducts.objects.get(status=1)
            except ImportProducts.DoesNotExist:
                return

            import_obj.rows_process = index
            import_obj.save()

        SourceProduct.objects.filter(is_updated=False).delete()
        transaction.savepoint_commit(sid)

        # Завершение
        import_obj.rows_process = import_obj.rows_count
        import_obj.status = 2
        import_obj.date_end = datetime.now()
        import_obj.save()

    except Exception as e:
        #var = traceback.format_exc()
        save_error(e)
        return
