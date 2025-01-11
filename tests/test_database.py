import pytest
from datetime import datetime
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
    get_varian,
    get_all_varian,
    update_varian,
    delete_varian,
    get_varian_by_barang_id,
    get_varian_by_nilai_varian,
    generate_sku,
    create_supplier,
    get_all_suppliers,
    get_supplier,
    update_supplier,
    delete_supplier,
    create_gudang,
    get_all_gudang,
    get_gudang,
    update_gudang,
    delete_gudang,
    create_rak,
    get_rak,
    get_all_rak,
    update_rak,
    delete_rak,
    create_pelanggan,
    get_all_pelanggan,
    get_pelanggan,
    update_pelanggan,
    delete_pelanggan,
    create_pembelian,
    get_all_pembelian,
    get_pembelian,
    update_pembelian,
    delete_pembelian,
    create_penjualan,
    get_all_penjualan,
    get_penjualan,
    update_penjualan,
    delete_penjualan,

)
from core.models import Kategori, Barang, Varian, Supplier, Gudang, Rak, Pelanggan, Pembelian, Penjualan

class TestKategori:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        # Setup: Bersihkan data kategori sebelum setiap test
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM varian")
        cursor.execute("DELETE FROM barang")
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
        cursor = db_connection.cursor()

        try:
            # Hapus data dari tabel yang bergantung terlebih dahulu
            cursor.execute("DELETE FROM varian")
            cursor.execute("DELETE FROM barang")
            cursor.execute("DELETE FROM kategori")
            db_connection.commit()

            # Isi data kategori yang diperlukan untuk pengujian
            kategori = Kategori('A', 'Kategori A')
            create_kategori(db_connection, kategori)

            # Lanjut ke test case
            yield
        except Exception as e:
            db_connection.rollback()
            raise e
        finally:
            cursor.close()

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
        barang = get_barang(db_connection, 99999)
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
        cursor = db_connection.cursor()
        try:
            # Hapus data dari tabel yang bergantung terlebih dahulu
            cursor.execute("DELETE FROM varian")
            cursor.execute("DELETE FROM barang")
            cursor.execute("DELETE FROM kategori")
            db_connection.commit()

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
            yield
        except Exception as e:
            db_connection.rollback()
            raise e
        finally:
            cursor.close()

    def test_generate_sku(self, db_connection):
        sku = generate_sku(db_connection, self.barang_id, "WARNA", "MERAH")
        assert sku is not None
        assert len(sku) == 14
        assert sku[2] == "-"
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

    def test_create_varian(self, db_connection):
        new_varian = Varian(None, self.barang_id, "Warna", "Merah", None)
        varian_id = create_varian(db_connection, new_varian)
        assert varian_id is not None

        retrieved_varian = get_varian(db_connection, varian_id)
        assert retrieved_varian is not None
        assert retrieved_varian.nama_varian == "Warna"
        assert retrieved_varian.sku is not None
        assert len(retrieved_varian.sku) == 14

    def test_get_all_varian(self, db_connection):
        varian1 = Varian(None, self.barang_id, "Warna", "Merah", None)
        varian2 = Varian(None, self.barang_id, "Warna", "Biru", None)
        create_varian(db_connection, varian1)
        create_varian(db_connection, varian2)

        varian_list = get_all_varian(db_connection)
        assert len(varian_list) == 2

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
            db_connection, self.barang_id, "Merah"
        )
        assert retrieved_varian is not None
        assert retrieved_varian.nilai_varian == "Merah"

    def test_get_varian_by_nilai_varian_not_found(self, db_connection):
        varian = get_varian_by_nilai_varian(
            db_connection, self.barang_id, "Hijau"
        )
        assert varian is None

    def test_update_varian(self, db_connection):
        varian = Varian(None, self.barang_id, "Warna", "Merah", None)
        varian_id = create_varian(db_connection, varian)

        varian = get_varian(db_connection, varian_id)
        varian.nilai_varian = "Hijau"
        is_update_success = update_varian(db_connection, varian)
        assert is_update_success == True

        retrieved_varian = get_varian(db_connection, varian_id)
        assert retrieved_varian is not None
        assert retrieved_varian.nama_varian == "Warna"
        assert retrieved_varian.nilai_varian == "Hijau"

    def test_delete_varian(self, db_connection):
        varian = Varian(None, self.barang_id, "Warna", "Merah", None)
        varian_id = create_varian(db_connection, varian)

        is_delete_success = delete_varian(db_connection, varian_id)
        assert is_delete_success == True

        retrieved_varian = get_varian(db_connection, varian_id)
        assert retrieved_varian is None

class TestSupplier:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM supplier")
        db_connection.commit()
        cursor.close()
        yield

    def test_create_supplier(self, db_connection):
        new_supplier = Supplier(None, "Supplier Test", "Alamat Test", "08123456789")
        supplier_id = create_supplier(db_connection, new_supplier)
        assert supplier_id is not None

        retrieved_supplier = get_supplier(db_connection, supplier_id)
        assert retrieved_supplier is not None
        assert retrieved_supplier.nama_supplier == "Supplier Test"

    def test_get_all_suppliers(self, db_connection):
        supplier1 = Supplier(None, "Supplier 1", "Alamat 1", "08123456781")
        supplier2 = Supplier(None, "Supplier 2", "Alamat 2", "08123456782")
        create_supplier(db_connection, supplier1)
        create_supplier(db_connection, supplier2)

        supplier_list = get_all_suppliers(db_connection)
        assert len(supplier_list) == 2

    def test_get_supplier_not_found(self, db_connection):
        supplier = get_supplier(db_connection, 99999)
        assert supplier is None

    def test_update_supplier(self, db_connection):
        supplier = Supplier(None, "Supplier Update", "Alamat Update", "08123456780")
        supplier_id = create_supplier(db_connection, supplier)

        supplier = get_supplier(db_connection, supplier_id)
        supplier.nama_supplier = "Supplier Updated"
        update_supplier(db_connection, supplier)

        retrieved_supplier = get_supplier(db_connection, supplier_id)
        assert retrieved_supplier is not None
        assert retrieved_supplier.nama_supplier == "Supplier Updated"

    def test_delete_supplier(self, db_connection):
        supplier = Supplier(None, "Supplier Delete", "Alamat Delete", "08123456788")
        supplier_id = create_supplier(db_connection, supplier)

        delete_supplier(db_connection, supplier_id)

        retrieved_supplier = get_supplier(db_connection, supplier_id)
        assert retrieved_supplier is None

class TestGudang:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM gudang")
        db_connection.commit()
        cursor.close()
        yield

    def test_create_gudang(self, db_connection):
        new_gudang = Gudang(None, "Gudang Test", "Alamat Gudang Test")
        gudang_id = create_gudang(db_connection, new_gudang)
        assert gudang_id is not None

        retrieved_gudang = get_gudang(db_connection, gudang_id)
        assert retrieved_gudang is not None
        assert retrieved_gudang.nama_gudang == "Gudang Test"

    def test_get_all_gudang(self, db_connection):
        gudang1 = Gudang(None, "Gudang 1", "Alamat 1")
        gudang2 = Gudang(None, "Gudang 2", "Alamat 2")
        create_gudang(db_connection, gudang1)
        create_gudang(db_connection, gudang2)

        gudang_list = get_all_gudang(db_connection)
        assert len(gudang_list) == 2

    def test_get_gudang_not_found(self, db_connection):
        gudang = get_gudang(db_connection, 99999)
        assert gudang is None

    def test_update_gudang(self, db_connection):
        gudang = Gudang(None, "Gudang Update", "Alamat Update")
        gudang_id = create_gudang(db_connection, gudang)

        gudang = get_gudang(db_connection, gudang_id)
        gudang.nama_gudang = "Gudang Updated"
        update_gudang(db_connection, gudang)

        retrieved_gudang = get_gudang(db_connection, gudang_id)
        assert retrieved_gudang is not None
        assert retrieved_gudang.nama_gudang == "Gudang Updated"

    def test_delete_gudang(self, db_connection):
        gudang = Gudang(None, "Gudang Delete", "Alamat Delete")
        gudang_id = create_gudang(db_connection, gudang)

        delete_gudang(db_connection, gudang_id)

        retrieved_gudang = get_gudang(db_connection, gudang_id)
        assert retrieved_gudang is None

class TestRak:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM rak")
        cursor.execute("DELETE FROM gudang")
        db_connection.commit()
        cursor.close()
        yield

    def test_create_rak(self, db_connection):
        new_gudang = Gudang(None, "Gudang Test", "Alamat Gudang Test")
        gudang_id = create_gudang(db_connection, new_gudang)
        assert gudang_id is not None

        new_rak = Rak(None, gudang_id, "Rak001")
        rak_id = create_rak(db_connection, new_rak)
        assert rak_id is not None

        retrieved_rak = get_rak(db_connection, rak_id)
        assert retrieved_rak is not None
        assert retrieved_rak.kode_rak == "Rak001"

    def test_get_all_rak(self, db_connection):
        new_gudang = Gudang(None, "Gudang Test", "Alamat Gudang Test")
        gudang_id = create_gudang(db_connection, new_gudang)
        assert gudang_id is not None

        rak1 = Rak(None, gudang_id, "Rak 1")
        rak2 = Rak(None, gudang_id, "Rak 2")
        create_rak(db_connection, rak1)
        create_rak(db_connection, rak2)

        rak_list = get_all_rak(db_connection)
        assert len(rak_list) == 2

    def test_get_rak_not_found(self, db_connection):
        rak = get_rak(db_connection, 99999)
        assert rak is None

    def test_update_rak(self, db_connection):
        new_gudang = Gudang(None, "Gudang Test", "Alamat Gudang Test")
        gudang_id = create_gudang(db_connection, new_gudang)
        assert gudang_id is not None

        rak = Rak(None, gudang_id, "Rak 1 Update")
        rak_id = create_rak(db_connection, rak)

        rak = get_rak(db_connection, rak_id)
        rak.kode_rak = "Rak 1 Updated"
        update_rak(db_connection, rak)

        retrieved_rak = get_rak(db_connection, rak_id)
        assert retrieved_rak is not None
        assert retrieved_rak.kode_rak == "Rak 1 Updated"

    def test_delete_rak(self, db_connection):
        new_gudang = Gudang(None, "Gudang Test", "Alamat Gudang Test")
        gudang_id = create_gudang(db_connection, new_gudang)
        assert gudang_id is not None

        rak = Rak(None, gudang_id, "Rak Delete")
        rak_id = create_rak(db_connection, rak)

        delete_rak(db_connection, rak_id)

        retrieved_rak = get_rak(db_connection, rak_id)
        assert retrieved_rak is None

class TestPelanggan:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM pelanggan")
        db_connection.commit()
        cursor.close()
        yield

    def test_create_pelanggan(self, db_connection):
        new_pelanggan = Pelanggan(None, "Pelanggan Test", "08123456789", "Alamat Pelanggan Test")
        pelanggan_id = create_pelanggan(db_connection, new_pelanggan)
        assert pelanggan_id is not None

        retrieved_pelanggan = get_pelanggan(db_connection, pelanggan_id)
        assert retrieved_pelanggan is not None
        assert retrieved_pelanggan.nama_pelanggan == "Pelanggan Test"

    def test_get_all_pelanggan(self, db_connection):
        pelanggan1 = Pelanggan(None, "Pelanggan 1", "08123456781", "Alamat 1")
        pelanggan2 = Pelanggan(None, "Pelanggan 2", "08123456782", "Alamat 2")
        create_pelanggan(db_connection, pelanggan1)
        create_pelanggan(db_connection, pelanggan2)

        pelanggan_list = get_all_pelanggan(db_connection)
        assert len(pelanggan_list) == 2

    def test_get_pelanggan_not_found(self, db_connection):
        pelanggan = get_pelanggan(db_connection, 99999)
        assert pelanggan is None

    def test_update_pelanggan(self, db_connection):
        pelanggan = Pelanggan(None, "Pelanggan Update", "08123456780", "Alamat Update")
        pelanggan_id = create_pelanggan(db_connection, pelanggan)

        pelanggan = get_pelanggan(db_connection, pelanggan_id)
        pelanggan.nama_pelanggan = "Pelanggan Updated"
        update_pelanggan(db_connection, pelanggan)

        retrieved_pelanggan = get_pelanggan(db_connection, pelanggan_id)
        assert retrieved_pelanggan is not None
        assert retrieved_pelanggan.nama_pelanggan == "Pelanggan Updated"

    def test_delete_pelanggan(self, db_connection):
        pelanggan = Pelanggan(None, "Pelanggan Delete", "08123456788", "Alamat Delete")
        pelanggan_id = create_pelanggan(db_connection, pelanggan)

        delete_pelanggan(db_connection, pelanggan_id)

        retrieved_pelanggan = get_pelanggan(db_connection, pelanggan_id)
        assert retrieved_pelanggan is None

class TestPembelian:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM pembelian")
        db_connection.commit()
        cursor.close()
        yield

    def test_create_pembelian(self, db_connection):
        new_supplier = Supplier(None, "Supplier Test", "Alamat Supplier Test", "08123456789")
        supplier_id = create_supplier(db_connection, new_supplier)
        assert supplier_id is not None

        new_pembelian = Pembelian(None, supplier_id, datetime(2023, 10, 1), "Keterangan Test")
        pembelian_id = create_pembelian(db_connection, new_pembelian)
        assert pembelian_id is not None

        retrieved_pembelian = get_pembelian(db_connection, pembelian_id)
        expected_date = datetime(2023, 10, 1)
        assert retrieved_pembelian is not None
        assert retrieved_pembelian.tanggal_pembelian == expected_date
        assert retrieved_pembelian.keterangan == "Keterangan Test"

    def test_get_all_pembelian(self, db_connection):
        new_supplier = Supplier(None, "Supplier Test", "Alamat Supplier Test", "08123456789")
        supplier_id = create_supplier(db_connection, new_supplier)
        assert supplier_id is not None

        pembelian1 = Pembelian(None, supplier_id, datetime(2023, 10, 1), "Keterangan 1")
        pembelian2 = Pembelian(None, supplier_id, datetime(2023, 10, 2), "Keterangan 2")
        create_pembelian(db_connection, pembelian1)
        create_pembelian(db_connection, pembelian2)

        pembelian_list = get_all_pembelian(db_connection)
        assert len(pembelian_list) == 2

    def test_get_pembelian_not_found(self, db_connection):
        pembelian = get_pembelian(db_connection, 99999)
        assert pembelian is None

    def test_update_pembelian(self, db_connection):
        new_supplier = Supplier(None, "Supplier Test", "Alamat Supplier Test", "08123456789")
        supplier_id = create_supplier(db_connection, new_supplier)
        assert supplier_id is not None

        pembelian = Pembelian(None, supplier_id, datetime(2023, 10, 1), "Keterangan Update")
        pembelian_id = create_pembelian(db_connection, pembelian)

        pembelian = get_pembelian(db_connection, pembelian_id)
        pembelian.tanggal_pembelian = datetime(2023, 10, 2)
        pembelian.keterangan = "Keterangan Updated"
        update_pembelian(db_connection, pembelian)

        retrieved_pembelian = get_pembelian(db_connection, pembelian_id)
        expected_date = datetime(2023, 10, 2)
        assert retrieved_pembelian is not None
        assert retrieved_pembelian.tanggal_pembelian == expected_date
        assert retrieved_pembelian.keterangan == "Keterangan Updated"

    def test_delete_pembelian(self, db_connection):
        new_supplier = Supplier(None, "Supplier Test", "Alamat Supplier Test", "08123456789")
        supplier_id = create_supplier(db_connection, new_supplier)
        assert supplier_id is not None

        pembelian = Pembelian(None, datetime(2023, 10, 1), supplier_id, "Keterangan Delete")
        pembelian_id = create_pembelian(db_connection, pembelian)

        delete_pembelian(db_connection, pembelian_id)

        retrieved_pembelian = get_pembelian(db_connection, pembelian_id)
        assert retrieved_pembelian is None

class TestPenjualan:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM penjualan")
        db_connection.commit()
        cursor.close()
        yield

    def test_create_penjualan(self, db_connection):
        new_pelanggan = Pelanggan(None, "Pelanggan Test", "08123456789", "Alamat Pelanggan Test")
        pelanggan_id = create_pelanggan(db_connection, new_pelanggan)
        assert pelanggan_id is not None

        new_penjualan = Penjualan(None, datetime(2023, 10, 1), pelanggan_id, "Keterangan Test")
        penjualan_id = create_penjualan(db_connection, new_penjualan)
        assert penjualan_id is not None

        retrieved_penjualan = get_penjualan(db_connection, penjualan_id)
        expected_date = datetime(2023, 10, 1)
        assert retrieved_penjualan is not None
        assert retrieved_penjualan.tanggal_penjualan == expected_date
        assert retrieved_penjualan.keterangan == "Keterangan Test"

    def test_get_all_penjualan(self, db_connection):
        new_pelanggan = Pelanggan(None, "Pelanggan Test", "08123456789", "Alamat Pelanggan Test")
        pelanggan_id = create_pelanggan(db_connection, new_pelanggan)
        assert pelanggan_id is not None

        penjualan1 = Penjualan(None, datetime(2023, 10, 1), pelanggan_id, "Keterangan 1")
        penjualan2 = Penjualan(None, datetime(2023, 10, 2), pelanggan_id, "Keterangan 2")
        create_penjualan(db_connection, penjualan1)
        create_penjualan(db_connection, penjualan2)

        penjualan_list = get_all_penjualan(db_connection)
        assert len(penjualan_list) == 2

    def test_get_penjualan_not_found(self, db_connection):
        penjualan = get_penjualan(db_connection, 99999)
        assert penjualan is None

    def test_update_penjualan(self, db_connection):
        new_pelanggan = Pelanggan(None, "Pelanggan Test", "08123456789", "Alamat Pelanggan Test")
        pelanggan_id = create_pelanggan(db_connection, new_pelanggan)
        assert pelanggan_id is not None

        penjualan = Penjualan(None, datetime(2023, 10, 1), pelanggan_id, "Keterangan Update")
        penjualan_id = create_penjualan(db_connection, penjualan)

        penjualan = get_penjualan(db_connection, penjualan_id)
        penjualan.tanggal_penjualan = datetime(2023, 10, 2)
        penjualan.keterangan = "Keterangan Updated"
        update_penjualan(db_connection, penjualan)

        retrieved_penjualan = get_penjualan(db_connection, penjualan_id)
        assert retrieved_penjualan is not None
        assert retrieved_penjualan.tanggal_penjualan == datetime(2023, 10, 2)
        assert retrieved_penjualan.keterangan == "Keterangan Updated"

    def test_delete_penjualan(self, db_connection):
        new_pelanggan = Pelanggan(None, "Pelanggan Test", "08123456789", "Alamat Pelanggan Test")
        pelanggan_id = create_pelanggan(db_connection, new_pelanggan)
        assert pelanggan_id is not None

        penjualan = Penjualan(None, datetime(2023, 10, 1), pelanggan_id, "Keterangan Delete")
        penjualan_id = create_penjualan(db_connection, penjualan)

        delete_penjualan(db_connection, penjualan_id)

        retrieved_penjualan = get_penjualan(db_connection, penjualan_id)
        assert retrieved_penjualan is None
