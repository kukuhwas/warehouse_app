from core.database import connect_to_db, create_kategori, get_all_kategori, get_kategori, update_kategori, delete_kategori
from core.models import Kategori

if __name__ == "__main__":
    conn = connect_to_db()

    if conn:
        # Contoh penggunaan fungsi-fungsi CRUD untuk tabel kategori
        # 1. Menambahkan kategori baru
        kategori_baru = Kategori('X', 'Kategori Baru')
        create_kategori(conn, kategori_baru)

        # 2. Mengambil semua kategori dan menampilkannya
        semua_kategori = get_all_kategori(conn)
        if semua_kategori:
            print("Semua Kategori:")
            for kat in semua_kategori:
                print(f"  ID: {kat.id_kategori}, Nama: {kat.nama_kategori}")

        # 3. Mengambil satu kategori berdasarkan ID
        kategori_x = get_kategori(conn, 'X')
        if kategori_x:
            print(f"\nKategori dengan ID X: {kategori_x.nama_kategori}")

            # 4. Memperbarui kategori
            kategori_x.nama_kategori = 'Kategori X Diperbarui'
            update_kategori(conn, kategori_x)

            # Cek perubahan
            kategori_x_updated = get_kategori(conn, 'X')
            if kategori_x_updated:
                print(f"Kategori dengan ID X setelah diperbarui: {kategori_x_updated.nama_kategori}")

        # 5. Menghapus kategori
        # delete_kategori(conn, 'X')

        # Cek apakah kategori sudah terhapus
        # kategori_x_deleted = get_kategori(conn, 'X')
        # if kategori_x_deleted is None:
        #     print("\nKategori dengan ID X berhasil dihapus.")

        # Menutup koneksi
        conn.close()
    else:
        print("Koneksi ke database gagal.")
