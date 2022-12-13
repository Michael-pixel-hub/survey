import collections
import hashlib
import random
import requests
import string

from django.utils.translation import ugettext_lazy as _
from preferences.utils import get_setting

from .models import SolarStaffPayments
from application.solar_staff_accounts.models import SolarStaffAccount
from application.survey.models import Request


class SolarStaff:

    salt = None
    client_id = None

    def __init__(self, salt=None, client_id=None):

        self.salt = salt
        self.client_id = client_id

    def worker_create(self, email, first_name, last_name):

        client_id = self.client_id if self.client_id is not None else get_setting('solar_staff_clientid')

        password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        upper_letter = random.choice(string.ascii_uppercase)
        password = f'{upper_letter}{password}'
        response = self.make_request(
            'workers',
            action='worker_create',
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            country='RU',
            send_message=1,
            specialization=409,
            client_id=client_id
        )

        return response

    def make_request(self, url, **kwargs):
        params = self.make_params(kwargs)
        response = requests.post('https://api.solar-staff.com/v1/%s' % url, params)
        Request(
            method='POST', url='https://api.solar-staff.com/v1/%s' % url, body=str(params), result=response.text
        ).save()
        return response.json()

    def make_params(self, params):

        salt = self.salt if self.salt is not None else get_setting('solar_staff_salt')

        params = collections.OrderedDict(sorted(params.items()))
        s = ''
        for key, value in params.items():
            s += '%s:%s;' % (key, value)
        s = '%s%s' % (s, salt)
        params['signature'] = hashlib.sha1(s.encode('utf-8')).hexdigest()
        return params

    def payout(self, te):

        client_id = self.client_id if self.client_id is not None else get_setting('solar_staff_clientid')

        solar_obj = SolarStaffPayments()
        try:
            account = SolarStaffAccount.objects.filter(client_id=client_id).first()
            if account:
                solar_obj.account = account
        except:
            pass

        solar_obj.te = te
        solar_obj.sum = round(te.task.money)

        if not te.user.email:
            solar_obj.server_code = 100
            solar_obj.server_error = _('User does not have an email field')
            solar_obj.save()
            return False

        if not te.user.name:
            solar_obj.server_code = 100
            solar_obj.server_error = _('User does not have name field')
            solar_obj.save()
            return False

        if not te.user.surname:
            solar_obj.server_code = 100
            solar_obj.server_error = _('User does not have surname field')
            solar_obj.save()
            return False

        solar_obj.email = te.user.email
        solar_obj.first_name = te.user.name
        solar_obj.last_name = te.user.surname

        result = self.worker_create(te.user.email, te.user.name, te.user.surname)
        if not result['success']:
            solar_obj.server_code = 100
            solar_obj.server_error = _('Error while user create')
            solar_obj.server_response = result
            solar_obj.save()
            return False

        response = self.make_request(
            'payment',
            action='payout',
            email=te.user.email,
            currency='RUB',
            amount=round(te.money if te.money else te.task.money),
            task_title='Задача в боте',
            task_description=te.id,
            client_id=client_id,
            todo_type='2889',
            todo_attributes='Мороженое ЧЛ',
            merchant_transaction=te.id,
        )

        if response.get('success'):
            solar_obj.server_code = response['response']['status_id']
            solar_obj.server_response = response
            solar_obj.save()
            return True

        try:
            solar_obj.server_code = response['response']['status_id']
            try:
                solar_obj.server_error = response['response']['error_text']
            except:
                pass
            solar_obj.server_response = response
            solar_obj.save()
            return True
        except:
            solar_obj.server_code = 100
            try:
                solar_obj.server_error = response['response']['error_text']
            except:
                pass
            solar_obj.server_response = response
            solar_obj.save()
            return False

    def payout_payment(self, payment):

        client_id = self.client_id if self.client_id is not None else get_setting('solar_staff_clientid')

        solar_obj = SolarStaffPayments()

        try:
            account = SolarStaffAccount.objects.filter(client_id=client_id).first()
            if account:
                solar_obj.account = account
        except:
            pass

        solar_obj.type = 3
        solar_obj.sum = round(payment.sum)

        if not payment.user.email:
            solar_obj.server_code = 100
            solar_obj.server_error = _('User does not have an email field')
            solar_obj.save()
            return False

        if not payment.user.name:
            solar_obj.server_code = 100
            solar_obj.server_error = _('User does not have name field')
            solar_obj.save()
            return False

        if not payment.user.surname:
            solar_obj.server_code = 100
            solar_obj.server_error = _('User does not have surname field')
            solar_obj.save()
            return False

        solar_obj.email = payment.user.email
        solar_obj.first_name = payment.user.name
        solar_obj.last_name = payment.user.surname

        result = self.worker_create(payment.user.email, payment.user.name, payment.user.surname)
        if not result['success']:
            solar_obj.server_code = 100
            solar_obj.server_error = _('Error while user create')
            solar_obj.server_response = result
            solar_obj.save()
            return False

        response = self.make_request(
            'payment',
            action='payout',
            email=payment.user.email,
            currency='RUB',
            amount=round(payment.sum),
            task_title='Кешбек заказа',
            task_description=payment.id,
            client_id=client_id,
            todo_type='2889',
            todo_attributes='Мороженое ЧЛ',
            merchant_transaction='PAYMENT%s' % payment.id,
        )

        if response.get('success'):
            solar_obj.server_code = response['response']['status_id']
            solar_obj.server_response = response
            solar_obj.save()
            return True

        try:
            solar_obj.server_code = response['response']['status_id']
            try:
                solar_obj.server_error = response['response']['error_text']
            except:
                pass
            solar_obj.server_response = response
            solar_obj.save()
            return True
        except:
            solar_obj.server_code = 100
            try:
                solar_obj.server_error = response['response']['error_text']
            except:
                pass
            solar_obj.server_response = response
            solar_obj.save()
            return False


    def payout_order(self, order):

        client_id = self.client_id if self.client_id is not None else get_setting('solar_staff_clientid')

        solar_obj = SolarStaffPayments()

        try:
            account = SolarStaffAccount.objects.filter(client_id=client_id).first()
            if account:
                solar_obj.account = account
        except:
            pass

        solar_obj.type = 2
        solar_obj.order = order
        solar_obj.sum = round(order.cashback_sum)

        if not order.user.email:
            solar_obj.server_code = 100
            solar_obj.server_error = _('User does not have an email field')
            solar_obj.save()
            return False

        if not order.user.name:
            solar_obj.server_code = 100
            solar_obj.server_error = _('User does not have name field')
            solar_obj.save()
            return False

        if not order.user.surname:
            solar_obj.server_code = 100
            solar_obj.server_error = _('User does not have surname field')
            solar_obj.save()
            return False

        solar_obj.email = order.user.email
        solar_obj.first_name = order.user.name
        solar_obj.last_name = order.user.surname

        result = self.worker_create(order.user.email, order.user.name, order.user.surname)
        if not result['success']:
            solar_obj.server_code = 100
            solar_obj.server_error = _('Error while user create')
            solar_obj.server_response = result
            solar_obj.save()
            return False

        response = self.make_request(
            'payment',
            action='payout',
            email=order.user.email,
            currency='RUB',
            amount=round(order.cashback_sum),
            task_title='Кешбек заказа',
            task_description=order.id,
            client_id=client_id,
            todo_type='2889',
            todo_attributes='Мороженое ЧЛ',
            merchant_transaction='ORDER%s' % order.id,
        )

        if response.get('success'):
            solar_obj.server_code = response['response']['status_id']
            solar_obj.server_response = response
            solar_obj.save()
            return True

        try:
            solar_obj.server_code = response['response']['status_id']
            try:
                solar_obj.server_error = response['response']['error_text']
            except:
                pass
            solar_obj.server_response = response
            solar_obj.save()
            return True
        except:
            solar_obj.server_code = 100
            try:
                solar_obj.server_error = response['response']['error_text']
            except:
                pass
            solar_obj.server_response = response
            solar_obj.save()
            return False
