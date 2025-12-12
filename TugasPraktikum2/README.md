### Penjelasan Singkat Algoritma

* **Logika Tree**
    Sesuai gambar, kita membangun pohon keputusan. Dari angka `0`, kita bisa pergi ke `2`, dari `2` bisa ke `8` atau `3` (tapi di gambar contoh `2 -> 8 -> 11`).

* **Proses**
    Kode membangun struktur pohon di mana *child* hanya ditambahkan jika nilainya **lebih besar** dari *parent* dan posisinya **setelah** *parent*. Kemudian fungsi `find_longest_path` menelusuri kedalaman pohon (*Depth First Search*) untuk menemukan rantai terpanjang.

* **Output**
    Program akan menghasilkan salah satu *subsequence* terpanjang, misalnya `[0, 2, 8, 11]` atau `[1, 2, 8, 11]`.

## 📋 Prasyarat

Pastikan Anda telah menginstal **Python 3.x** di komputer Anda.

## 1. Largest Monotonically Increasing Subsequence (LMIS)

[cite_start]Program ini mengimplementasikan struktur data **Tree** untuk mencari urutan angka yang nilainya terus meningkat dari sebuah deret bilangan acak, sesuai dengan konsep yang diberikan[cite: 3, 4].

### 🚀 Cara Menjalankan Program

1.  Buka terminal atau command prompt.
2.  Arahkan direktori ke folder tempat file disimpan.
3.  Jalankan perintah berikut:
    ```bash
    python lmis_tree.py
    ```
    *(Ganti `lmis_tree.py` dengan nama file kode python Anda)*

### 📥 Format Input

Program dirancang untuk menerima input dinamis dari pengguna.
* Masukkan sekumpulan angka bilangan bulat.
* Pisahkan setiap angka dengan **SPASI**.
* Tekan **Enter** untuk memproses.

**Contoh Input:**
```text
4 1 13 7 0 2 8 11 3
