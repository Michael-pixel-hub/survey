ALTER TABLE IF EXISTS public.archive_tasks_executions
    ADD COLUMN "check" character varying(20) NOT NULL DEFAULT 'not_need';
