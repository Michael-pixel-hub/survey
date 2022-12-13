ALTER TABLE public.archive_tasks_executions
    ADD COLUMN constructor_step_id integer;

ALTER TABLE public.archive_tasks_executions
ADD CONSTRAINT archive_tasks_executions_constructor_step_id_fk_chl_tasks_steps FOREIGN KEY (constructor_step_id)
        REFERENCES public.chl_tasks_steps (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE public.archive_tasks_executions_images
    ADD COLUMN constructor_step_name character varying(200) COLLATE pg_catalog."default" NOT NULL default '',
	ADD COLUMN constructor_check boolean NOT NULL default false;

ALTER TABLE public.archive_tasks_executions_assortment
    ADD COLUMN constructor_step_name character varying(200) COLLATE pg_catalog."default" NOT NULL default '';

CREATE SEQUENCE IF NOT EXISTS public.archive_tasks_executions_questionnairess_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

ALTER SEQUENCE public.archive_tasks_executions_questionnairess_id_seq
    OWNER TO postgres;

CREATE TABLE IF NOT EXISTS public.archive_tasks_executions_questionnairess
(
    id integer NOT NULL DEFAULT nextval('archive_tasks_executions_questionnairess_id_seq'::regclass),
    question character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    answer character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    task_id integer NOT NULL,
    date_start timestamp without time zone NOT NULL,
    constructor_step_name character varying(200) COLLATE pg_catalog."default" NOT NULL,
    name character varying(200) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT archive_tasks_executions_questionnairess_pkey PRIMARY KEY (id),
    CONSTRAINT archive_tasks_executions_que_name_task_id_constructor_ee49c80e_uniq UNIQUE (name, task_id, constructor_step_name),
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey1 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2018_m09 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey10 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m06 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey11 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m07 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey12 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m08 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey13 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m09 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey14 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m10 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey15 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m11 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey16 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m12 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey17 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m01 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey18 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m02 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey19 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m03 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey2 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2018_m10 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey20 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m04 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey21 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m05 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey22 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m06 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey23 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m07 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey24 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m08 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey25 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m09 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey26 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m10 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey27 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m11 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey28 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2020_m12 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey29 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m01 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey3 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2018_m11 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey30 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m02 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey31 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m03 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey32 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m04 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey33 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m05 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey34 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m06 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey35 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m07 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey36 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m08 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey37 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m09 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey38 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m10 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey39 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m11 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey4 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2018_m12 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey40 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2021_m12 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey5 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m01 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey6 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m02 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey7 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m03 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey8 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m04 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT archive_tasks_executions_qr_task_id_date_start_fkey9 FOREIGN KEY (date_start, task_id)
        REFERENCES public.archive_tasks_executions_y2019_m05 (date_start, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.archive_tasks_executions_questionnairess
    OWNER TO postgres;

CREATE INDEX archive_tasks_executions_qr_task_id_1bad36bd
    ON public.archive_tasks_executions_questionnairess USING btree
    (task_id ASC NULLS LAST)
    TABLESPACE pg_default;
