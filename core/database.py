import psycopg2
import configparser
import uuid
from core.models import Kategori, Barang
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

def get_varian_by_barang_id(conn, barang_id):
    """Mengambil data varian berdasarkan barang_id.
       Karena sekarang nama_varian selalu 'Warna', fungsi ini tetap berguna
       untuk menampilkan semua varian (warna) dari suatu barang.
    """
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM varian WHERE barang_id = %s", (barang_id,))
        rows = cursor.fetchall()
        varian_list = []
        for row in rows:
            varian = Varian(row[0], row[1], row[2], row[3], row[4])
            varian_list.append(varian)
        return varian_list
    except psycopg2.Error as e:
        print(f"Error mengambil data varian: {e}")
        return None
    finally:
        cursor.close()

def get_varian_by_nilai_varian(conn, barang_id, nilai_varian):
    """Mengambil data varian berdasarkan barang_id dan nilai_varian (warna)."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM varian WHERE barang_id = %s AND nilai_varian = %s", (barang_id, nilai_varian))
        row = cursor.fetchone()
        if row:
            varian = Varian(row[0], row[1], row[2], row[3], row[4])
            return varian
        else:
            print("Varian tidak ditemukan.")
            return None
    except psycopg2.Error as e:
        print(f"Error mengambil data varian: {e}")
        return None
    finally:
        cursor.close()



