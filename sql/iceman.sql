ALTER TABLE IF EXISTS public.archive_tasks_executions
    ADD COLUMN application character varying(20) NOT NULL DEFAULT 'shop_survey';

ALTER TABLE IF EXISTS public.archive_tasks_executions
    ADD COLUMN store_iceman_id integer;
ALTER TABLE IF EXISTS public.archive_tasks_executions
    ADD CONSTRAINT archive_tasks_executions_store_iceman_id_69b8ed3f_fk_iceman_st FOREIGN KEY (store_iceman_id)
    REFERENCES public.iceman_stores (id) MATCH SIMPLE;
