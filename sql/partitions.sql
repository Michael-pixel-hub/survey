create sequence if not exists public.archive_tasks_executions_id_seq
    as integer;

alter sequence public.archive_tasks_executions_id_seq owner to postgres;

create table archive_tasks_executions
(
    id                           integer default nextval('archive_tasks_executions_id_seq'::regclass) not null,
    money                        double precision                                                     not null,
    money_source                 double precision                                                     not null,
    date_start                   timestamp without time zone                                          not null,
    date_end                     timestamp without time zone,
    date_end_user                timestamp without time zone,
    status                       integer                                                              not null,
    image                        varchar(100),
    comments                     text                                                                 not null,
    comments_status              text,
    comments_internal            text,
    longitude                    double precision,
    latitude                     double precision,
    distance                     double precision,
    step                         varchar(10)                                                          not null,
    check_type                   varchar(12)                                                          not null,
    "check"                      varchar(12)                                                          not null,
    set_check_verified           boolean                                                              not null,
    set_check_not_verified       boolean                                                              not null,
    is_auditor                   boolean                                                              not null,
    inspector_upload_images_text text                                                                 not null,
    inspector_error              text,
    inspector_recognize_text     text,
    inspector_report_text        text,
    inspector_positions_text     text,
    inspector_status             varchar(20)                                                          not null,
    inspector_report_id          integer,
    inspector_report_id_before   integer,
    inspector_status_before      varchar(20)                                                          not null,
    inspector_is_alert           boolean                                                              not null,
    inspector_re_work            boolean                                                              not null,
    inspector_is_work            boolean                                                              not null,
    telegram_channel_status      integer                                                              not null,
    source                       varchar(20)                                                          not null,
    check_user_id                integer
        constraint archive_tasks_executions_check_user_id_26560e77_fk_auth_user_id
            references auth_user
            deferrable initially deferred,
    store_id                     integer
        constraint archive_tasks_executions_store_id_fc6ceb77_fk_chl_stores_id
            references chl_stores
            deferrable initially deferred,
    task_id                      integer
        constraint archive_tasks_executions_task_id_eae7fb54_fk_chl_tasks_id
            references chl_tasks
            deferrable initially deferred,
    user_id                      integer                                                              not null
        constraint archive_tasks_executions_user_id_d4bcf77c_fk_telegram_users_id
            references telegram_users
            deferrable initially deferred,
    constraint archive_tasks_executions_pkey
        primary key (id, date_start)
)
    partition by RANGE (date_start);

alter table archive_tasks_executions
    owner to postgres;

create table archive_tasks_executions_y2021_m01
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-01-01 00:00:00+00') TO ('2021-02-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m01
    owner to postgres;

create index archive_tasks_executions_y2021_m01_check_user_id_idx
    on archive_tasks_executions_y2021_m01 (check_user_id);

create index archive_tasks_executions_y2021_m01_store_id_idx
    on archive_tasks_executions_y2021_m01 (store_id);

create index archive_tasks_executions_y2021_m01_task_id_idx
    on archive_tasks_executions_y2021_m01 (task_id);

create index archive_tasks_executions_y2021_m01_user_id_idx
    on archive_tasks_executions_y2021_m01 (user_id);

create index archive_tasks_executions_y2021_m01_date_start_idx
    on archive_tasks_executions_y2021_m01 (date_start);

create table archive_tasks_executions_y2021_m02
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-02-01 00:00:00+00') TO ('2021-03-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m02
    owner to postgres;

create index archive_tasks_executions_y2021_m02_check_user_id_idx
    on archive_tasks_executions_y2021_m02 (check_user_id);

create index archive_tasks_executions_y2021_m02_store_id_idx
    on archive_tasks_executions_y2021_m02 (store_id);

create index archive_tasks_executions_y2021_m02_task_id_idx
    on archive_tasks_executions_y2021_m02 (task_id);

create index archive_tasks_executions_y2021_m02_user_id_idx
    on archive_tasks_executions_y2021_m02 (user_id);

create index archive_tasks_executions_y2021_m02_date_start_idx
    on archive_tasks_executions_y2021_m02 (date_start);

create table archive_tasks_executions_y2021_m03
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-03-01 00:00:00+00') TO ('2021-04-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m03
    owner to postgres;

create index archive_tasks_executions_y2021_m03_check_user_id_idx
    on archive_tasks_executions_y2021_m03 (check_user_id);

create index archive_tasks_executions_y2021_m03_store_id_idx
    on archive_tasks_executions_y2021_m03 (store_id);

create index archive_tasks_executions_y2021_m03_task_id_idx
    on archive_tasks_executions_y2021_m03 (task_id);

create index archive_tasks_executions_y2021_m03_user_id_idx
    on archive_tasks_executions_y2021_m03 (user_id);

create index archive_tasks_executions_y2021_m03_date_start_idx
    on archive_tasks_executions_y2021_m03 (date_start);

create table archive_tasks_executions_y2021_m04
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-04-01 00:00:00+00') TO ('2021-05-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m04
    owner to postgres;

create index archive_tasks_executions_y2021_m04_check_user_id_idx
    on archive_tasks_executions_y2021_m04 (check_user_id);

create index archive_tasks_executions_y2021_m04_store_id_idx
    on archive_tasks_executions_y2021_m04 (store_id);

create index archive_tasks_executions_y2021_m04_task_id_idx
    on archive_tasks_executions_y2021_m04 (task_id);

create index archive_tasks_executions_y2021_m04_user_id_idx
    on archive_tasks_executions_y2021_m04 (user_id);

create index archive_tasks_executions_y2021_m04_date_start_idx
    on archive_tasks_executions_y2021_m04 (date_start);

create table archive_tasks_executions_y2021_m05
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-05-01 00:00:00+00') TO ('2021-06-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m05
    owner to postgres;

create index archive_tasks_executions_y2021_m05_check_user_id_idx
    on archive_tasks_executions_y2021_m05 (check_user_id);

create index archive_tasks_executions_y2021_m05_store_id_idx
    on archive_tasks_executions_y2021_m05 (store_id);

create index archive_tasks_executions_y2021_m05_task_id_idx
    on archive_tasks_executions_y2021_m05 (task_id);

create index archive_tasks_executions_y2021_m05_user_id_idx
    on archive_tasks_executions_y2021_m05 (user_id);

create index archive_tasks_executions_y2021_m05_date_start_idx
    on archive_tasks_executions_y2021_m05 (date_start);

create table archive_tasks_executions_y2021_m06
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-06-01 00:00:00+00') TO ('2021-07-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m06
    owner to postgres;

create index archive_tasks_executions_y2021_m06_check_user_id_idx
    on archive_tasks_executions_y2021_m06 (check_user_id);

create index archive_tasks_executions_y2021_m06_store_id_idx
    on archive_tasks_executions_y2021_m06 (store_id);

create index archive_tasks_executions_y2021_m06_task_id_idx
    on archive_tasks_executions_y2021_m06 (task_id);

create index archive_tasks_executions_y2021_m06_user_id_idx
    on archive_tasks_executions_y2021_m06 (user_id);

create index archive_tasks_executions_y2021_m06_date_start_idx
    on archive_tasks_executions_y2021_m06 (date_start);

create table archive_tasks_executions_y2021_m07
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-07-01 00:00:00+00') TO ('2021-08-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m07
    owner to postgres;

create index archive_tasks_executions_y2021_m07_check_user_id_idx
    on archive_tasks_executions_y2021_m07 (check_user_id);

create index archive_tasks_executions_y2021_m07_store_id_idx
    on archive_tasks_executions_y2021_m07 (store_id);

create index archive_tasks_executions_y2021_m07_task_id_idx
    on archive_tasks_executions_y2021_m07 (task_id);

create index archive_tasks_executions_y2021_m07_user_id_idx
    on archive_tasks_executions_y2021_m07 (user_id);

create index archive_tasks_executions_y2021_m07_date_start_idx
    on archive_tasks_executions_y2021_m07 (date_start);

create table archive_tasks_executions_y2021_m08
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-08-01 00:00:00+00') TO ('2021-09-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m08
    owner to postgres;

create index archive_tasks_executions_y2021_m08_check_user_id_idx
    on archive_tasks_executions_y2021_m08 (check_user_id);

create index archive_tasks_executions_y2021_m08_store_id_idx
    on archive_tasks_executions_y2021_m08 (store_id);

create index archive_tasks_executions_y2021_m08_task_id_idx
    on archive_tasks_executions_y2021_m08 (task_id);

create index archive_tasks_executions_y2021_m08_user_id_idx
    on archive_tasks_executions_y2021_m08 (user_id);

create index archive_tasks_executions_y2021_m08_date_start_idx
    on archive_tasks_executions_y2021_m08 (date_start);

create table archive_tasks_executions_y2021_m09
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-09-01 00:00:00+00') TO ('2021-10-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m09
    owner to postgres;

create index archive_tasks_executions_y2021_m09_check_user_id_idx
    on archive_tasks_executions_y2021_m09 (check_user_id);

create index archive_tasks_executions_y2021_m09_store_id_idx
    on archive_tasks_executions_y2021_m09 (store_id);

create index archive_tasks_executions_y2021_m09_task_id_idx
    on archive_tasks_executions_y2021_m09 (task_id);

create index archive_tasks_executions_y2021_m09_user_id_idx
    on archive_tasks_executions_y2021_m09 (user_id);

create index archive_tasks_executions_y2021_m09_date_start_idx
    on archive_tasks_executions_y2021_m09 (date_start);

create table archive_tasks_executions_y2021_m10
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-10-01 00:00:00+00') TO ('2021-11-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m10
    owner to postgres;

create index archive_tasks_executions_y2021_m10_check_user_id_idx
    on archive_tasks_executions_y2021_m10 (check_user_id);

create index archive_tasks_executions_y2021_m10_store_id_idx
    on archive_tasks_executions_y2021_m10 (store_id);

create index archive_tasks_executions_y2021_m10_task_id_idx
    on archive_tasks_executions_y2021_m10 (task_id);

create index archive_tasks_executions_y2021_m10_user_id_idx
    on archive_tasks_executions_y2021_m10 (user_id);

create index archive_tasks_executions_y2021_m10_date_start_idx
    on archive_tasks_executions_y2021_m10 (date_start);

create table archive_tasks_executions_y2021_m11
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-11-01 00:00:00+00') TO ('2021-12-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m11
    owner to postgres;

create index archive_tasks_executions_y2021_m11_check_user_id_idx
    on archive_tasks_executions_y2021_m11 (check_user_id);

create index archive_tasks_executions_y2021_m11_store_id_idx
    on archive_tasks_executions_y2021_m11 (store_id);

create index archive_tasks_executions_y2021_m11_task_id_idx
    on archive_tasks_executions_y2021_m11 (task_id);

create index archive_tasks_executions_y2021_m11_user_id_idx
    on archive_tasks_executions_y2021_m11 (user_id);

create index archive_tasks_executions_y2021_m11_date_start_idx
    on archive_tasks_executions_y2021_m11 (date_start);

create table archive_tasks_executions_y2021_m12
    partition of archive_tasks_executions
        FOR VALUES FROM ('2021-12-01 00:00:00+00') TO ('2022-01-01 00:00:00+00');

alter table archive_tasks_executions_y2021_m12
    owner to postgres;

create index archive_tasks_executions_y2021_m12_check_user_id_idx
    on archive_tasks_executions_y2021_m12 (check_user_id);

create index archive_tasks_executions_y2021_m12_store_id_idx
    on archive_tasks_executions_y2021_m12 (store_id);

create index archive_tasks_executions_y2021_m12_task_id_idx
    on archive_tasks_executions_y2021_m12 (task_id);

create index archive_tasks_executions_y2021_m12_user_id_idx
    on archive_tasks_executions_y2021_m12 (user_id);

create index archive_tasks_executions_y2021_m12_date_start_idx
    on archive_tasks_executions_y2021_m12 (date_start);

create table archive_tasks_executions_y2020_m01
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-01-01 00:00:00+00') TO ('2020-02-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m01
    owner to postgres;

create index archive_tasks_executions_y2020_m01_check_user_id_idx
    on archive_tasks_executions_y2020_m01 (check_user_id);

create index archive_tasks_executions_y2020_m01_store_id_idx
    on archive_tasks_executions_y2020_m01 (store_id);

create index archive_tasks_executions_y2020_m01_task_id_idx
    on archive_tasks_executions_y2020_m01 (task_id);

create index archive_tasks_executions_y2020_m01_user_id_idx
    on archive_tasks_executions_y2020_m01 (user_id);

create index archive_tasks_executions_y2020_m01_date_start_idx
    on archive_tasks_executions_y2020_m01 (date_start);

create table archive_tasks_executions_y2020_m02
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-02-01 00:00:00+00') TO ('2020-03-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m02
    owner to postgres;

create index archive_tasks_executions_y2020_m02_check_user_id_idx
    on archive_tasks_executions_y2020_m02 (check_user_id);

create index archive_tasks_executions_y2020_m02_store_id_idx
    on archive_tasks_executions_y2020_m02 (store_id);

create index archive_tasks_executions_y2020_m02_task_id_idx
    on archive_tasks_executions_y2020_m02 (task_id);

create index archive_tasks_executions_y2020_m02_user_id_idx
    on archive_tasks_executions_y2020_m02 (user_id);

create index archive_tasks_executions_y2020_m02_date_start_idx
    on archive_tasks_executions_y2020_m02 (date_start);

create table archive_tasks_executions_y2020_m03
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-03-01 00:00:00+00') TO ('2020-04-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m03
    owner to postgres;

create index archive_tasks_executions_y2020_m03_check_user_id_idx
    on archive_tasks_executions_y2020_m03 (check_user_id);

create index archive_tasks_executions_y2020_m03_store_id_idx
    on archive_tasks_executions_y2020_m03 (store_id);

create index archive_tasks_executions_y2020_m03_task_id_idx
    on archive_tasks_executions_y2020_m03 (task_id);

create index archive_tasks_executions_y2020_m03_user_id_idx
    on archive_tasks_executions_y2020_m03 (user_id);

create index archive_tasks_executions_y2020_m03_date_start_idx
    on archive_tasks_executions_y2020_m03 (date_start);

create table archive_tasks_executions_y2020_m04
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-04-01 00:00:00+00') TO ('2020-05-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m04
    owner to postgres;

create index archive_tasks_executions_y2020_m04_check_user_id_idx
    on archive_tasks_executions_y2020_m04 (check_user_id);

create index archive_tasks_executions_y2020_m04_store_id_idx
    on archive_tasks_executions_y2020_m04 (store_id);

create index archive_tasks_executions_y2020_m04_task_id_idx
    on archive_tasks_executions_y2020_m04 (task_id);

create index archive_tasks_executions_y2020_m04_user_id_idx
    on archive_tasks_executions_y2020_m04 (user_id);

create index archive_tasks_executions_y2020_m04_date_start_idx
    on archive_tasks_executions_y2020_m04 (date_start);

create table archive_tasks_executions_y2020_m05
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-05-01 00:00:00+00') TO ('2020-06-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m05
    owner to postgres;

create index archive_tasks_executions_y2020_m05_check_user_id_idx
    on archive_tasks_executions_y2020_m05 (check_user_id);

create index archive_tasks_executions_y2020_m05_store_id_idx
    on archive_tasks_executions_y2020_m05 (store_id);

create index archive_tasks_executions_y2020_m05_task_id_idx
    on archive_tasks_executions_y2020_m05 (task_id);

create index archive_tasks_executions_y2020_m05_user_id_idx
    on archive_tasks_executions_y2020_m05 (user_id);

create index archive_tasks_executions_y2020_m05_date_start_idx
    on archive_tasks_executions_y2020_m05 (date_start);

create table archive_tasks_executions_y2020_m06
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-06-01 00:00:00+00') TO ('2020-07-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m06
    owner to postgres;

create index archive_tasks_executions_y2020_m06_check_user_id_idx
    on archive_tasks_executions_y2020_m06 (check_user_id);

create index archive_tasks_executions_y2020_m06_store_id_idx
    on archive_tasks_executions_y2020_m06 (store_id);

create index archive_tasks_executions_y2020_m06_task_id_idx
    on archive_tasks_executions_y2020_m06 (task_id);

create index archive_tasks_executions_y2020_m06_user_id_idx
    on archive_tasks_executions_y2020_m06 (user_id);

create index archive_tasks_executions_y2020_m06_date_start_idx
    on archive_tasks_executions_y2020_m06 (date_start);

create table archive_tasks_executions_y2020_m07
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-07-01 00:00:00+00') TO ('2020-08-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m07
    owner to postgres;

create index archive_tasks_executions_y2020_m07_check_user_id_idx
    on archive_tasks_executions_y2020_m07 (check_user_id);

create index archive_tasks_executions_y2020_m07_store_id_idx
    on archive_tasks_executions_y2020_m07 (store_id);

create index archive_tasks_executions_y2020_m07_task_id_idx
    on archive_tasks_executions_y2020_m07 (task_id);

create index archive_tasks_executions_y2020_m07_user_id_idx
    on archive_tasks_executions_y2020_m07 (user_id);

create index archive_tasks_executions_y2020_m07_date_start_idx
    on archive_tasks_executions_y2020_m07 (date_start);

create table archive_tasks_executions_y2020_m08
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-08-01 00:00:00+00') TO ('2020-09-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m08
    owner to postgres;

create index archive_tasks_executions_y2020_m08_check_user_id_idx
    on archive_tasks_executions_y2020_m08 (check_user_id);

create index archive_tasks_executions_y2020_m08_store_id_idx
    on archive_tasks_executions_y2020_m08 (store_id);

create index archive_tasks_executions_y2020_m08_task_id_idx
    on archive_tasks_executions_y2020_m08 (task_id);

create index archive_tasks_executions_y2020_m08_user_id_idx
    on archive_tasks_executions_y2020_m08 (user_id);

create index archive_tasks_executions_y2020_m08_date_start_idx
    on archive_tasks_executions_y2020_m08 (date_start);

create table archive_tasks_executions_y2020_m09
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-09-01 00:00:00+00') TO ('2020-10-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m09
    owner to postgres;

create index archive_tasks_executions_y2020_m09_check_user_id_idx
    on archive_tasks_executions_y2020_m09 (check_user_id);

create index archive_tasks_executions_y2020_m09_store_id_idx
    on archive_tasks_executions_y2020_m09 (store_id);

create index archive_tasks_executions_y2020_m09_task_id_idx
    on archive_tasks_executions_y2020_m09 (task_id);

create index archive_tasks_executions_y2020_m09_user_id_idx
    on archive_tasks_executions_y2020_m09 (user_id);

create index archive_tasks_executions_y2020_m09_date_start_idx
    on archive_tasks_executions_y2020_m09 (date_start);

create table archive_tasks_executions_y2020_m10
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-10-01 00:00:00+00') TO ('2020-11-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m10
    owner to postgres;

create index archive_tasks_executions_y2020_m10_check_user_id_idx
    on archive_tasks_executions_y2020_m10 (check_user_id);

create index archive_tasks_executions_y2020_m10_store_id_idx
    on archive_tasks_executions_y2020_m10 (store_id);

create index archive_tasks_executions_y2020_m10_task_id_idx
    on archive_tasks_executions_y2020_m10 (task_id);

create index archive_tasks_executions_y2020_m10_user_id_idx
    on archive_tasks_executions_y2020_m10 (user_id);

create index archive_tasks_executions_y2020_m10_date_start_idx
    on archive_tasks_executions_y2020_m10 (date_start);

create table archive_tasks_executions_y2020_m11
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-11-01 00:00:00+00') TO ('2020-12-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m11
    owner to postgres;

create index archive_tasks_executions_y2020_m11_check_user_id_idx
    on archive_tasks_executions_y2020_m11 (check_user_id);

create index archive_tasks_executions_y2020_m11_store_id_idx
    on archive_tasks_executions_y2020_m11 (store_id);

create index archive_tasks_executions_y2020_m11_task_id_idx
    on archive_tasks_executions_y2020_m11 (task_id);

create index archive_tasks_executions_y2020_m11_user_id_idx
    on archive_tasks_executions_y2020_m11 (user_id);

create index archive_tasks_executions_y2020_m11_date_start_idx
    on archive_tasks_executions_y2020_m11 (date_start);

create table archive_tasks_executions_y2020_m12
    partition of archive_tasks_executions
        FOR VALUES FROM ('2020-12-01 00:00:00+00') TO ('2021-01-01 00:00:00+00');

alter table archive_tasks_executions_y2020_m12
    owner to postgres;

create index archive_tasks_executions_y2020_m12_check_user_id_idx
    on archive_tasks_executions_y2020_m12 (check_user_id);

create index archive_tasks_executions_y2020_m12_store_id_idx
    on archive_tasks_executions_y2020_m12 (store_id);

create index archive_tasks_executions_y2020_m12_task_id_idx
    on archive_tasks_executions_y2020_m12 (task_id);

create index archive_tasks_executions_y2020_m12_user_id_idx
    on archive_tasks_executions_y2020_m12 (user_id);

create index archive_tasks_executions_y2020_m12_date_start_idx
    on archive_tasks_executions_y2020_m12 (date_start);

-- Images
create table public.archive_tasks_executions_images
(
    id serial not null constraint archive_tasks_executions_images_pkey primary key,
    image       varchar(100),
    status      varchar(1000) not null,
    md5         varchar(32),
    type        varchar(10)   not null,
    telegram_id varchar(200),
    task_id     integer not null,
    date_start  timestamp without time zone not null,
    FOREIGN KEY ("task_id", "date_start") REFERENCES archive_tasks_executions ("id", "date_start")
);

alter table public.archive_tasks_executions_images
    owner to postgres;

create index archive_tasks_executions_images_task_id_01934471
    on public.archive_tasks_executions_images (task_id);

-- Assortment before
create table public.archive_tasks_executions_assortment_before
(
    id serial not null constraint archive_tasks_executions_assortment_before_pkey primary key,
    avail   double precision not null,
    good_id integer
        constraint archive_tasks_executions_good_id_c77b50fe_fk_chl_goods
            references public.chl_goods
            deferrable initially deferred,
    task_id     integer not null,
    date_start  timestamp without time zone not null,
    FOREIGN KEY ("task_id", "date_start") REFERENCES archive_tasks_executions ("id", "date_start")
);

alter table public.archive_tasks_executions_assortment_before
    owner to postgres;

create index archive_tasks_executions_assortment_before_good_id_c77b50fe
    on public.archive_tasks_executions_assortment_before (good_id);

create index archive_tasks_executions_assortment_before_task_id_1bad36bd
    on public.archive_tasks_executions_assortment_before (task_id);


-- Assortment
create table public.archive_tasks_executions_assortment
(
    id serial not null constraint archive_tasks_executions_assortment_pkey primary key,
    avail   double precision not null,
    good_id integer
        constraint archive_tasks_executions_good_id_d77b50fe_fk_chl_goods
            references public.chl_goods
            deferrable initially deferred,
    task_id     integer not null,
    date_start  timestamp without time zone not null,
    FOREIGN KEY ("task_id", "date_start") REFERENCES archive_tasks_executions ("id", "date_start")
);

alter table public.archive_tasks_executions_assortment
    owner to postgres;

create index archive_tasks_executions_assortment_good_id_c77b50fe
    on public.archive_tasks_executions_assortment (good_id);

create index archive_tasks_executions_assortment_task_id_1bad36bd
    on public.archive_tasks_executions_assortment (task_id);
