from celery import shared_task


@shared_task(name='dump')
def dump():

    from application.dump.utils import dump

    dump()

    return 'OK'
