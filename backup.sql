--
-- PostgreSQL database dump
--

-- Dumped from database version 12.18 (Ubuntu 12.18-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.18 (Ubuntu 12.18-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.Users (
    userid VARCHAR(40) PRIMARY KEY,
    username VARCHAR(40) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

ALTER TABLE public.Users OWNER TO postgres;

--
-- Name: Roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.Roles (
    roleid VARCHAR(40) PRIMARY KEY,
    rolename VARCHAR(40) UNIQUE NOT NULL
);

ALTER TABLE public.Roles OWNER TO postgres;

--
-- Name: UserRoles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.UserRoles (
    userid VARCHAR(40) REFERENCES public.Users(userid),
    roleid VARCHAR(40) REFERENCES public.Roles(roleid),
    PRIMARY KEY (userid, roleid)
);

ALTER TABLE public.UserRoles OWNER TO postgres;

--
-- PostgreSQL database dump complete
--
