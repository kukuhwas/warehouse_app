import psycopg2
import configparser
import uuid
from core.models import Kategori, Barang, Varian, Supplier, Gudang, Rak, Pelanggan, Pembelian, Penjualan
from datetime import datetime


def load_config(filepath="data/config.ini", environment="production"):
    """Memuat konfigurasi database dari file config.ini."""
    config = configparser.ConfigParser()
    config.read(filepath)
    if environment == "development":
        return config['database_dev']
    else:
        return config['database']

def load_app_config(filepath="data/config.ini"):
    """Memuat konfigurasi aplikasi dari file config.ini."""
    config = configparser.ConfigParser()
    config.read(filepath)
    return config['app']

def _create_connection(db_config):
    """Membuat koneksi ke database menggunakan konfigurasi."""
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        print(f"Berhasil koneksi ke database {db_config['database']}!")
        return conn
    except psycopg2.Error as e:
        print(f"Error koneksi ke database: {e}")
        return None

def connect_to_db(environment="production"):
    """Membuat koneksi ke database PostgreSQL."""
    db_config = load_config(environment=environment)
    return _create_connection(db_config)

def create_kategori(conn, kategori):
    """Menambahkan data kategori baru ke database."""
    app_config = load_app_config()
    max_kategori = int(app_config['max_kategori'])

    cursor = conn.cursor()
    try:
        # Cek apakah jumlah kategori sudah mencapai batas maksimal
        cursor.execute("SELECT COUNT(*) FROM kategori")
        count = cursor.fetchone()[0]
        if count >= max_kategori:
            print(f"Error: Jumlah kategori sudah mencapai batas maksimal ({max_kategori}).")
            return None

        # Cek apakah kategori dengan ID tersebut sudah ada
        cursor.execute("SELECT COUNT(*) FROM kategori WHERE id_kategori = %s", (kategori.id_kategori,))
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"Error: Kategori dengan ID {kategori.id_kategori} sudah ada.")
            return None

        # Jika belum mencapai batas maksimal, tambahkan kategori baru
        cursor.execute("INSERT INTO kategori (id_kategori, nama_kategori) VALUES (%s, %s)", (kategori.id_kategori, kategori.nama_kategori))
        conn.commit()
        print("Data kategori berhasil ditambahkan.")
        return kategori.id_kategori
    except psycopg2.Error as e:
        print(f"Error menambahkan kategori: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def get_all_kategori(conn):
    """Mengambil semua data kategori dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM kategori")
        rows = cursor.fetchall()
        kategori_list = []
        for row in rows:
            kategori = Kategori(row[0], row[1])
            kategori_list.append(kategori)
        return kategori_list
    except psycopg2.Error as e:
        print(f"Error mengambil data kategori: {e}")
        return None
    finally:
        cursor.close()

def get_kategori(conn, id_kategori):
    """Mengambil data kategori berdasarkan id_kategori."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM kategori WHERE id_kategori = %s", (id_kategori,))
        row = cursor.fetchone()
        if row:
            kategori = Kategori(row[0], row[1])
            return kategori
        else:
            print("Kategori tidak ditemukan.")
            return None
    except psycopg2.Error as e:
        print(f"Error mengambil data kategori: {e}")
        return None
    finally:
        cursor.close()

def update_kategori(conn, kategori):
    """Memperbarui data kategori di database."""
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE kategori SET nama_kategori = %s WHERE id_kategori = %s", (kategori.nama_kategori, kategori.id_kategori))
        conn.commit()
        print("Data kategori berhasil diperbarui.")
    except psycopg2.Error as e:
        print(f"Error memperbarui kategori: {e}")
        conn.rollback()
    finally:
        cursor.close()

def delete_kategori(conn, id_kategori):
    """Menghapus data kategori dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM kategori WHERE id_kategori = %s", (id_kategori,))
        conn.commit()
        print("Data kategori berhasil dihapus.")
    except psycopg2.Error as e:
        print(f"Error menghapus kategori: {e}")
        conn.rollback()
    finally:
        cursor.close()

def generate_kode_barang(conn, kategori_id):
    """
    Membuat kode barang baru berdasarkan kategori_id dengan UUID.

    Args:
        conn: Objek koneksi database.
        kategori_id: ID kategori barang.

    Returns:
        String kode barang baru, atau None jika terjadi error.
    """
    cursor = conn.cursor()
    try:
        # Generate UUID versi 4, konversi ke string, ambil 4 karakter pertama, dan uppercase
        new_uuid = str(uuid.uuid4()).upper()[:4]
        kode_barang = f"{kategori_id}{new_uuid}"

        return kode_barang
    except psycopg2.Error as e:
        print(f"Error generating kode barang: {e}")
        return None
    finally:
        cursor.close()

def create_barang(conn, barang):
    """Menambahkan data barang baru ke database."""
    cursor = conn.cursor()
    try:
        # Generate kode barang
        kode_barang = generate_kode_barang(conn, barang.kategori_id)
        if kode_barang is None:
            print("Error: Gagal membuat kode barang.")
            return None

        barang.kode_barang = kode_barang

        # Query untuk insert data barang
        cursor.execute("INSERT INTO barang (kode_barang, nama_barang, deskripsi, kategori_id, satuan) VALUES (%s, %s, %s, %s, %s)",
                       (barang.kode_barang, barang.nama_barang, barang.deskripsi, barang.kategori_id, barang.satuan))
        conn.commit()
        print("Data barang berhasil ditambahkan.")

        # Mendapatkan ID barang yang baru saja di-insert
        cursor.execute("SELECT currval(pg_get_serial_sequence('barang','id_barang'))")
        barang_id = cursor.fetchone()[0]

        return barang_id
    except psycopg2.Error as e:
        print(f"Error menambahkan barang: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def get_all_barang(conn):
    """Mengambil semua data barang dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM barang")
        rows = cursor.fetchall()
        barang_list = []
        for row in rows:
            barang = Barang(row[0], row[1], row[2], row[3], row[4], row[5])
            barang_list.append(barang)
        return barang_list
    except psycopg2.Error as e:
        print(f"Error mengambil data barang: {e}")
        return None
    finally:
        cursor.close()

def get_barang(conn, id_barang):
    """Mengambil data barang berdasarkan id_barang."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM barang WHERE id_barang = %s", (id_barang,))
        row = cursor.fetchone()
        if row:
            barang = Barang(row[0], row[1], row[2], row[3], row[4], row[5])
            return barang
        else:
            print("Barang tidak ditemukan.")
            return None
    except psycopg2.Error as e:
        print(f"Error mengambil data barang: {e}")
        return None
    finally:
        cursor.close()

def update_barang(conn, barang):
    """Memperbarui data barang di database."""
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE barang SET kode_barang = %s, nama_barang = %s, deskripsi = %s, kategori_id = %s, satuan = %s WHERE id_barang = %s",
                       (barang.kode_barang, barang.nama_barang, barang.deskripsi, barang.kategori_id, barang.satuan, barang.id_barang))
        conn.commit()
        print("Data barang berhasil diperbarui.")
    except psycopg2.Error as e:
        print(f"Error memperbarui barang: {e}")
        conn.rollback()
    finally:
        cursor.close()

def delete_barang(conn, id_barang):
    """Menghapus data barang dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM barang WHERE id_barang = %s", (id_barang,))
        conn.commit()
        print("Data barang berhasil dihapus.")
    except psycopg2.Error as e:
        print(f"Error menghapus barang: {e}")
        conn.rollback()
    finally:
        cursor.close()

def generate_sku(conn, barang_id, nama_varian, nilai_varian):
    cursor = conn.cursor()
    try:
        # 1. Ambil kode barang (2 karakter)
        cursor.execute("SELECT kode_barang FROM barang WHERE id_barang = %s", (barang_id,))
        row = cursor.fetchone()
        if row is None:
            print(f"Error: Barang dengan ID {barang_id} tidak ditemukan.")
            return None
        kode_barang = row[0][:2]

        # 2. Buat kode varian (3 karakter) - Sekarang hanya dari nilai_varian
        kode_varian = nilai_varian[0].upper() # Hanya ambil karakter pertama dari nilai varian
        kode_varian = kode_varian.ljust(3, 'X')[:3]  # Padding dengan 'X'

        # 3. Ambil tahun dan bulan (YYMM)
        yymm = datetime.now().strftime("%y%m")

        # 4. Ambil 2 karakter dari UUID
        uu = str(uuid.uuid4()).upper()[:2]

        # Gabungkan menjadi SKU
        sku = f"{kode_barang}-{kode_varian}-{yymm}-{uu}"
        return sku
    except psycopg2.Error as e:
        print(f"Error generating SKU: {e}")
        return None
    finally:
        cursor.close()

def create_varian(conn, varian):
    """Menambahkan data varian baru ke database."""
    cursor = conn.cursor()
    try:
        # Validasi nama_varian
        if varian.nama_varian.upper() != "WARNA":
            print("Error: Nama varian harus 'Warna'.")
            return None

        # Generate SKU
        sku = generate_sku(conn, varian.barang_id, varian.nama_varian, varian.nilai_varian)
        if sku is None:
            print("Error: Gagal membuat SKU.")
            return None

        varian.sku = sku # Set nilai sku ke objek varian

        cursor.execute("INSERT INTO varian (barang_id, nama_varian, nilai_varian, sku) VALUES (%s, %s, %s, %s)",
                       (varian.barang_id, varian.nama_varian, varian.nilai_varian, varian.sku))
        conn.commit()
        print("Data varian berhasil ditambahkan.")
        # Mendapatkan ID varian yang baru saja di-insert
        cursor.execute("SELECT currval(pg_get_serial_sequence('varian','id_varian'))")
        varian_id = cursor.fetchone()[0]
        return varian_id
    except psycopg2.Error as e:
        print(f"Error menambahkan varian: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def get_all_varian(conn):
    """Mengambil semua data varian dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT v.*, b.kode_barang FROM varian v JOIN barang b ON v.barang_id = b.id_barang")
        rows = cursor.fetchall()
        varian_list = []
        for row in rows:
            varian = Varian(row[0], row[1], row[2], row[3], row[4])  # Hanya 5 argumen
            varian_list.append(varian)
        return varian_list
    except psycopg2.Error as e:
        print(f"Error mengambil semua varian: {e}")
        return None
    finally:
        cursor.close()

def get_varian_by_barang_id(conn, barang_id):
    """Mengambil data varian berdasarkan barang_id."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM varian WHERE barang_id = %s", (barang_id,))
        rows = cursor.fetchall()
        varian_list = []
        for row in rows:
            varian = Varian(row[0], row[1], row[2], row[3], row[4])  # Tambahkan argumen sku
            varian_list.append(varian)
        return varian_list
    except psycopg2.Error as e:
        print(f"Error mengambil varian berdasarkan barang_id: {e}")
        return None
    finally:
        cursor.close()

def get_varian_by_nilai_varian(conn, barang_id, nilai_varian):
    """Mengambil data varian berdasarkan barang_id dan nilai_varian."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM varian WHERE barang_id = %s AND nilai_varian = %s", (barang_id, nilai_varian))
        row = cursor.fetchone()
        if row:
            return Varian(row[0], row[1], row[2], row[3], row[4])
        return None
    except psycopg2.Error as e:
        print(f"Error mengambil varian berdasarkan nilai_varian: {e}")
        return None
    finally:
        cursor.close()

def update_varian(conn, varian):
    """Memperbarui data varian di database.

    Args:
        conn: Objek koneksi database.
        varian: Objek Varian yang berisi data yang akan diupdate.
    """
    cursor = conn.cursor()
    try:
        # Generate SKU baru jika nama_varian atau nilai_varian berubah
        sku = generate_sku(conn, varian.barang_id, varian.nama_varian, varian.nilai_varian)
        if sku is None:
            print("Error: Gagal membuat SKU.")
            return False

        varian.sku = sku

        cursor.execute("UPDATE varian SET barang_id = %s, nama_varian = %s, nilai_varian = %s, sku = %s WHERE id_varian = %s",
                       (varian.barang_id, varian.nama_varian, varian.nilai_varian, varian.sku, varian.id_varian))
        conn.commit()
        print("Data varian berhasil diperbarui.")
        return True
    except psycopg2.Error as e:
        print(f"Error memperbarui varian: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def delete_varian(conn, id_varian):
    """Menghapus data varian dari database berdasarkan id_varian.

    Args:
        conn: Objek koneksi database.
        id_varian: ID varian yang akan dihapus.

    Returns:
        True jika berhasil dihapus, False jika gagal.
    """
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM varian WHERE id_varian = %s", (id_varian,))
        conn.commit()
        print("Data varian berhasil dihapus.")
        return True
    except psycopg2.Error as e:
        print(f"Error menghapus varian: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def get_varian(conn, id_varian):
    """Mengambil data varian berdasarkan id_varian."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM varian WHERE id_varian = %s", (id_varian,))
        row = cursor.fetchone()
        if row:
            return Varian(row[0], row[1], row[2], row[3], row[4])
        return None
    except psycopg2.Error as e:
        print(f"Error mengambil varian: {e}")
        return None
    finally:
        cursor.close()

def create_supplier(conn, supplier):
    """Menambahkan data supplier baru ke database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO supplier (nama_supplier, kontak, alamat) VALUES (%s, %s, %s) RETURNING id_supplier",
            (supplier.nama_supplier, supplier.kontak, supplier.alamat)
        )
        supplier_id = cursor.fetchone()[0]
        conn.commit()
        return supplier_id
    except psycopg2.Error as e:
        print(f"Error menambahkan supplier: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def get_all_suppliers(conn):
    """Mengambil semua data supplier dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM supplier")
        rows = cursor.fetchall()
        supplier_list = []
        for row in rows:
            supplier = Supplier(row[0], row[1], row[2], row[3])
            supplier_list.append(supplier)
        return supplier_list
    except psycopg2.Error as e:
        print(f"Error mengambil semua supplier: {e}")
        return None
    finally:
        cursor.close()

def get_supplier(conn, id_supplier):
    """Mengambil data supplier berdasarkan id_supplier."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM supplier WHERE id_supplier = %s", (id_supplier,))
        row = cursor.fetchone()
        if row:
            return Supplier(row[0], row[1], row[2], row[3])
        return None
    except psycopg2.Error as e:
        print(f"Error mengambil supplier: {e}")
        return None
    finally:
        cursor.close()

def update_supplier(conn, supplier):
    """Memperbarui data supplier di database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE supplier SET nama_supplier = %s, alamat = %s, kontak = %s WHERE id_supplier = %s",
            (supplier.nama_supplier, supplier.alamat, supplier.kontak, supplier.id_supplier)
        )
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error memperbarui supplier: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def delete_supplier(conn, id_supplier):
    """Menghapus data supplier dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM supplier WHERE id_supplier = %s", (id_supplier,))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error menghapus supplier: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def create_gudang(conn, gudang):
    """Menambahkan data gudang baru ke database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO gudang (nama_gudang, alamat_gudang) VALUES (%s, %s) RETURNING id_gudang",
            (gudang.nama_gudang, gudang.alamat_gudang)
        )
        gudang_id = cursor.fetchone()[0]
        conn.commit()
        return gudang_id
    except psycopg2.Error as e:
        print(f"Error menambahkan gudang: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def get_all_gudang(conn):
    """Mengambil semua data gudang dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM gudang")
        rows = cursor.fetchall()
        gudang_list = []
        for row in rows:
            gudang = Gudang(row[0], row[1], row[2])
            gudang_list.append(gudang)
        return gudang_list
    except psycopg2.Error as e:
        print(f"Error mengambil data gudang: {e}")
        return None
    finally:
        cursor.close()

def get_gudang(conn, id_gudang):
    """Mengambil data gudang berdasarkan id_gudang."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM gudang WHERE id_gudang = %s", (id_gudang,))
        row = cursor.fetchone()
        if row:
            gudang = Gudang(row[0], row[1], row[2])
            return gudang
        else:
            print("Gudang tidak ditemukan.")
            return None
    except psycopg2.Error as e:
        print(f"Error mengambil data gudang: {e}")
        return None
    finally:
        cursor.close()

def update_gudang(conn, gudang):
    """Memperbarui data gudang di database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE gudang SET nama_gudang = %s, alamat_gudang = %s WHERE id_gudang = %s",
            (gudang.nama_gudang, gudang.alamat_gudang, gudang.id_gudang)
        )
        conn.commit()
        print("Data gudang berhasil diperbarui.")
    except psycopg2.Error as e:
        print(f"Error memperbarui gudang: {e}")
        conn.rollback()
    finally:
        cursor.close()

def delete_gudang(conn, id_gudang):
    """Menghapus data gudang dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM gudang WHERE id_gudang = %s", (id_gudang,))
        conn.commit()
        print("Data gudang berhasil dihapus.")
    except psycopg2.Error as e:
        print(f"Error menghapus gudang: {e}")
        conn.rollback()
    finally:
        cursor.close()


def create_rak(conn, rak):
    """Menambahkan data rak baru ke database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO rak (gudang_id, kode_rak) VALUES (%s, %s) RETURNING id_rak",
            (rak.gudang_id, rak.kode_rak)
        )
        rak_id = cursor.fetchone()[0]
        conn.commit()
        return rak_id
    except psycopg2.Error as e:
        print(f"Error menambahkan rak: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def get_all_rak(conn):
    """Mengambil semua data rak dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM rak")
        rows = cursor.fetchall()
        rak_list = []
        for row in rows:
            rak = Rak(row[0], row[1], row[2])
            rak_list.append(rak)
        return rak_list
    except psycopg2.Error as e:
        print(f"Error mengambil data rak: {e}")
        return None
    finally:
        cursor.close()

def get_rak(conn, id_rak):
    """Mengambil data rak berdasarkan id_rak."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM rak WHERE id_rak = %s", (id_rak,))
        row = cursor.fetchone()
        if row:
            rak = Rak(row[0], row[1], row[2])
            return rak
        else:
            print("Rak tidak ditemukan.")
            return None
    except psycopg2.Error as e:
        print(f"Error mengambil data rak: {e}")
        return None
    finally:
        cursor.close()

def update_rak(conn, rak):
    """Memperbarui data rak di database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE rak SET kode_rak = %s, gudang_id = %s WHERE id_rak = %s",
            (rak.kode_rak, rak.gudang_id, rak.id_rak)
        )
        conn.commit()
        print("Data rak berhasil diperbarui.")
    except psycopg2.Error as e:
        print(f"Error memperbarui rak: {e}")
        conn.rollback()
    finally:
        cursor.close()

def delete_rak(conn, id_rak):
    """Menghapus data rak dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM rak WHERE id_rak = %s", (id_rak,))
        conn.commit()
        print("Data rak berhasil dihapus.")
    except psycopg2.Error as e:
        print(f"Error menghapus rak: {e}")
        conn.rollback()
    finally:
        cursor.close()

def create_pelanggan(conn, pelanggan):
    """Menambahkan data pelanggan baru ke database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO pelanggan (nama_pelanggan, kontak, alamat) VALUES (%s, %s, %s) RETURNING id_pelanggan",
            (pelanggan.nama_pelanggan, pelanggan.kontak, pelanggan.alamat)
        )
        pelanggan_id = cursor.fetchone()[0]
        conn.commit()
        return pelanggan_id
    except psycopg2.Error as e:
        print(f"Error menambahkan pelanggan: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def get_all_pelanggan(conn):
    """Mengambil semua data pelanggan dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pelanggan")
        rows = cursor.fetchall()
        pelanggan_list = []
        for row in rows:
            pelanggan = Pelanggan(row[0], row[1], row[2], row[3])
            pelanggan_list.append(pelanggan)
        return pelanggan_list
    except psycopg2.Error as e:
        print(f"Error mengambil data pelanggan: {e}")
        return None
    finally:
        cursor.close()

def get_pelanggan(conn, id_pelanggan):
    """Mengambil data pelanggan berdasarkan id_pelanggan."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pelanggan WHERE id_pelanggan = %s", (id_pelanggan,))
        row = cursor.fetchone()
        if row:
            pelanggan = Pelanggan(row[0], row[1], row[2], row[3])
            return pelanggan
        else:
            print("Pelanggan tidak ditemukan.")
            return None
    except psycopg2.Error as e:
        print(f"Error mengambil data pelanggan: {e}")
        return None
    finally:
        cursor.close()

def update_pelanggan(conn, pelanggan):
    """Memperbarui data pelanggan di database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE pelanggan SET nama_pelanggan = %s, kontak = %s, alamat = %s WHERE id_pelanggan = %s",
            (pelanggan.nama_pelanggan, pelanggan.kontak, pelanggan.alamat, pelanggan.id_pelanggan)
        )
        conn.commit()
        print("Data pelanggan berhasil diperbarui.")
    except psycopg2.Error as e:
        print(f"Error memperbarui pelanggan: {e}")
        conn.rollback()
    finally:
        cursor.close()

def delete_pelanggan(conn, id_pelanggan):
    """Menghapus data pelanggan dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pelanggan WHERE id_pelanggan = %s", (id_pelanggan,))
        conn.commit()
        print("Data pelanggan berhasil dihapus.")
    except psycopg2.Error as e:
        print(f"Error menghapus pelanggan: {e}")
        conn.rollback()
    finally:
        cursor.close()

def create_pembelian(conn, pembelian):
    """Menambahkan data pembelian baru ke database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO pembelian (tanggal_pembelian, supplier_id, keterangan) VALUES (%s, %s, %s) RETURNING id_pembelian",
            (pembelian.tanggal_pembelian, pembelian.supplier_id, pembelian.keterangan)
        )
        pembelian_id = cursor.fetchone()[0]
        conn.commit()
        return pembelian_id
    except psycopg2.Error as e:
        print(f"Error menambahkan pembelian: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def get_all_pembelian(conn):
    """Mengambil semua data pembelian dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pembelian")
        rows = cursor.fetchall()
        pembelian_list = []
        for row in rows:
            pembelian = Pembelian(row[0], row[1], row[2], row[3])
            pembelian_list.append(pembelian)
        return pembelian_list
    except psycopg2.Error as e:
        print(f"Error mengambil data pembelian: {e}")
        return None
    finally:
        cursor.close()

def get_pembelian(conn, id_pembelian):
    """Mengambil data pembelian berdasarkan id_pembelian."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM pembelian WHERE id_pembelian = %s", (id_pembelian,))
        row = cursor.fetchone()
        if row:
            pembelian = Pembelian(row[0], row[1], row[2], row[3])
            return pembelian
        else:
            print("Pembelian tidak ditemukan.")
            return None
    except psycopg2.Error as e:
        print(f"Error mengambil data pembelian: {e}")
        return None
    finally:
        cursor.close()

def update_pembelian(conn, pembelian):
    """Memperbarui data pembelian di database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE pembelian SET tanggal_pembelian = %s, supplier_id = %s, keterangan = %s WHERE id_pembelian = %s",
            (pembelian.tanggal_pembelian, pembelian.supplier_id, pembelian.keterangan, pembelian.id_pembelian)
        )
        conn.commit()
        print("Data pembelian berhasil diperbarui.")
    except psycopg2.Error as e:
        print(f"Error memperbarui pembelian: {e}")
        conn.rollback()
    finally:
        cursor.close()

def delete_pembelian(conn, id_pembelian):
    """Menghapus data pembelian dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pembelian WHERE id_pembelian = %s", (id_pembelian,))
        conn.commit()
        print("Data pembelian berhasil dihapus.")
    except psycopg2.Error as e:
        print(f"Error menghapus pembelian: {e}")
        conn.rollback()
    finally:
        cursor.close()

def create_penjualan(conn, penjualan):
    """Menambahkan data penjualan baru ke database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO penjualan (pelanggan_id, tanggal_penjualan, keterangan) VALUES (%s, %s, %s) RETURNING id_penjualan",
            (penjualan.tanggal_penjualan, penjualan.pelanggan_id, penjualan.keterangan)
        )
        penjualan_id = cursor.fetchone()[0]
        conn.commit()
        return penjualan_id
    except psycopg2.Error as e:
        print(f"Error menambahkan penjualan: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()

def get_all_penjualan(conn):
    """Mengambil semua data penjualan dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM penjualan")
        rows = cursor.fetchall()
        penjualan_list = []
        for row in rows:
            penjualan = Penjualan(row[0], row[1], row[2], row[3])
            penjualan_list.append(penjualan)
        return penjualan_list
    except psycopg2.Error as e:
        print(f"Error mengambil data penjualan: {e}")
        return None
    finally:
        cursor.close()

def get_penjualan(conn, id_penjualan):
    """Mengambil data penjualan berdasarkan id_penjualan."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM penjualan WHERE id_penjualan = %s", (id_penjualan,))
        row = cursor.fetchone()
        if row:
            penjualan = Penjualan(row[0], row[1], row[2], row[3])
            return penjualan
        else:
            print("Penjualan tidak ditemukan.")
            return None
    except psycopg2.Error as e:
        print(f"Error mengambil data penjualan: {e}")
        return None
    finally:
        cursor.close()

def update_penjualan(conn, penjualan):
    """Memperbarui data penjualan di database."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE penjualan SET tanggal_penjualan = %s, pelanggan_id = %s, keterangan = %s WHERE id_penjualan = %s",
            (penjualan.tanggal_penjualan, penjualan.pelanggan_id, penjualan.keterangan, penjualan.id_penjualan)
        )
        conn.commit()
        print("Data penjualan berhasil diperbarui.")
    except psycopg2.Error as e:
        print(f"Error memperbarui penjualan: {e}")
        conn.rollback()
    finally:
        cursor.close()

def delete_penjualan(conn, id_penjualan):
    """Menghapus data penjualan dari database."""
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM penjualan WHERE id_penjualan = %s", (id_penjualan,))
        conn.commit()
        print("Data penjualan berhasil dihapus.")
    except psycopg2.Error as e:
        print(f"Error menghapus penjualan: {e}")
        conn.rollback()
    finally:
        cursor.close()
