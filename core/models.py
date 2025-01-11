from datetime import datetime

class Kategori:
    def __init__(self, id_kategori, nama_kategori):
        self.id_kategori = id_kategori
        self.nama_kategori = nama_kategori

class Barang:
    def __init__(self, id_barang, kode_barang, nama_barang, deskripsi, kategori_id, satuan):
        self.id_barang = id_barang
        self.kode_barang = kode_barang
        self.nama_barang = nama_barang
        self.deskripsi = deskripsi
        self.kategori_id = kategori_id
        self.satuan = satuan

class Varian:
    def __init__(self, id_varian, barang_id, nama_varian, nilai_varian, sku):
        self.id_varian = id_varian
        self.barang_id = barang_id
        self.nama_varian = nama_varian
        self.nilai_varian = nilai_varian
        self.sku = sku # Pastikan untuk menambahkan atribut sku

class Supplier:
    def __init__(self, id_supplier, nama_supplier, kontak, alamat):
        self.id_supplier = id_supplier
        self.nama_supplier = nama_supplier
        self.kontak = kontak
        self.alamat = alamat

class Gudang:
    def __init__(self, id_gudang, nama_gudang, alamat_gudang):
        self.id_gudang = id_gudang
        self.nama_gudang = nama_gudang
        self.alamat_gudang = alamat_gudang

class Rak:
    def __init__(self, id_rak, gudang_id, kode_rak):
        self.id_rak = id_rak
        self.gudang_id = gudang_id
        self.kode_rak = kode_rak

class Pelanggan:
    def __init__(self, id_pelanggan, nama_pelanggan, kontak, alamat):
        self.id_pelanggan = id_pelanggan
        self.nama_pelanggan = nama_pelanggan
        self.kontak = kontak
        self.alamat = alamat

class Pembelian:
    def __init__(self, id_pembelian, supplier_id, tanggal_pembelian, keterangan):
        self.id_pembelian = id_pembelian
        self.supplier_id = supplier_id
        self.tanggal_pembelian = tanggal_pembelian
        self.keterangan = keterangan

class Penjualan:
    def __init__(self, id_penjualan, pelanggan_id, tanggal_penjualan, keterangan):
        self.id_penjualan = id_penjualan
        self.tanggal_penjualan = tanggal_penjualan
        self.pelanggan_id = pelanggan_id
        self.keterangan = keterangan
