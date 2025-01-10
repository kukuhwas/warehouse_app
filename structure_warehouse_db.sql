--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Homebrew)
-- Dumped by pg_dump version 17.2 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: jenis_transaksi_enum; Type: TYPE; Schema: public; Owner: kukuh
--

CREATE TYPE public.jenis_transaksi_enum AS ENUM (
    'masuk',
    'keluar',
    'perpindahan'
);


ALTER TYPE public.jenis_transaksi_enum OWNER TO kukuh;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: barang; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.barang (
    id_barang integer NOT NULL,
    kode_barang character varying(255) NOT NULL,
    nama_barang character varying(255) NOT NULL,
    deskripsi text,
    kategori_id character(1),
    satuan character varying(50) NOT NULL
);


ALTER TABLE public.barang OWNER TO kukuh;

--
-- Name: barang_id_barang_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.barang_id_barang_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.barang_id_barang_seq OWNER TO kukuh;

--
-- Name: barang_id_barang_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.barang_id_barang_seq OWNED BY public.barang.id_barang;


--
-- Name: detail_pembelian; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.detail_pembelian (
    id_detail_pembelian integer NOT NULL,
    pembelian_id integer NOT NULL,
    varian_id integer NOT NULL,
    jumlah integer NOT NULL,
    harga_beli numeric(10,2) NOT NULL
);


ALTER TABLE public.detail_pembelian OWNER TO kukuh;

--
-- Name: detail_pembelian_id_detail_pembelian_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.detail_pembelian_id_detail_pembelian_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.detail_pembelian_id_detail_pembelian_seq OWNER TO kukuh;

--
-- Name: detail_pembelian_id_detail_pembelian_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.detail_pembelian_id_detail_pembelian_seq OWNED BY public.detail_pembelian.id_detail_pembelian;


--
-- Name: detail_penjualan; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.detail_penjualan (
    id_detail_penjualan integer NOT NULL,
    penjualan_id integer NOT NULL,
    varian_id integer NOT NULL,
    jumlah integer NOT NULL,
    harga_jual numeric(10,2) NOT NULL,
    diskon_nominal numeric(10,2)
);


ALTER TABLE public.detail_penjualan OWNER TO kukuh;

--
-- Name: detail_penjualan_id_detail_penjualan_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.detail_penjualan_id_detail_penjualan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.detail_penjualan_id_detail_penjualan_seq OWNER TO kukuh;

--
-- Name: detail_penjualan_id_detail_penjualan_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.detail_penjualan_id_detail_penjualan_seq OWNED BY public.detail_penjualan.id_detail_penjualan;


--
-- Name: detail_transaksi; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.detail_transaksi (
    id_detail_transaksi integer NOT NULL,
    transaksi_id integer NOT NULL,
    varian_id integer NOT NULL,
    jumlah integer NOT NULL,
    pembelian_id integer,
    penjualan_id integer,
    rak_id_asal integer,
    rak_id_tujuan integer
);


ALTER TABLE public.detail_transaksi OWNER TO kukuh;

--
-- Name: detail_transaksi_id_detail_transaksi_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.detail_transaksi_id_detail_transaksi_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.detail_transaksi_id_detail_transaksi_seq OWNER TO kukuh;

--
-- Name: detail_transaksi_id_detail_transaksi_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.detail_transaksi_id_detail_transaksi_seq OWNED BY public.detail_transaksi.id_detail_transaksi;


--
-- Name: gudang; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.gudang (
    id_gudang integer NOT NULL,
    nama_gudang character varying(255) NOT NULL,
    alamat_gudang text
);


ALTER TABLE public.gudang OWNER TO kukuh;

--
-- Name: gudang_id_gudang_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.gudang_id_gudang_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.gudang_id_gudang_seq OWNER TO kukuh;

--
-- Name: gudang_id_gudang_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.gudang_id_gudang_seq OWNED BY public.gudang.id_gudang;


--
-- Name: kategori; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.kategori (
    id_kategori character(1) NOT NULL,
    nama_kategori character varying(255) NOT NULL
);


ALTER TABLE public.kategori OWNER TO kukuh;

--
-- Name: pelanggan; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.pelanggan (
    id_pelanggan integer NOT NULL,
    nama_pelanggan character varying(255),
    kontak character varying(255),
    alamat text
);


ALTER TABLE public.pelanggan OWNER TO kukuh;

--
-- Name: pelanggan_id_pelanggan_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.pelanggan_id_pelanggan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pelanggan_id_pelanggan_seq OWNER TO kukuh;

--
-- Name: pelanggan_id_pelanggan_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.pelanggan_id_pelanggan_seq OWNED BY public.pelanggan.id_pelanggan;


--
-- Name: pembelian; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.pembelian (
    id_pembelian integer NOT NULL,
    supplier_id integer NOT NULL,
    tanggal_pembelian timestamp with time zone NOT NULL,
    keterangan text
);


ALTER TABLE public.pembelian OWNER TO kukuh;

--
-- Name: pembelian_id_pembelian_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.pembelian_id_pembelian_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pembelian_id_pembelian_seq OWNER TO kukuh;

--
-- Name: pembelian_id_pembelian_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.pembelian_id_pembelian_seq OWNED BY public.pembelian.id_pembelian;


--
-- Name: penjualan; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.penjualan (
    id_penjualan integer NOT NULL,
    pelanggan_id integer NOT NULL,
    tanggal_penjualan timestamp with time zone NOT NULL,
    keterangan text
);


ALTER TABLE public.penjualan OWNER TO kukuh;

--
-- Name: penjualan_id_penjualan_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.penjualan_id_penjualan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.penjualan_id_penjualan_seq OWNER TO kukuh;

--
-- Name: penjualan_id_penjualan_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.penjualan_id_penjualan_seq OWNED BY public.penjualan.id_penjualan;


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.permissions (
    id_permission integer NOT NULL,
    nama_permission character varying(255) NOT NULL,
    deskripsi text
);


ALTER TABLE public.permissions OWNER TO kukuh;

--
-- Name: permissions_id_permission_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.permissions_id_permission_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.permissions_id_permission_seq OWNER TO kukuh;

--
-- Name: permissions_id_permission_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.permissions_id_permission_seq OWNED BY public.permissions.id_permission;


--
-- Name: rak; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.rak (
    id_rak integer NOT NULL,
    gudang_id integer NOT NULL,
    kode_rak character varying(255) NOT NULL
);


ALTER TABLE public.rak OWNER TO kukuh;

--
-- Name: rak_id_rak_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.rak_id_rak_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rak_id_rak_seq OWNER TO kukuh;

--
-- Name: rak_id_rak_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.rak_id_rak_seq OWNED BY public.rak.id_rak;


--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.role_permissions (
    role_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.role_permissions OWNER TO kukuh;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.roles (
    id_role integer NOT NULL,
    nama_role character varying(50) NOT NULL,
    deskripsi text
);


ALTER TABLE public.roles OWNER TO kukuh;

--
-- Name: roles_id_role_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.roles_id_role_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_role_seq OWNER TO kukuh;

--
-- Name: roles_id_role_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.roles_id_role_seq OWNED BY public.roles.id_role;


--
-- Name: stok; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.stok (
    id_stok integer NOT NULL,
    varian_id integer NOT NULL,
    rak_id integer NOT NULL,
    jumlah_stok integer NOT NULL
);


ALTER TABLE public.stok OWNER TO kukuh;

--
-- Name: stok_id_stok_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.stok_id_stok_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stok_id_stok_seq OWNER TO kukuh;

--
-- Name: stok_id_stok_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.stok_id_stok_seq OWNED BY public.stok.id_stok;


--
-- Name: supplier; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.supplier (
    id_supplier integer NOT NULL,
    nama_supplier character varying(255) NOT NULL,
    kontak character varying(255),
    alamat text
);


ALTER TABLE public.supplier OWNER TO kukuh;

--
-- Name: supplier_id_supplier_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.supplier_id_supplier_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.supplier_id_supplier_seq OWNER TO kukuh;

--
-- Name: supplier_id_supplier_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.supplier_id_supplier_seq OWNED BY public.supplier.id_supplier;


--
-- Name: transaksi; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.transaksi (
    id_transaksi integer NOT NULL,
    jenis_transaksi public.jenis_transaksi_enum NOT NULL,
    tanggal_transaksi timestamp with time zone NOT NULL,
    keterangan text
);


ALTER TABLE public.transaksi OWNER TO kukuh;

--
-- Name: transaksi_id_transaksi_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.transaksi_id_transaksi_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transaksi_id_transaksi_seq OWNER TO kukuh;

--
-- Name: transaksi_id_transaksi_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.transaksi_id_transaksi_seq OWNED BY public.transaksi.id_transaksi;


--
-- Name: users; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.users (
    id_user integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    role_id integer NOT NULL,
    nama_lengkap character varying(255),
    email character varying(255),
    aktif boolean DEFAULT true
);


ALTER TABLE public.users OWNER TO kukuh;

--
-- Name: users_id_user_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.users_id_user_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_user_seq OWNER TO kukuh;

--
-- Name: users_id_user_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.users_id_user_seq OWNED BY public.users.id_user;


--
-- Name: varian; Type: TABLE; Schema: public; Owner: kukuh
--

CREATE TABLE public.varian (
    id_varian bigint NOT NULL,
    barang_id integer NOT NULL,
    nama_varian character varying(255) NOT NULL,
    nilai_varian character varying(255) NOT NULL,
    sku character varying(255) NOT NULL
);


ALTER TABLE public.varian OWNER TO kukuh;

--
-- Name: varian_id_varian_seq; Type: SEQUENCE; Schema: public; Owner: kukuh
--

CREATE SEQUENCE public.varian_id_varian_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.varian_id_varian_seq OWNER TO kukuh;

--
-- Name: varian_id_varian_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kukuh
--

ALTER SEQUENCE public.varian_id_varian_seq OWNED BY public.varian.id_varian;


--
-- Name: barang id_barang; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.barang ALTER COLUMN id_barang SET DEFAULT nextval('public.barang_id_barang_seq'::regclass);


--
-- Name: detail_pembelian id_detail_pembelian; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_pembelian ALTER COLUMN id_detail_pembelian SET DEFAULT nextval('public.detail_pembelian_id_detail_pembelian_seq'::regclass);


--
-- Name: detail_penjualan id_detail_penjualan; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_penjualan ALTER COLUMN id_detail_penjualan SET DEFAULT nextval('public.detail_penjualan_id_detail_penjualan_seq'::regclass);


--
-- Name: detail_transaksi id_detail_transaksi; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_transaksi ALTER COLUMN id_detail_transaksi SET DEFAULT nextval('public.detail_transaksi_id_detail_transaksi_seq'::regclass);


--
-- Name: gudang id_gudang; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.gudang ALTER COLUMN id_gudang SET DEFAULT nextval('public.gudang_id_gudang_seq'::regclass);


--
-- Name: pelanggan id_pelanggan; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.pelanggan ALTER COLUMN id_pelanggan SET DEFAULT nextval('public.pelanggan_id_pelanggan_seq'::regclass);


--
-- Name: pembelian id_pembelian; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.pembelian ALTER COLUMN id_pembelian SET DEFAULT nextval('public.pembelian_id_pembelian_seq'::regclass);


--
-- Name: penjualan id_penjualan; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.penjualan ALTER COLUMN id_penjualan SET DEFAULT nextval('public.penjualan_id_penjualan_seq'::regclass);


--
-- Name: permissions id_permission; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.permissions ALTER COLUMN id_permission SET DEFAULT nextval('public.permissions_id_permission_seq'::regclass);


--
-- Name: rak id_rak; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.rak ALTER COLUMN id_rak SET DEFAULT nextval('public.rak_id_rak_seq'::regclass);


--
-- Name: roles id_role; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.roles ALTER COLUMN id_role SET DEFAULT nextval('public.roles_id_role_seq'::regclass);


--
-- Name: stok id_stok; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.stok ALTER COLUMN id_stok SET DEFAULT nextval('public.stok_id_stok_seq'::regclass);


--
-- Name: supplier id_supplier; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.supplier ALTER COLUMN id_supplier SET DEFAULT nextval('public.supplier_id_supplier_seq'::regclass);


--
-- Name: transaksi id_transaksi; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.transaksi ALTER COLUMN id_transaksi SET DEFAULT nextval('public.transaksi_id_transaksi_seq'::regclass);


--
-- Name: users id_user; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.users ALTER COLUMN id_user SET DEFAULT nextval('public.users_id_user_seq'::regclass);


--
-- Name: varian id_varian; Type: DEFAULT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.varian ALTER COLUMN id_varian SET DEFAULT nextval('public.varian_id_varian_seq'::regclass);


--
-- Name: barang barang_kode_barang_key; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.barang
    ADD CONSTRAINT barang_kode_barang_key UNIQUE (kode_barang);


--
-- Name: barang barang_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.barang
    ADD CONSTRAINT barang_pkey PRIMARY KEY (id_barang);


--
-- Name: detail_pembelian detail_pembelian_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_pembelian
    ADD CONSTRAINT detail_pembelian_pkey PRIMARY KEY (id_detail_pembelian);


--
-- Name: detail_penjualan detail_penjualan_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_penjualan
    ADD CONSTRAINT detail_penjualan_pkey PRIMARY KEY (id_detail_penjualan);


--
-- Name: detail_transaksi detail_transaksi_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_transaksi
    ADD CONSTRAINT detail_transaksi_pkey PRIMARY KEY (id_detail_transaksi);


--
-- Name: gudang gudang_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.gudang
    ADD CONSTRAINT gudang_pkey PRIMARY KEY (id_gudang);


--
-- Name: kategori kategori_nama_kategori_key; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.kategori
    ADD CONSTRAINT kategori_nama_kategori_key UNIQUE (nama_kategori);


--
-- Name: kategori kategori_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.kategori
    ADD CONSTRAINT kategori_pkey PRIMARY KEY (id_kategori);


--
-- Name: pelanggan pelanggan_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.pelanggan
    ADD CONSTRAINT pelanggan_pkey PRIMARY KEY (id_pelanggan);


--
-- Name: pembelian pembelian_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.pembelian
    ADD CONSTRAINT pembelian_pkey PRIMARY KEY (id_pembelian);


--
-- Name: penjualan penjualan_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.penjualan
    ADD CONSTRAINT penjualan_pkey PRIMARY KEY (id_penjualan);


--
-- Name: permissions permissions_nama_permission_key; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_nama_permission_key UNIQUE (nama_permission);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id_permission);


--
-- Name: rak rak_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.rak
    ADD CONSTRAINT rak_pkey PRIMARY KEY (id_rak);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (role_id, permission_id);


--
-- Name: roles roles_nama_role_key; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_nama_role_key UNIQUE (nama_role);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id_role);


--
-- Name: stok stok_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.stok
    ADD CONSTRAINT stok_pkey PRIMARY KEY (id_stok);


--
-- Name: supplier supplier_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.supplier
    ADD CONSTRAINT supplier_pkey PRIMARY KEY (id_supplier);


--
-- Name: transaksi transaksi_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.transaksi
    ADD CONSTRAINT transaksi_pkey PRIMARY KEY (id_transaksi);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id_user);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: varian varian_pkey; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.varian
    ADD CONSTRAINT varian_pkey PRIMARY KEY (id_varian);


--
-- Name: varian varian_sku_key; Type: CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.varian
    ADD CONSTRAINT varian_sku_key UNIQUE (sku);


--
-- Name: barang barang_kategori_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.barang
    ADD CONSTRAINT barang_kategori_id_fkey FOREIGN KEY (kategori_id) REFERENCES public.kategori(id_kategori);


--
-- Name: detail_pembelian detail_pembelian_pembelian_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_pembelian
    ADD CONSTRAINT detail_pembelian_pembelian_id_fkey FOREIGN KEY (pembelian_id) REFERENCES public.pembelian(id_pembelian);


--
-- Name: detail_pembelian detail_pembelian_varian_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_pembelian
    ADD CONSTRAINT detail_pembelian_varian_id_fkey FOREIGN KEY (varian_id) REFERENCES public.varian(id_varian);


--
-- Name: detail_penjualan detail_penjualan_penjualan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_penjualan
    ADD CONSTRAINT detail_penjualan_penjualan_id_fkey FOREIGN KEY (penjualan_id) REFERENCES public.penjualan(id_penjualan);


--
-- Name: detail_penjualan detail_penjualan_varian_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_penjualan
    ADD CONSTRAINT detail_penjualan_varian_id_fkey FOREIGN KEY (varian_id) REFERENCES public.varian(id_varian);


--
-- Name: detail_transaksi detail_transaksi_pembelian_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_transaksi
    ADD CONSTRAINT detail_transaksi_pembelian_id_fkey FOREIGN KEY (pembelian_id) REFERENCES public.pembelian(id_pembelian);


--
-- Name: detail_transaksi detail_transaksi_penjualan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_transaksi
    ADD CONSTRAINT detail_transaksi_penjualan_id_fkey FOREIGN KEY (penjualan_id) REFERENCES public.penjualan(id_penjualan);


--
-- Name: detail_transaksi detail_transaksi_rak_id_asal_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_transaksi
    ADD CONSTRAINT detail_transaksi_rak_id_asal_fkey FOREIGN KEY (rak_id_asal) REFERENCES public.rak(id_rak);


--
-- Name: detail_transaksi detail_transaksi_rak_id_tujuan_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_transaksi
    ADD CONSTRAINT detail_transaksi_rak_id_tujuan_fkey FOREIGN KEY (rak_id_tujuan) REFERENCES public.rak(id_rak);


--
-- Name: detail_transaksi detail_transaksi_transaksi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_transaksi
    ADD CONSTRAINT detail_transaksi_transaksi_id_fkey FOREIGN KEY (transaksi_id) REFERENCES public.transaksi(id_transaksi);


--
-- Name: detail_transaksi detail_transaksi_varian_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.detail_transaksi
    ADD CONSTRAINT detail_transaksi_varian_id_fkey FOREIGN KEY (varian_id) REFERENCES public.varian(id_varian);


--
-- Name: pembelian pembelian_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.pembelian
    ADD CONSTRAINT pembelian_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.supplier(id_supplier);


--
-- Name: penjualan penjualan_pelanggan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.penjualan
    ADD CONSTRAINT penjualan_pelanggan_id_fkey FOREIGN KEY (pelanggan_id) REFERENCES public.pelanggan(id_pelanggan);


--
-- Name: rak rak_gudang_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.rak
    ADD CONSTRAINT rak_gudang_id_fkey FOREIGN KEY (gudang_id) REFERENCES public.gudang(id_gudang);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id_permission);


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id_role);


--
-- Name: stok stok_rak_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.stok
    ADD CONSTRAINT stok_rak_id_fkey FOREIGN KEY (rak_id) REFERENCES public.rak(id_rak);


--
-- Name: stok stok_varian_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.stok
    ADD CONSTRAINT stok_varian_id_fkey FOREIGN KEY (varian_id) REFERENCES public.varian(id_varian);


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id_role);


--
-- Name: varian varian_barang_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kukuh
--

ALTER TABLE ONLY public.varian
    ADD CONSTRAINT varian_barang_id_fkey FOREIGN KEY (barang_id) REFERENCES public.barang(id_barang);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT USAGE ON SCHEMA public TO operator;
GRANT USAGE ON SCHEMA public TO kasir;
GRANT ALL ON SCHEMA public TO wh_admin;


--
-- Name: TABLE barang; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.barang TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.barang TO operator;
GRANT SELECT ON TABLE public.barang TO kasir;


--
-- Name: TABLE detail_pembelian; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.detail_pembelian TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.detail_pembelian TO operator;


--
-- Name: TABLE detail_penjualan; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.detail_penjualan TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.detail_penjualan TO kasir;


--
-- Name: TABLE detail_transaksi; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.detail_transaksi TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.detail_transaksi TO operator;


--
-- Name: TABLE gudang; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.gudang TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.gudang TO operator;


--
-- Name: TABLE kategori; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.kategori TO wh_admin;
GRANT SELECT ON TABLE public.kategori TO operator;
GRANT SELECT ON TABLE public.kategori TO kasir;


--
-- Name: TABLE pelanggan; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.pelanggan TO wh_admin;
GRANT SELECT ON TABLE public.pelanggan TO kasir;


--
-- Name: TABLE pembelian; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.pembelian TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.pembelian TO operator;


--
-- Name: TABLE penjualan; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.penjualan TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.penjualan TO kasir;


--
-- Name: TABLE permissions; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.permissions TO wh_admin;


--
-- Name: TABLE rak; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.rak TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.rak TO operator;


--
-- Name: TABLE role_permissions; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.role_permissions TO wh_admin;


--
-- Name: TABLE roles; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.roles TO wh_admin;


--
-- Name: TABLE stok; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.stok TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stok TO operator;


--
-- Name: TABLE supplier; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.supplier TO wh_admin;
GRANT SELECT ON TABLE public.supplier TO operator;


--
-- Name: TABLE transaksi; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.transaksi TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.transaksi TO operator;


--
-- Name: TABLE users; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.users TO wh_admin;


--
-- Name: TABLE varian; Type: ACL; Schema: public; Owner: kukuh
--

GRANT ALL ON TABLE public.varian TO wh_admin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.varian TO operator;
GRANT SELECT ON TABLE public.varian TO kasir;


--
-- PostgreSQL database dump complete
--

