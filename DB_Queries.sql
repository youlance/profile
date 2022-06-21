CREATE DATABASE profiles
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;



CREATE TABLE IF NOT EXISTS public.profiles
(
    id integer NOT NULL DEFAULT nextval('profiles_id_seq'::regclass),
    username character varying COLLATE pg_catalog."default" NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    email character varying COLLATE pg_catalog."default" NOT NULL,
    gender character varying COLLATE pg_catalog."default" NOT NULL,
    birthdate date NOT NULL,
    picture character varying COLLATE pg_catalog."default",
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT profiles_pkey PRIMARY KEY (username)
)

TABLESPACE pg_default;


ALTER TABLE IF EXISTS public.profiles
    ADD COLUMN bio character varying;


ALTER TABLE IF EXISTS public.profiles
    OWNER to postgres;
