from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Telegram spam to unregistered users'

    def handle(self, *args, **options):

        from application.dump.utils import dump
        dump()
