from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Calc ranks'

    def handle(self, *args, **options):

        print('Calc ranks ...')

        from application.survey.tasks import calc_ranks
        print(calc_ranks())
