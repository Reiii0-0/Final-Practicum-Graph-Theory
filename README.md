# Praktikum Teori Graf

Repositori ini berisi kode implementasi untuk tugas praktikum mata kuliah Teori Graf. Terdapat dua permasalahan utama yang diselesaikan dalam praktikum ini: *The Knight's Tour* dan *Largest Monotonically Increasing Subsequence*.

---

## Anggota Kelompok

| Nama | NRP |
| :--- | :--- |
| Farikh Muhammad Fauzan | 5025241135 |
| Muhammad Akhdan Alwaafy | 5025241223 |
| Raymond Julius Pardosi | 5025241268 |


---

## Struktur Direktori

Setiap folder Praktikum berisi dua jenis file:
* **`.md`**: Berisi penjelasan algoritma dan visualisasi.
* **`.py`**: Berisi kode implementasi untuk menyelesaikan permasalahan.

```bash
.
├── TugasPraktikum1/
│   ├── README.md
│   └── knights_tour.py
├── TugasPraktikum2/
│   ├── README.md
│   └── lis_tree.py
└── README.md
````

-----

## Praktikum 1: The Knight's Tour

### Deskripsi Masalah

Program ini menyimulasikan perjalanan bidak kuda (*Knight*) pada papan catur berukuran $8 \times 8$. Kuda diletakkan pada sembarang kotak dan harus mengunjungi **setiap kotak tepat satu kali**.

Program dapat menangani dua situasi:

1.  **Open Tour**: Kuda mengakhiri perjalanan di sembarang kotak (kotak terakhir tidak perlu bisa menyerang kotak awal).
2.  **Closed Tour**: Kuda mengakhiri perjalanan pada *attacking square* (kotak terakhir dapat melangkah kembali ke kotak awal, membentuk sirkuit tertutup).

Output program akan menampilkan visualisasi rute perjalanan kuda pada grid papan catur.

### Cara Penggunaan (Input & Output)

1.  Jalankan file script:
    ```bash
    python "TugasPraktikum1/knights_tour.py"
    ```
2.  **Input**: Masukkan koordinat awal kuda (baris 0-7, kolom 0-7) saat diminta program.
3.  **Output**: Program akan mencetak matriks atau visualisasi langkah demi langkah (1 sampai 64) yang menunjukkan urutan kunjungan kuda.

-----

## Praktikum 2: Largest Monotonically Increasing Subsequence

### Deskripsi Masalah

Program ini mengimplementasikan algoritma berbasis *Tree* untuk menyelesaikan permasalahan *Largest Monotonically Increasing Subsequence* (Subsekuens Mennaik Terpanjang).

Tujuan program adalah mencari urutan bilangan yang nilainya terus menaik dengan panjang maksimum dari sebuah urutan input, tanpa mengubah posisi relatif urutan aslinya (hanya boleh melompati/membuang angka).

**Contoh Kasus Sesuai Modul:**

  * **Input Sequence**: `4, 1, 13, 7, 0, 2, 8, 11, 3`
  * **Metode**: Menggunakan struktur pohon (*tree*) untuk menelusuri kemungkinan subsekuens.

### Cara Penggunaan (Input & Output)

1.  Jalankan file script:
    ```bash
    python "TugasPraktikum2/lis_tree.py"
    ```
2.  **Input**: Program secara default menggunakan urutan angka dari modul. (Opsional: Anda bisa memodifikasi kode untuk menerima input user).
3.  **Output**: Program akan menampilkan panjang maksimum subsekuens dan deret angka tersebut.
      * *Contoh Output yang diharapkan*: `Longest Subsequence: [1, 2, 8, 11]` (Panjang: 4).
