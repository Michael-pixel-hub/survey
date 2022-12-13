import datetime
import psycopg2.extras

from celery import shared_task


@shared_task(name='archive_create_tables')
def archive_create_tables():

    year = datetime.datetime.now().year + 1

    conn = psycopg2.connect(dbname='shop_survey', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    for i in range(1, 13):

        date_start = datetime.datetime(year=year, month=i, day=1)
        date_start_s = date_start.strftime('%Y-%m-%d 00:00:00+00')
        if i == 12:
            date_end = datetime.datetime(year=year+1, month=1, day=1)
        else:
            date_end = datetime.datetime(year=year, month=i+1, day=1)
        date_end_s = date_end.strftime('%Y-%m-%d 00:00:00+00')

        m = f'{i}' if i >= 10 else f'0{i}'

        cursor.execute(f"""
create table archive_tasks_executions_y{year}_m{m}
    partition of archive_tasks_executions
        FOR VALUES FROM ('{date_start_s}') TO ('{date_end_s}');

alter table archive_tasks_executions_y{year}_m{m}
    owner to postgres;

create index archive_tasks_e_y{year}_m{m}_check_user_id_idx
    on archive_tasks_executions_y{year}_m{m} (check_user_id);

create index archive_tasks_e_y{year}_m{m}_store_id_idx
    on archive_tasks_executions_y{year}_m{m} (store_id);

create index archive_tasks_e_y{year}_m{m}_task_id_idx
    on archive_tasks_executions_y{year}_m{m} (task_id);

create index archive_tasks_e_y{year}_m{m}_user_id_idx
    on archive_tasks_executions_y{year}_m{m} (user_id);

create index archive_tasks_e_y{year}_m{m}_date_start_idx
    on archive_tasks_executions_y{year}_m{m} (date_start);
        """)

    conn.commit()

    return 'OK'
