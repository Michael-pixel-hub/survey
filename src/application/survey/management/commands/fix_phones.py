import re

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Fix phones'

    def handle(self, *args, **options):

        print('Fixing phones ...')

        from application.survey.models import User

        users = User.objects.all()
        for user in users:
            if user.phone is None or user.phone == '':
                continue
            phone = '+' + re.sub(r'\D', '', user.phone)
            phone = phone.replace('+8', '+7')
            if len(phone) == 11:
                phone = phone.replace('+', '+7')
            if not re.match(r'^\+7[\d]{10}$', phone):
                print(phone)
            else:
                user.phone = phone
                user.save()
        print('Done')
