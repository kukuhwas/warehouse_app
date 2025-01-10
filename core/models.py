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
