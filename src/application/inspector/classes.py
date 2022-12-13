import datetime
import json
import requests

from django.db import transaction

from preferences.utils import get_setting

from application.survey.models import TasksExecutionImage, Good as GoodAssortment, TasksExecutionAssortment, \
    TasksExecutionAssortmentBefore, TasksExecutionAssortmentAll

from .models import Good, Manufacturer, Brand, Category, InspectorGood


class Inspector:

    def __init__(self):
        self.url = get_setting('inspector_url')
        self.token = get_setting('inspector_token')
        self.headers = {'Authorization': 'Token %s' % self.token}
        self.headers_json = {'Authorization': 'Token %s' % self.token, 'content-type': 'application/json'}

    def parse_constructor(self, inspector_obj):

        inspector_obj.inspector_status = 'upload_wait'
        inspector_obj.save()
        transaction.commit()

        # Image uploads
        images = TasksExecutionImage.objects.filter(
            task=inspector_obj.task, constructor_step_name=inspector_obj.constructor_step_name)
        images_ids = []
        content = ''
        for i in images:
            try:
                message = self.upload_image(str(i))
                content += str(message) + '\n\n'
                image_id = message['id']
                images_ids.append(image_id)
            except:
                inspector_obj.inspector_upload_images_text = content
                inspector_obj.inspector_status = 'upload_error'
                inspector_obj.save()
                transaction.commit()
                return

        inspector_obj.inspector_upload_images_text = content
        inspector_obj.save()

        if len(images_ids) < 1:
            inspector_obj.inspector_status = 'upload_error'
            inspector_obj.save()
            transaction.commit()
            return

        # Recognize
        data = self.recognize(images_ids)
        inspector_obj.inspector_recognize_text = data
        inspector_obj.save()

        try:
            report_id = data['reports']['FACING_COUNT']
        except:
            inspector_obj.inspector_status = 'parse_error'
            inspector_obj.save()
            transaction.commit()
            return

        # Report
        inspector_obj.inspector_status = 'report_wait'
        inspector_obj.inspector_report_id = report_id
        inspector_obj.save()
        transaction.commit()


    def parse(self, te_obj):

        te_obj.inspector_status = 'upload_wait'
        te_obj.save()

        transaction.commit()

        # Image uploads
        images = TasksExecutionImage.objects.filter(task=te_obj, type='after')
        images_ids = []
        content = ''
        for i in images:
            try:
                message = self.upload_image(str(i))
                content += str(message) + '\n\n'
                image_id = message['id']
                images_ids.append(image_id)
            except:
                te_obj.inspector_upload_images_text = content
                te_obj.inspector_status = 'upload_error'
                te_obj.save()
                transaction.commit()
                return

        te_obj.inspector_upload_images_text = content
        te_obj.save()

        if len(images_ids) < 1:
            te_obj.inspector_status = 'upload_error'
            te_obj.save()
            transaction.commit()
            return

        # Recognize
        data = self.recognize(images_ids)
        te_obj.inspector_recognize_text = data
        te_obj.save()

        try:
            report_id = data['reports']['FACING_COUNT']
        except:
            te_obj.inspector_status = 'parse_error'
            te_obj.save()
            transaction.commit()
            return

        # Report
        te_obj.inspector_status = 'report_wait'
        te_obj.inspector_report_id = report_id
        te_obj.save()
        transaction.commit()

    def parse_before(self, te_obj):

        te_obj.inspector_status_before = 'upload_wait'
        te_obj.save()

        transaction.commit()

        # Image uploads
        images = TasksExecutionImage.objects.filter(task=te_obj, type='before')
        images_ids = []
        content = ''
        for i in images:
            message = self.upload_image(str(i))
            content += str(message) + '\n\n'
            try:
                image_id = message['id']
                images_ids.append(image_id)
            except:
                pass

        if len(images_ids) < 1:
            te_obj.inspector_status_before = 'upload_error'
            te_obj.save()
            transaction.commit()
            return

        # Recognize
        data = self.recognize(images_ids)

        try:
            report_id = data['reports']['FACING_COUNT']
        except:
            te_obj.inspector_status_before = 'parse_error'
            te_obj.save()
            transaction.commit()
            return

        # Report
        te_obj.inspector_status_before = 'report_wait'
        te_obj.inspector_report_id_before = report_id
        te_obj.save()
        transaction.commit()

    def report_constructor(self, inspector_obj):

        s = '; '

        inspector_obj.inspector_status = 'report_process'
        inspector_obj.save()
        transaction.commit()

        data = self.get_report(inspector_obj.inspector_report_id)
        inspector_obj.inspector_report_text = json.dumps(data)
        inspector_obj.save()

        try:
            status = data['status']
        except:
            inspector_obj.inspector_status = 'report_error'
            inspector_obj.save()
            transaction.commit()
            return s

        if status != 'NOT_READY' and status != 'READY':
            inspector_obj.inspector_status = 'report_error'
            inspector_obj.save()
            transaction.commit()
            return s

        if status == 'NOT_READY':
            inspector_obj.inspector_status = 'report_wait'
            inspector_obj.save()
            transaction.commit()
            return s

        if status == 'READY':
            s += self.goods_constructor(inspector_obj)
            inspector_obj.inspector_status = 'success'
            inspector_obj.save()
            inspector_obj.task.inspector_status = 'success'
            inspector_obj.task.save(update_fields=['inspector_status'])
            transaction.commit()
            return s

    def report(self, te_obj):

        s = '; '

        te_obj.inspector_status = 'report_process'
        te_obj.save()

        transaction.commit()

        data = self.get_report(te_obj.inspector_report_id)

        te_obj.inspector_report_text = json.dumps(data)
        te_obj.save()

        try:
            status = data['status']
        except:
            te_obj.inspector_status = 'report_error'
            te_obj.save()
            transaction.commit()
            return s

        if status != 'NOT_READY' and status != 'READY':
            te_obj.inspector_status = 'report_error'
            te_obj.save()
            transaction.commit()
            return s

        if status == 'NOT_READY':
            te_obj.inspector_status = 'report_wait'
            te_obj.save()
            transaction.commit()
            return s

        if status == 'READY':
            s += self.goods(te_obj)
            te_obj.inspector_status = 'success'
            te_obj.save()
            transaction.commit()
            return s

    def report_before(self, te_obj):

        te_obj.inspector_status_before = 'report_process'
        te_obj.save()

        transaction.commit()

        data = self.get_report(te_obj.inspector_report_id_before)

        try:
            status = data['status']
        except:
            te_obj.inspector_status_before = 'report_error'
            te_obj.save()
            transaction.commit()
            return

        if status != 'NOT_READY' and status != 'READY':
            te_obj.inspector_status_before = 'report_error'
            te_obj.save()
            transaction.commit()
            return

        if status == 'NOT_READY':
            te_obj.inspector_status_before = 'report_wait'
            te_obj.save()
            transaction.commit()
            return

        if status == 'READY':
            self.goods_before(te_obj, data)
            te_obj.inspector_status_before = 'success'
            te_obj.save()
            transaction.commit()
            return

    def goods_constructor(self, inspector_obj):

        ss = ' ** '

        data = json.loads(inspector_obj.inspector_report_text)
        today = datetime.datetime.now()

        s = ''
        for i in data['json']:

            try:
                good = Good.objects.get(sku_id=i['sku_id'])
                if good.date_update < today - datetime.timedelta(days=3):
                    # ss += 'good loaded ' + str(i['sku_id'])
                    try:
                        data_sku = self.get_sku(i['sku_id'])
                        good.name = data_sku['name']
                        good.cid = data_sku['cid']
                        good.date_update = today
                        good.save()
                    except:
                        good.date_update = today
                        good.save()
                        # import traceback
                        # tb = traceback.format_exc()
                        # ss += ' ____ ' + str(tb)
                cid = good.cid
            except Good.DoesNotExist:
                data_sku = self.get_sku(i['sku_id'])
                cid = data_sku['cid']
                try:
                    good = Good(name=data_sku['name'], sku_id=i['sku_id'], cid=data_sku['cid'])
                    good.date_update = today
                    good.save()
                except:
                    pass

            if cid:
                ga = GoodAssortment.objects.filter(code=cid).first()
                if ga:
                    tea_obj_old = TasksExecutionAssortment.objects.filter(
                        task=inspector_obj.task, good=ga, constructor_step_name=inspector_obj.constructor_step_name).count()
                    if tea_obj_old < 1:
                        tea_obj = TasksExecutionAssortment()
                        tea_obj.task = inspector_obj.task
                        tea_obj.good = ga
                        tea_obj.avail = i['count']
                        tea_obj.constructor_step_name = inspector_obj.constructor_step_name
                        tea_obj.save()

            try:
                ig = InspectorGood.objects.get(sku_id=i['sku_id'])
            except InspectorGood.DoesNotExist:

                try:
                    data_sku = self.get_sku(i['sku_id'])

                    try:
                        manufacturer = self.get_manufacturer(data_sku['manufacturer'])
                    except:
                        manufacturer = None
                    try:
                        brand = self.get_brand(data_sku['brand'])
                    except:
                        brand = None
                    try:
                        category = self.get_category(data_sku['category'])
                    except:
                        category = None

                    ig = InspectorGood(sku_id=i['sku_id'])

                    try:
                        ig.cid = cid
                    except:
                        pass

                    ig.category = category
                    ig.brand = brand
                    ig.manufacturer = manufacturer
                    try:
                        ig.name = data_sku['name']
                    except:
                        ig.name = 'Другой товар'
                    ig.save()
                except:
                    ig = None

            if ig and not inspector_obj.inspector_is_alert:
                tea_a_obj = TasksExecutionAssortmentAll()
                tea_a_obj.task = inspector_obj.task
                tea_a_obj.good = ig
                tea_a_obj.avail = i['count']
                tea_a_obj.save()

            try:
                s += '%s - %s - %s\n' % (good.name, cid, i['count'])
            except:
                s += '%s - %s - %s\n' % ('None', cid, i['count'])

        inspector_obj.inspector_positions_text = s
        inspector_obj.save()

        return ss


    def goods(self, te_obj):

        ss = ' ** '

        data = json.loads(te_obj.inspector_report_text)
        today = datetime.datetime.now()

        s = ''
        for i in data['json']:

            try:
                good = Good.objects.get(sku_id=i['sku_id'])
                if good.date_update < today - datetime.timedelta(days=3):
                    # ss += 'good loaded ' + str(i['sku_id'])
                    try:
                        data_sku = self.get_sku(i['sku_id'])
                        good.name = data_sku['name']
                        good.cid = data_sku['cid']
                        good.date_update = today
                        good.save()
                    except:
                        good.date_update = today
                        good.save()
                        # import traceback
                        # tb = traceback.format_exc()
                        # ss += ' ____ ' + str(tb)
                cid = good.cid
            except Good.DoesNotExist:
                data_sku = self.get_sku(i['sku_id'])
                cid = data_sku['cid']
                try:
                    good = Good(name=data_sku['name'], sku_id=i['sku_id'], cid=data_sku['cid'])
                    good.date_update = today
                    good.save()
                except:
                    pass

            if cid:
                ga = GoodAssortment.objects.filter(code=cid).first()
                if ga:
                    tea_obj_old = TasksExecutionAssortment.objects.filter(task=te_obj, good=ga).count()
                    if tea_obj_old < 1:
                        tea_obj = TasksExecutionAssortment()
                        tea_obj.task = te_obj
                        tea_obj.good = ga
                        tea_obj.avail = i['count']
                        tea_obj.save()

            try:
                ig = InspectorGood.objects.get(sku_id=i['sku_id'])
            except InspectorGood.DoesNotExist:

                try:
                    data_sku = self.get_sku(i['sku_id'])

                    try:
                        manufacturer = self.get_manufacturer(data_sku['manufacturer'])
                    except:
                        manufacturer = None
                    try:
                        brand = self.get_brand(data_sku['brand'])
                    except:
                        brand = None
                    try:
                        category = self.get_category(data_sku['category'])
                    except:
                        category = None

                    ig = InspectorGood(sku_id=i['sku_id'])

                    try:
                        ig.cid = cid
                    except:
                        pass

                    ig.category = category
                    ig.brand = brand
                    ig.manufacturer = manufacturer
                    try:
                        ig.name = data_sku['name']
                    except:
                        ig.name = 'Другой товар'
                    ig.save()
                except:
                    ig = None

            if ig:
                tea_a_obj = TasksExecutionAssortmentAll()
                tea_a_obj.task = te_obj
                tea_a_obj.good = ig
                tea_a_obj.avail = i['count']
                tea_a_obj.save()

            try:
                s += '%s - %s - %s\n' % (good.name, cid, i['count'])
            except:
                s += '%s - %s - %s\n' % ('None', cid, i['count'])

        te_obj.inspector_positions_text = s
        te_obj.save()

        return ss

    def goods_before(self, te_obj, data):

        today = datetime.datetime.now()

        s = ''

        for i in data['json']:

            try:
                good = Good.objects.get(sku_id=i['sku_id'])
                if good.date_update < today - datetime.timedelta(days=3):
                    try:
                        data_sku = self.get_sku(i['sku_id'])
                        good.name = data_sku['name']
                        good.cid = data_sku['cid']
                        good.date_update = today
                        good.save()
                    except:
                        good.date_update = today
                        good.save()
                cid = good.cid
            except Good.DoesNotExist:
                data_sku = self.get_sku(i['sku_id'])
                cid = data_sku['cid']
                try:
                    good = Good(name=data_sku['name'], sku_id=i['sku_id'], cid=data_sku['cid'])
                    good.date_update = today
                    good.save()
                except:
                    pass

            if cid:
                ga = GoodAssortment.objects.filter(code=cid).first()
                if ga:
                    tea_obj_old = TasksExecutionAssortmentBefore.objects.filter(task=te_obj, good=ga).count()
                    if tea_obj_old < 1:
                        tea_obj = TasksExecutionAssortmentBefore()
                        tea_obj.task = te_obj
                        tea_obj.good = ga
                        tea_obj.avail = i['count']
                        tea_obj.save()

    def upload_image(self, image_file):

        data = {}
        files = {'datafile': open(image_file, 'rb')}

        response = requests.post(self.url + 'uploads/', data=data, headers=self.headers, files=files)

        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            return data

        return data

    def recognize(self, images_ids):

        data = {'images': images_ids, 'report_types': ['FACING_COUNT'], 'retail_chain': 'chl_bot'}

        response = requests.post(self.url + 'recognize/', data=json.dumps(data), headers=self.headers_json)

        return response.json()

    def get_report(self, report_id):
        response = requests.get(self.url + 'reports/%s/' % report_id, headers=self.headers, timeout=5)
        return response.json()

    def get_sku(self, sku_id):
        response = requests.get(self.url + 'sku/%s/' % sku_id, headers=self.headers_json)
        return response.json()

    def get_manufacturers(self):
        response = requests.get(self.url + 'manufacturers/', headers=self.headers_json)
        data = response.json()

        while True:
            if data.get('next'):

                for i in data['results']:
                    print(i['name'], i['id'])

                response = requests.get(data.get('next'), headers=self.headers_json)
                data = response.json()
            else:
                return

    def get_goods(self):
        response = requests.get(self.url + 'sku/?limit=1000', headers=self.headers_json)
        data = response.json()

        while True:
            if data.get('next'):

                for i in data['results']:
                    if i['manufacturer'] == 373:
                        print(i['name'], i['id'], i['cid'])

                response = requests.get(data.get('next'), headers=self.headers_json)
                data = response.json()
            else:
                return

    def get_manufacturer(self, sid):
        if not sid:
            return None
        response = requests.get(self.url + 'manufacturers/%s/' % sid, headers=self.headers_json)
        try:
            m, created = Manufacturer.objects.get_or_create(internal_id=sid)
            m.name = response.json()['name']
            m.save()
            return m
        except:
            return None

    def get_brand(self, sid):
        if not sid:
            return None
        response = requests.get(self.url + 'brands/%s/' % sid, headers=self.headers_json)
        try:
            m, created = Brand.objects.get_or_create(internal_id=sid)
            m.name = response.json()['name']
            m.save()
            return m
        except:
            return None

    def get_category(self, sid):
        if not sid:
            return None
        response = requests.get(self.url + 'categories/%s/' % sid, headers=self.headers_json)
        try:
            m, created = Category.objects.get_or_create(internal_id=sid)
            m.name = response.json()['name']
            m.save()
            return m
        except:
            return None

