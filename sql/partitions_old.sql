create table archive_tasks_executions_y2018_m09
    partition of archive_tasks_executions
        FOR VALUES FROM ('2018-09-01 00:00:00+00') TO ('2018-10-01 00:00:00+00');

alter table archive_tasks_executions_y2018_m09
    owner to postgres;

create index archive_tasks_executions_y2018_m09_check_user_id_idx
    on archive_tasks_executions_y2018_m09 (check_user_id);

create index archive_tasks_executions_y2018_m09_store_id_idx
    on archive_tasks_executions_y2018_m09 (store_id);

create index archive_tasks_executions_y2018_m09_task_id_idx
    on archive_tasks_executions_y2018_m09 (task_id);

create index archive_tasks_executions_y2018_m09_user_id_idx
    on archive_tasks_executions_y2018_m09 (user_id);

create index archive_tasks_executions_y2018_m09_date_start_idx
    on archive_tasks_executions_y2018_m09 (date_start);

create table archive_tasks_executions_y2018_m10
    partition of archive_tasks_executions
        FOR VALUES FROM ('2018-10-01 00:00:00+00') TO ('2018-11-01 00:00:00+00');

alter table archive_tasks_executions_y2018_m10
    owner to postgres;

create index archive_tasks_executions_y2018_m10_check_user_id_idx
    on archive_tasks_executions_y2018_m10 (check_user_id);

create index archive_tasks_executions_y2018_m10_store_id_idx
    on archive_tasks_executions_y2018_m10 (store_id);

create index archive_tasks_executions_y2018_m10_task_id_idx
    on archive_tasks_executions_y2018_m10 (task_id);

create index archive_tasks_executions_y2018_m10_user_id_idx
    on archive_tasks_executions_y2018_m10 (user_id);

create index archive_tasks_executions_y2018_m10_date_start_idx
    on archive_tasks_executions_y2018_m10 (date_start);

create table archive_tasks_executions_y2018_m11
    partition of archive_tasks_executions
        FOR VALUES FROM ('2018-11-01 00:00:00+00') TO ('2018-12-01 00:00:00+00');

alter table archive_tasks_executions_y2018_m11
    owner to postgres;

create index archive_tasks_executions_y2018_m11_check_user_id_idx
    on archive_tasks_executions_y2018_m11 (check_user_id);

create index archive_tasks_executions_y2018_m11_store_id_idx
    on archive_tasks_executions_y2018_m11 (store_id);

create index archive_tasks_executions_y2018_m11_task_id_idx
    on archive_tasks_executions_y2018_m11 (task_id);

create index archive_tasks_executions_y2018_m11_user_id_idx
    on archive_tasks_executions_y2018_m11 (user_id);

create index archive_tasks_executions_y2018_m11_date_start_idx
    on archive_tasks_executions_y2018_m11 (date_start);

create table archive_tasks_executions_y2018_m12
    partition of archive_tasks_executions
        FOR VALUES FROM ('2018-12-01 00:00:00+00') TO ('2019-01-01 00:00:00+00');

alter table archive_tasks_executions_y2018_m12
    owner to postgres;

create index archive_tasks_executions_y2018_m12_check_user_id_idx
    on archive_tasks_executions_y2018_m12 (check_user_id);

create index archive_tasks_executions_y2018_m12_store_id_idx
    on archive_tasks_executions_y2018_m12 (store_id);

create index archive_tasks_executions_y2018_m12_task_id_idx
    on archive_tasks_executions_y2018_m12 (task_id);

create index archive_tasks_executions_y2018_m12_user_id_idx
    on archive_tasks_executions_y2018_m12 (user_id);

create index archive_tasks_executions_y2018_m12_date_start_idx
    on archive_tasks_executions_y2018_m12 (date_start);

create table archive_tasks_executions_y2019_m01
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-01-01 00:00:00+00') TO ('2019-02-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m01
    owner to postgres;

create index archive_tasks_executions_y2019_m01_check_user_id_idx
    on archive_tasks_executions_y2019_m01 (check_user_id);

create index archive_tasks_executions_y2019_m01_store_id_idx
    on archive_tasks_executions_y2019_m01 (store_id);

create index archive_tasks_executions_y2019_m01_task_id_idx
    on archive_tasks_executions_y2019_m01 (task_id);

create index archive_tasks_executions_y2019_m01_user_id_idx
    on archive_tasks_executions_y2019_m01 (user_id);

create index archive_tasks_executions_y2019_m01_date_start_idx
    on archive_tasks_executions_y2019_m01 (date_start);

create table archive_tasks_executions_y2019_m02
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-02-01 00:00:00+00') TO ('2019-03-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m02
    owner to postgres;

create index archive_tasks_executions_y2019_m02_check_user_id_idx
    on archive_tasks_executions_y2019_m02 (check_user_id);

create index archive_tasks_executions_y2019_m02_store_id_idx
    on archive_tasks_executions_y2019_m02 (store_id);

create index archive_tasks_executions_y2019_m02_task_id_idx
    on archive_tasks_executions_y2019_m02 (task_id);

create index archive_tasks_executions_y2019_m02_user_id_idx
    on archive_tasks_executions_y2019_m02 (user_id);

create index archive_tasks_executions_y2019_m02_date_start_idx
    on archive_tasks_executions_y2019_m02 (date_start);

create table archive_tasks_executions_y2019_m03
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-03-01 00:00:00+00') TO ('2019-04-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m03
    owner to postgres;

create index archive_tasks_executions_y2019_m03_check_user_id_idx
    on archive_tasks_executions_y2019_m03 (check_user_id);

create index archive_tasks_executions_y2019_m03_store_id_idx
    on archive_tasks_executions_y2019_m03 (store_id);

create index archive_tasks_executions_y2019_m03_task_id_idx
    on archive_tasks_executions_y2019_m03 (task_id);

create index archive_tasks_executions_y2019_m03_user_id_idx
    on archive_tasks_executions_y2019_m03 (user_id);

create index archive_tasks_executions_y2019_m03_date_start_idx
    on archive_tasks_executions_y2019_m03 (date_start);

create table archive_tasks_executions_y2019_m04
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-04-01 00:00:00+00') TO ('2019-05-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m04
    owner to postgres;

create index archive_tasks_executions_y2019_m04_check_user_id_idx
    on archive_tasks_executions_y2019_m04 (check_user_id);

create index archive_tasks_executions_y2019_m04_store_id_idx
    on archive_tasks_executions_y2019_m04 (store_id);

create index archive_tasks_executions_y2019_m04_task_id_idx
    on archive_tasks_executions_y2019_m04 (task_id);

create index archive_tasks_executions_y2019_m04_user_id_idx
    on archive_tasks_executions_y2019_m04 (user_id);

create index archive_tasks_executions_y2019_m04_date_start_idx
    on archive_tasks_executions_y2019_m04 (date_start);

create table archive_tasks_executions_y2019_m05
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-05-01 00:00:00+00') TO ('2019-06-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m05
    owner to postgres;

create index archive_tasks_executions_y2019_m05_check_user_id_idx
    on archive_tasks_executions_y2019_m05 (check_user_id);

create index archive_tasks_executions_y2019_m05_store_id_idx
    on archive_tasks_executions_y2019_m05 (store_id);

create index archive_tasks_executions_y2019_m05_task_id_idx
    on archive_tasks_executions_y2019_m05 (task_id);

create index archive_tasks_executions_y2019_m05_user_id_idx
    on archive_tasks_executions_y2019_m05 (user_id);

create index archive_tasks_executions_y2019_m05_date_start_idx
    on archive_tasks_executions_y2019_m05 (date_start);

create table archive_tasks_executions_y2019_m06
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-06-01 00:00:00+00') TO ('2019-07-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m06
    owner to postgres;

create index archive_tasks_executions_y2019_m06_check_user_id_idx
    on archive_tasks_executions_y2019_m06 (check_user_id);

create index archive_tasks_executions_y2019_m06_store_id_idx
    on archive_tasks_executions_y2019_m06 (store_id);

create index archive_tasks_executions_y2019_m06_task_id_idx
    on archive_tasks_executions_y2019_m06 (task_id);

create index archive_tasks_executions_y2019_m06_user_id_idx
    on archive_tasks_executions_y2019_m06 (user_id);

create index archive_tasks_executions_y2019_m06_date_start_idx
    on archive_tasks_executions_y2019_m06 (date_start);

create table archive_tasks_executions_y2019_m07
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-07-01 00:00:00+00') TO ('2019-08-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m07
    owner to postgres;

create index archive_tasks_executions_y2019_m07_check_user_id_idx
    on archive_tasks_executions_y2019_m07 (check_user_id);

create index archive_tasks_executions_y2019_m07_store_id_idx
    on archive_tasks_executions_y2019_m07 (store_id);

create index archive_tasks_executions_y2019_m07_task_id_idx
    on archive_tasks_executions_y2019_m07 (task_id);

create index archive_tasks_executions_y2019_m07_user_id_idx
    on archive_tasks_executions_y2019_m07 (user_id);

create index archive_tasks_executions_y2019_m07_date_start_idx
    on archive_tasks_executions_y2019_m07 (date_start);

create table archive_tasks_executions_y2019_m08
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-08-01 00:00:00+00') TO ('2019-09-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m08
    owner to postgres;

create index archive_tasks_executions_y2019_m08_check_user_id_idx
    on archive_tasks_executions_y2019_m08 (check_user_id);

create index archive_tasks_executions_y2019_m08_store_id_idx
    on archive_tasks_executions_y2019_m08 (store_id);

create index archive_tasks_executions_y2019_m08_task_id_idx
    on archive_tasks_executions_y2019_m08 (task_id);

create index archive_tasks_executions_y2019_m08_user_id_idx
    on archive_tasks_executions_y2019_m08 (user_id);

create index archive_tasks_executions_y2019_m08_date_start_idx
    on archive_tasks_executions_y2019_m08 (date_start);

create table archive_tasks_executions_y2019_m09
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-09-01 00:00:00+00') TO ('2019-10-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m09
    owner to postgres;

create index archive_tasks_executions_y2019_m09_check_user_id_idx
    on archive_tasks_executions_y2019_m09 (check_user_id);

create index archive_tasks_executions_y2019_m09_store_id_idx
    on archive_tasks_executions_y2019_m09 (store_id);

create index archive_tasks_executions_y2019_m09_task_id_idx
    on archive_tasks_executions_y2019_m09 (task_id);

create index archive_tasks_executions_y2019_m09_user_id_idx
    on archive_tasks_executions_y2019_m09 (user_id);

create index archive_tasks_executions_y2019_m09_date_start_idx
    on archive_tasks_executions_y2019_m09 (date_start);

create table archive_tasks_executions_y2019_m10
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-10-01 00:00:00+00') TO ('2019-11-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m10
    owner to postgres;

create index archive_tasks_executions_y2019_m10_check_user_id_idx
    on archive_tasks_executions_y2019_m10 (check_user_id);

create index archive_tasks_executions_y2019_m10_store_id_idx
    on archive_tasks_executions_y2019_m10 (store_id);

create index archive_tasks_executions_y2019_m10_task_id_idx
    on archive_tasks_executions_y2019_m10 (task_id);

create index archive_tasks_executions_y2019_m10_user_id_idx
    on archive_tasks_executions_y2019_m10 (user_id);

create index archive_tasks_executions_y2019_m10_date_start_idx
    on archive_tasks_executions_y2019_m10 (date_start);

create table archive_tasks_executions_y2019_m11
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-11-01 00:00:00+00') TO ('2019-12-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m11
    owner to postgres;

create index archive_tasks_executions_y2019_m11_check_user_id_idx
    on archive_tasks_executions_y2019_m11 (check_user_id);

create index archive_tasks_executions_y2019_m11_store_id_idx
    on archive_tasks_executions_y2019_m11 (store_id);

create index archive_tasks_executions_y2019_m11_task_id_idx
    on archive_tasks_executions_y2019_m11 (task_id);

create index archive_tasks_executions_y2019_m11_user_id_idx
    on archive_tasks_executions_y2019_m11 (user_id);

create index archive_tasks_executions_y2019_m11_date_start_idx
    on archive_tasks_executions_y2019_m11 (date_start);

create table archive_tasks_executions_y2019_m12
    partition of archive_tasks_executions
        FOR VALUES FROM ('2019-12-01 00:00:00+00') TO ('2020-01-01 00:00:00+00');

alter table archive_tasks_executions_y2019_m12
    owner to postgres;

create index archive_tasks_executions_y2019_m12_check_user_id_idx
    on archive_tasks_executions_y2019_m12 (check_user_id);

create index archive_tasks_executions_y2019_m12_store_id_idx
    on archive_tasks_executions_y2019_m12 (store_id);

create index archive_tasks_executions_y2019_m12_task_id_idx
    on archive_tasks_executions_y2019_m12 (task_id);

create index archive_tasks_executions_y2019_m12_user_id_idx
    on archive_tasks_executions_y2019_m12 (user_id);

create index archive_tasks_executions_y2019_m12_date_start_idx
    on archive_tasks_executions_y2019_m12 (date_start);
