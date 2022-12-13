import os

from application.agent.models import PromoCode
from django.conf import settings
from django.core.management.base import BaseCommand
from openpyxl import load_workbook


class Command(BaseCommand):

    help = 'Promo codes used'

    def handle(self, *args, **options):

        print('Promo codes used ...')

        wb = load_workbook(os.path.join(settings.DATA_DIR, 'promo_used.xlsx'))
        ws = wb.worksheets[0]

        stores = []

        for i in ws.rows:

            try:
                promo_obj = PromoCode.objects.get(code=i[0].value)
                store = promo_obj.store
                promo_obj.delete()
                if store:
                    stores.append(store)
            except PromoCode.DoesNotExist:
                pass

        for i in stores:
            promo_code = PromoCode.objects.filter(is_used=False).first()
            if promo_code:
                promo_code.is_used = True
                promo_code.store = i
                promo_code.save()
