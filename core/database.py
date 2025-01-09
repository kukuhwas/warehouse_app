import psycopg2
import configparser
from core.models import Kategori  # Tambahkan baris ini


def load_config(filepath="data/config.ini"):
    """Memuat konfigurasi database dari file config.ini."""
    config = configparser.ConfigParser()
    config.read(filepath)
    return config['database']

def connect_to_db():
    """Membuat koneksi ke database PostgreSQL."""
    db_config = load_config()
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        print("Berhasil koneksi ke database!")
        return conn
    except psycopg2.Error as e:
        print(f"Error koneksi ke database: {e}")
        return None
    
def create_kategori(conn, kategori):
    """Menambahkan data kategori baru ke database."""
    cursor = conn.cursor()
    try:
        # Cek apakah kategori dengan ID tersebut sudah ada
        cursor.execute("SELECT COUNT(*) FROM kategori WHERE id_kategori = %s", (kategori.id_kategori,))
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"Error: Kategori dengan ID {kategori.id_kategori} sudah ada.")
            return None

        # Cek apakah jumlah kategori sudah mencapai batas maksimal
        cursor.execute("SELECT COUNT(*) FROM kategori")
        count = cursor.fetchone()[0]
        if count >= 5:
            print("Error: Jumlah kategori sudah mencapai batas maksimal (5).")
            return None

        # Jika belum ada dan belum mencapai batas maksimal, tambahkan kategori baru
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
            kategori = Kategori(row[0], row[1])  # Asumsikan Anda sudah punya class Kategori di core/models.py
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
            kategori = Kategori(row[0], row[1]) # Asumsikan Anda sudah punya class Kategori di core/models.py
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
