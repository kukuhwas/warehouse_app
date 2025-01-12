INSERT INTO
    barang (kode_barang, nama_barang, deskripsi, kategori_id, satuan)
VALUES
    ('ABDD11', 'Pensil 2B', 'Pensil kayu 2B merk Y', 'A', 'pcs'),
    ('ABDD12', 'Pulpen Hitam', 'Pulpen tinta hitam merk X', 'A', 'pcs'),
    ('ABDD13', 'Buku Tulis', 'Buku tulis isi 50 lembar', 'B', 'pak'),
    ('ABDD14', 'Snack Kentang', 'Snack kentang rasa rumput laut', 'C', 'pcs'),
    ('ABDD15', 'Minuman Soda', 'Minuman soda kaleng', 'D', 'pcs'),
    ('ABDD16', 'Kabel HDMI', 'Kabel HDMI 2 meter', 'E', 'pcs');


INSERT INTO
    varian (barang_id, nama_varian, nilai_varian, sku)
VALUES
    (1558, 'Warna', 'Hitam', 'ABDD11-01'),
    (1558, 'Warna', 'Biru', 'ABDD11-02'),
    (1559, 'Warna', 'Abu-abu', 'ABDD12-01'),
    (1560, 'Isi', '50', 'ABDD13-01'), 
    (1561, 'Rasa', 'Rumput Laut', 'ABDD14-01'),
    (1562, 'Rasa', 'Cola', 'ABDD15-01'),
    (1563, 'Panjang', '2 Meter', 'ABDD16-01');