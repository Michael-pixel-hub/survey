from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):

    help = 'Fill api keys'

    def handle(self, *args, **options):

        print('Fill api keys ...')

        from application.survey.models import User, gen_key

        users = User.objects.filter(Q(api_key__isnull=True) | Q(api_key=''))
        for user in users:
            user.api_key = gen_key()
            user.save()
