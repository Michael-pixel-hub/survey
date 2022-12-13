ALTER TABLE IF EXISTS public.archive_tasks_executions
    ADD COLUMN source character varying(20) NOT NULL DEFAULT 'undefined';
