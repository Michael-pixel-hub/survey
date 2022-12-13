import requests

from django.conf import settings
from django.db import transaction
from preferences.utils import get_setting

from application.survey.models import TasksExecutionImage, TasksExecutionAssortment, Good

from .models import AIProject


class Ai:

    def __init__(self):
        self.url = get_setting('ai_url')
        self.token = get_setting('ai_token')

    def parse_constructor(self, inspector_obj):

        # Получаем приложение
        application = 'Неизвестно'
        for i in settings.APPLICATIONS:
            if i[0] == inspector_obj.task.application:
                application = i[1]
                break

        # Получаем проект распознавания
        project = None
        if inspector_obj.task is not None and inspector_obj.task.task is not None \
                and inspector_obj.task.task.ai_project is not None:
            project = inspector_obj.task.task.ai_project.name
        if project is None:
            ai_project = AIProject.objects.filter(is_default=True).first()
            if ai_project is not None:
                project = ai_project.name

        # Image uploads
        images = TasksExecutionImage.objects.filter(
            task=inspector_obj.task, constructor_step_name=inspector_obj.constructor_step_name)

        data = [('application', application)]
        if project is not None:
            data.append(('project', project))
        for image in images:
            data.append(('images', f'https://admin.shop-survey.ru/media/{image.image}'))

        if data:
            try:
                response = requests.post(
                    f'{self.url}reports/create/?api_key={self.token}',
                    data=data
                )
                report_id = response.json()['id']
                inspector_obj.inspector_upload_images_text = response.text
                inspector_obj.inspector_status = 'report_wait'
                inspector_obj.inspector_report_id = report_id
                inspector_obj.save(update_fields=['inspector_status', 'inspector_report_id', 'inspector_upload_images_text'])
                transaction.commit()
            except:
                pass
        else:
            raise Exception('Нет изображений')

    def report_constructor(self, inspector_obj):

        response = requests.get(f'{self.url}reports/{inspector_obj.inspector_report_id}/?api_key={self.token}')

        data = response.json()

        inspector_obj.inspector_report_text = response.text
        inspector_obj.save(update_fields=['inspector_report_text'])
        transaction.commit()

        if data['status'] == 'error':
            inspector_obj.inspector_status = 'error'
            inspector_obj.save(update_fields=['inspector_positions_text', 'inspector_status'])
            inspector_obj.task.inspector_status = 'error'
            inspector_obj.task.save(update_fields=['inspector_status'])
            transaction.commit()
            return

        if data['status'] != 'complete':
            inspector_obj.inspector_status = 'report_wait'
            inspector_obj.save(update_fields=['inspector_status'])
            transaction.commit()
            return

        inspector_obj.inspector_positions_text = ''

        for product in data['products']:
            inspector_obj.inspector_positions_text += f"{product['product_name']} - {product['product_code']} - " \
                                                      f"{product['faces_count']}\r\n"
            good = Good.objects.filter(code=product['product_code']).first()

            if good is not None:
                try:
                    tea = TasksExecutionAssortment.objects.get(good=good, task=inspector_obj.task, constructor_step_name=inspector_obj.constructor_step_name)
                except:
                    tea = TasksExecutionAssortment(good=good, task=inspector_obj.task, constructor_step_name=inspector_obj.constructor_step_name)
                tea.avail = round(product['faces_count'], 2)
                tea.save()

        inspector_obj.inspector_status = 'success'
        inspector_obj.save(update_fields=['inspector_positions_text', 'inspector_status'])
        inspector_obj.task.inspector_status = 'success'
        inspector_obj.task.save(update_fields=['inspector_status'])
        transaction.commit()

    def problem(self, report_id, goods):

        data = [('report_id', report_id)]
        for good in goods:
            if good is not None:
                data.append(('products', good))

        try:
            requests.post(
                f'{self.url}reports/problem/create/?api_key={self.token}',
                data=data
            )
        except:
            pass
