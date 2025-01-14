import pytest
from core.database import (
    create_kategori, 
    get_all_kategori, 
    get_kategori,
    update_kategori,
    delete_kategori,
    create_barang, 
    get_all_barang, 
    get_barang, 
    update_barang, 
    delete_barang,
    create_varian,
    get_varian,
    generate_sku,
)
from core.models import Kategori, Barang, Varian


class TestKategori:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        cursor = db_connection.cursor()
        try:
            # Hapus data dari tabel yang bergantung terlebih dahulu
            cursor.execute("DELETE FROM varian")
            cursor.execute("DELETE FROM barang")
            cursor.execute("DELETE FROM kategori")
            db_connection.commit()
            yield
        except Exception as e:
            db_connection.rollback()
            raise e
        finally:
            cursor.close()

    def test_create_kategori(self, db_connection):
        kategori = Kategori("A", "Kategori A")
        kategori_id = create_kategori(db_connection, kategori)
        assert kategori_id is not None

        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM kategori WHERE id_kategori = %s", (kategori_id,))
        result = cursor.fetchone()
        cursor.close()

        assert result is not None
        assert result[0] == kategori.id_kategori
        assert result[1] == kategori.nama_kategori

    def test_get_all_kategori(self, db_connection):
        kategori1 = Kategori("A", "Kategori A")
        kategori2 = Kategori("B", "Kategori B")
        create_kategori(db_connection, kategori1)
        create_kategori(db_connection, kategori2)

        kategori_list = get_all_kategori(db_connection)
        assert len(kategori_list) == 2
        assert kategori_list[0].id_kategori == "A"
        assert kategori_list[0].nama_kategori == "Kategori A"
        assert kategori_list[1].id_kategori == "B"
        assert kategori_list[1].nama_kategori == "Kategori B"

    def test_get_kategori(self, db_connection):
        # Membuat dan menyimpan kategori yang diperlukan
        kategori = Kategori("A", "Kategori A")
        id_kategori = create_kategori(db_connection, kategori)
        assert kategori is not None

        retrieved_kategori = get_kategori(db_connection, id_kategori)
        assert retrieved_kategori is not None
        assert retrieved_kategori.id_kategori == "A"
        assert retrieved_kategori.nama_kategori == "Kategori A"         

    def test_update_kategori(self, db_connection):
        kategori = Kategori("A", "Kategori A Updated")
        kategori_id = create_kategori(db_connection, kategori)
        assert kategori_id is not None

        kategori.id_kategori = kategori_id
        kategori.nama_kategori = "Kategori A Updated"
        update_kategori(db_connection, kategori)

        retrieved_kategori = get_kategori(db_connection, kategori_id)   
        assert retrieved_kategori is not None
        assert retrieved_kategori.id_kategori == "A"
        assert retrieved_kategori.nama_kategori == "Kategori A Updated"
        
    def test_delete_kategori(self, db_connection):
        kategori = Kategori("A", "Kategori A")
        kategori_id = create_kategori(db_connection, kategori)
        assert kategori_id == "A"

        delete_kategori(db_connection, kategori_id)
        deleted_kategori = get_kategori(db_connection, kategori_id)
        assert deleted_kategori is None
class TestBarang:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        cursor = db_connection.cursor()
        try:
            # Hapus data dari tabel yang bergantung terlebih dahulu
            cursor.execute("DELETE FROM varian")
            cursor.execute("DELETE FROM barang")
            cursor.execute("DELETE FROM kategori")
            db_connection.commit()

            # Isi data kategori yang diperlukan
            kategori = Kategori("A", "Kategori A")
            create_kategori(db_connection, kategori)
            self.kategori_id = kategori.id_kategori
            yield
        except Exception as e:
            db_connection.rollback()
            raise e
        finally:
            cursor.close()

    def test_create_barang(self, db_connection):
        barang = Barang(
            None, 
            None, 
            "Barang Test", 
            "Deskripsi Barang Test", 
            self.kategori_id, 
            "pcs"
        )
        barang_id, kode_barang = create_barang(db_connection, barang)
        assert barang_id is not None
        assert kode_barang is not None

        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM barang WHERE id_barang = %s", (barang_id,))
        result = cursor.fetchone()
        cursor.close()

        # Cetak hasil result untuk memastikan data yang diambil dari database
        print(f"Result: {result}")

        assert result is not None
        assert result[1] is not None
        assert result[2] == "Barang Test"
        assert result[3] == "Deskripsi Barang Test"
        assert result[4] == self.kategori_id
        assert result[5] == "pcs"

    def test_get_all_barang(self, db_connection):
        barang1 = Barang(None, None, "Barang Test 1", "Deskripsi Barang Test 1", self.kategori_id, "pcs")
        barang2 = Barang(None, None, "Barang Test 2", "Deskripsi Barang Test 2", self.kategori_id, "pcs")
        create_barang(db_connection, barang1)
        create_barang(db_connection, barang2)

        barang_list = get_all_barang(db_connection)
        assert len(barang_list) == 2
        assert barang_list[0].kode_barang is not None
        assert barang_list[0].nama_barang == "Barang Test 1"
        assert barang_list[1].kode_barang is not None
        assert barang_list[1].nama_barang == "Barang Test 2"

    def test_get_barang(self, db_connection):
        barang = Barang(None, None, "Barang Test", "Deskripsi Barang Test", self.kategori_id, "pcs")
        barang_id, kode_barang = create_barang(db_connection, barang)
        assert barang_id is not None
        assert kode_barang is not None

        retrieved_barang = get_barang(db_connection, barang_id)
        assert retrieved_barang is not None
        assert retrieved_barang.kode_barang is not None
        assert retrieved_barang.nama_barang == "Barang Test"

    def test_update_barang(self, db_connection):
        barang = Barang(None, None, "Barang Test", "Deskripsi Barang Test", self.kategori_id, "pcs")
        barang_id, kode_barang = create_barang(db_connection, barang)
        assert barang_id is not None
        assert kode_barang is not None

        # Set id_barang ke objek barang sebelum update
        barang.id_barang = barang_id
        barang.kode_barang = kode_barang
        barang.nama_barang = "Barang Test Updated"
        barang.deskripsi_barang = "Deskripsi Barang Test Updated"
        update_barang(db_connection, barang)

        retrieved_barang = get_barang(db_connection, barang_id)
        assert retrieved_barang is not None
        assert retrieved_barang.kode_barang is not None
        assert retrieved_barang.nama_barang == "Barang Test Updated"
        assert retrieved_barang.deskripsi_barang == "Deskripsi Barang Test Updated"

'''
    def test_delete_barang(self, db_connection):
        barang = Barang(None, None, "Barang Test", "Deskripsi Barang Test", self.kategori_id, "pcs")
        barang_id = create_barang(db_connection, barang)
        assert barang_id is not None

        delete_barang(db_connection, barang_id)

        retrieved_barang = get_barang(db_connection, barang_id)
        assert retrieved_barang is None
'''
class TestVarian:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        cursor = db_connection.cursor()
        try:
            # Hapus data
            cursor.execute("DELETE FROM varian")
            cursor.execute("DELETE FROM barang")
            cursor.execute("DELETE FROM kategori")
            db_connection.commit()

            # Isi data kategori dan barang
            kategori = Kategori("A", "Kategori A")
            create_kategori(db_connection, kategori)
            self.kategori_id = kategori.id_kategori

            barang = Barang(
                None,
                None,
                "Barang Test",
                "Deskripsi Barang Test",
                kategori.id_kategori,
                "pcs",
            )
            self.barang_id, self.kode_barang = create_barang(db_connection, barang)
            if self.barang_id is None or self.kode_barang is None:
                raise Exception("Gagal membuat data barang di setup_and_teardown")
            yield  # Lanjut ke test case
        except Exception as e:
            db_connection.rollback()
            print(f"Error di setup_and_teardown: {e}")
            raise e
        finally:
            cursor.close()
            db_connection.rollback()

    def test_create_varian(self, db_connection):
        # Panggil generate_sku untuk mendapatkan SKU
        sku = generate_sku(db_connection, self.kode_barang, "Merah")
        print(f"SKU yang dihasilkan: {sku}")
        assert sku is not None
        assert len(sku) == 14

        new_varian = Varian(
            None, 
            self.barang_id, 
            "Warna", 
            "Merah", 
            sku,
        )
        varian_id = create_varian(db_connection, new_varian)
        assert varian_id is not None

        retrieved_varian = get_varian(db_connection, varian_id)
        assert retrieved_varian is not None
        assert retrieved_varian.nama_varian == "Warna"
        assert retrieved_varian.nilai_varian == "Merah"
        assert retrieved_varian.sku == sku
        assert len(retrieved_varian.sku) == 14