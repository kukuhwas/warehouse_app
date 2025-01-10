import pytest
from core.database import (
    connect_to_db,
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
    generate_kode_barang,
    create_varian,
    get_all_varian,
    get_varian,
    update_varian,
    delete_varian,
    get_varian_by_barang_id,
    get_varian_by_nilai_varian,
    generate_sku,
)
from core.models import Kategori, Barang, Varian

class TestKategori:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        # Setup: Bersihkan data kategori sebelum setiap test
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM kategori")
        db_connection.commit()
        cursor.close()
        yield  # Lanjut ke test case
        # Teardown: Tidak perlu teardown khusus untuk saat ini

    def test_create_kategori(self, db_connection):
        new_kategori = Kategori("Z", "Kategori Test")
        create_kategori(db_connection, new_kategori)
        retrieved_kategori = get_kategori(db_connection, "Z")
        assert retrieved_kategori is not None
        assert retrieved_kategori.id_kategori == "Z"
        assert retrieved_kategori.nama_kategori == "Kategori Test"

    def test_get_all_kategori(self, db_connection):
        kategori1 = Kategori("X", "Kategori X")
        kategori2 = Kategori("Y", "Kategori Y")
        create_kategori(db_connection, kategori1)
        create_kategori(db_connection, kategori2)

        kategori_list = get_all_kategori(db_connection)
        assert len(kategori_list) == 2
        assert kategori_list[0].id_kategori == "X"
        assert kategori_list[1].id_kategori == "Y"

    def test_get_kategori_not_found(self, db_connection):
        kategori = get_kategori(db_connection, "XXX")
        assert kategori is None

    def test_update_kategori(self, db_connection):
        kategori = Kategori("W", "Kategori Update")
        create_kategori(db_connection, kategori)

        kategori.nama_kategori = "Kategori Update - Updated"
        update_kategori(db_connection, kategori)

        retrieved_kategori = get_kategori(db_connection, "W")
        assert retrieved_kategori is not None
        assert retrieved_kategori.nama_kategori == "Kategori Update - Updated"

    def test_delete_kategori(self, db_connection):
        kategori = Kategori("V", "Kategori Delete")
        create_kategori(db_connection, kategori)

        delete_kategori(db_connection, "V")

        retrieved_kategori = get_kategori(db_connection, "V")
        assert retrieved_kategori is None

class TestBarang:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        # Setup: Bersihkan data sebelum setiap test
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM barang")
        cursor.execute("DELETE FROM kategori")
        db_connection.commit()
        cursor.close()
        # Isi data kategori yang diperlukan
        kategori = Kategori('A', 'Kategori A')
        create_kategori(db_connection, kategori)

        yield # Lanjut ke test case

        # Teardown: Tidak perlu teardown khusus untuk saat ini

    def test_create_barang(self, db_connection):
        new_barang = Barang(None, None, "Laptop Test", "Laptop untuk testing", "A", "pcs")
        barang_id = create_barang(db_connection, new_barang)
        assert barang_id is not None

        retrieved_barang = get_barang(db_connection, barang_id)
        assert retrieved_barang is not None
        assert retrieved_barang.nama_barang == "Laptop Test"

    def test_generate_kode_barang(self, db_connection):
        kode_barang = generate_kode_barang(db_connection, "A")
        assert kode_barang is not None
        assert len(kode_barang) == 5  # Pastikan panjang kode barang sesuai
        assert kode_barang[0] == "A"  # Pastikan prefix kategori benar

    def test_get_all_barang(self, db_connection):
        barang1 = Barang(None, None, "Barang Test 1", "Deskripsi 1", "A", "pcs")
        barang2 = Barang(None, None, "Barang Test 2", "Deskripsi 2", "A", "pcs")
        create_barang(db_connection, barang1)
        create_barang(db_connection, barang2)

        barang_list = get_all_barang(db_connection)
        assert len(barang_list) >= 2

    def test_get_barang_not_found(self, db_connection):
        barang = get_barang(db_connection, 99999)  # ID yang tidak mungkin ada
        assert barang is None

    def test_update_barang(self, db_connection):
        barang = Barang(None, None, "Barang Update", "Deskripsi Update", "A", "pcs")
        barang_id = create_barang(db_connection, barang)
        barang = get_barang(db_connection, barang_id)
        
        barang.nama_barang = "Barang Update - Updated"
        update_barang(db_connection, barang)

        retrieved_barang = get_barang(db_connection, barang_id)
        assert retrieved_barang is not None
        assert retrieved_barang.nama_barang == "Barang Update - Updated"

    def test_delete_barang(self, db_connection):
        barang = Barang(None, None, "Barang Delete", "Deskripsi Delete", "A", "pcs")
        barang_id = create_barang(db_connection, barang)

        delete_barang(db_connection, barang_id)

        retrieved_barang = get_barang(db_connection, barang_id)
        assert retrieved_barang is None

class TestVarian:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        # Setup: Bersihkan data sebelum setiap test
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM varian")
        cursor.execute("DELETE FROM barang")
        cursor.execute("DELETE FROM kategori")
        db_connection.commit()
        cursor.close()

        # Isi data kategori dan barang yang diperlukan
        kategori = Kategori("A", "Kategori A")
        create_kategori(db_connection, kategori)
        barang = Barang(
            None,
            generate_kode_barang(db_connection, kategori.id_kategori),
            "Barang Test",
            "Deskripsi Barang Test",
            kategori.id_kategori,
            "pcs",
        )
        barang.id_barang = create_barang(db_connection, barang)

        self.barang_id = barang.id_barang
        self.kategori_id = kategori.id_kategori
        yield  # Lanjut ke test case
        # Teardown: Tidak perlu teardown khusus untuk saat ini

    def test_create_varian(self, db_connection):
        new_varian = Varian(None, self.barang_id, "Warna", "Merah", None)
        varian_id = create_varian(db_connection, new_varian)
        assert varian_id is not None

        retrieved_varian = get_varian(db_connection, varian_id)
        assert retrieved_varian is not None
        assert retrieved_varian.nama_varian == "Warna"
        # Tambahkan assertion untuk memeriksa SKU
        assert retrieved_varian.sku is not None
        assert len(retrieved_varian.sku) == 14  # format: PP-VVV-YYMM-UU

    def test_get_all_varian(self, db_connection):
        varian1 = Varian(None, self.barang_id, "Warna", "Merah", None)
        varian2 = Varian(None, self.barang_id, "Warna", "Biru", None)
        create_varian(db_connection, varian1)
        create_varian(db_connection, varian2)

        varian_list = get_all_varian(db_connection)
        assert len(varian_list) == 2

    def test_get_varian_not_found(self, db_connection):
        varian = get_varian(db_connection, 9999)
        assert varian is None

    def test_update_varian(self, db_connection):
        varian = Varian(None, self.barang_id, "Warna", "Merah", None)
        varian_id = create_varian(db_connection, varian)

        varian = get_varian(db_connection, varian_id)
        varian.nilai_varian = "Hijau"  # Update hanya nilai varian, nama varian tetap "Warna"
        update_varian(db_connection, varian)

        retrieved_varian = get_varian(db_connection, varian_id)
        assert retrieved_varian is not None
        assert retrieved_varian.nama_varian == "Warna"
        assert retrieved_varian.nilai_varian == "Hijau"

    def test_delete_varian(self, db_connection):
        varian = Varian(None, self.barang_id, "Warna", "Merah", None)
        varian_id = create_varian(db_connection, varian)

        delete_varian(db_connection, varian_id)

        retrieved_varian = get_varian(db_connection, varian_id)
        assert retrieved_varian is None

    def test_generate_sku(self, db_connection):
        sku = generate_sku(db_connection, self.barang_id, "WARNA", "MERAH")
        assert sku is not None
        assert len(sku) == 14
        assert sku[2] == "-"  # Cek format: PP-VVV-YYMM-UU
        assert sku[6] == "-"
        assert sku[11] == "-"

    def test_generate_sku_short_values(self, db_connection):
        sku = generate_sku(db_connection, self.barang_id, "W", "M")
        assert sku is not None
        assert len(sku) == 14
        assert sku[2] == "-"
        assert sku[6] == "-"
        assert sku[11] == "-"

    def test_generate_sku_long_values(self, db_connection):
        sku = generate_sku(
            db_connection, self.barang_id, "WARNA PANJANG", "MERAH DAN MOTIF"
        )
        assert sku is not None
        assert len(sku) == 14
        assert sku[2] == "-"
        assert sku[6] == "-"
        assert sku[11] == "-"

    def test_get_varian_by_barang_id(self, db_connection):
        varian1 = Varian(None, self.barang_id, "Warna", "Merah", None)
        varian2 = Varian(None, self.barang_id, "Warna", "Biru", None)
        create_varian(db_connection, varian1)
        create_varian(db_connection, varian2)

        varian_list = get_varian_by_barang_id(db_connection, self.barang_id)
        assert len(varian_list) == 2

    def test_get_varian_by_nilai_varian(self, db_connection):
        varian1 = Varian(None, self.barang_id, "Warna", "Merah", None)
        create_varian(db_connection, varian1)

        retrieved_varian = get_varian_by_nilai_varian(
            db_connection, self.barang_id, "Warna", "Merah"
        )
        assert retrieved_varian is not None
        assert retrieved_varian.nilai_varian == "Merah"

    def test_get_varian_by_nilai_varian_not_found(self, db_connection):
        varian = get_varian_by_nilai_varian(
            db_connection, self.barang_id, "Warna", "Hijau"
        )
        assert varian is None
