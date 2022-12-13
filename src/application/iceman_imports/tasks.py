from celery import shared_task


@shared_task(name='iceman_import_stores')
def iceman_import_stores(file, file_name, user=None):

    from application.iceman_imports.utils import iceman_import_stores_from_file

    iceman_import_stores_from_file(file, file_name, user=user)

    return 'OK'


@shared_task(name='iceman_import_products')
def iceman_import_products(file, file_name, user=None):

    from application.iceman_imports.utils import iceman_import_products_from_file

    iceman_import_products_from_file(file, file_name, user=user)

    return 'OK'


@shared_task(name='iceman_import_tasks')
def iceman_import_tasks(file, file_name, user=None):

    from application.iceman_imports.utils import iceman_import_tasks_from_file

    iceman_import_tasks_from_file(file, file_name, user=user)

    return 'OK'
