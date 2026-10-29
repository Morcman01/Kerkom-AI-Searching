# TSP dengan A* dan Greedy Best-First Search (GBFS)

Program mencari rute terpendek TSP (mengunjungi semua kota sekali, lalu kembali
ke kota asal) menggunakan dua algoritma: A* dan GBFS.

## Persyaratan
Python 3.8 atau lebih baru. Tidak perlu install library tambahan.

## Format file input
4                  <- jumlah kota
A B C D            <- nama kota (dipisah spasi, tanpa spasi di dalam nama)
0 10 15 20         <- matriks jarak n x n (bilangan bulat >= 0, diagonal 0)
10 0 35 25
15 35 0 30
20 25 30 0

## Cara menjalankan
Buka terminal di folder proyek, lalu jalankan:
python main.py --input inputs/easy.txt
python main.py --input inputs/medium.txt --trace
python main.py --input inputs/hard.txt --algo astar --runs 5
python main.py --input inputs/easy.txt --algo astar --trace

| Argumen | Pilihan | Default | Fungsi |
|---|---|---|---|
| `--input` | path file | `inputs/easy.txt` | file input |
| `--algo` | `astar`, `gbfs`, `both` | `both` | algoritma yang dijalankan |
| `--start` | nama atau indeks kota | `0` | kota asal |
| `--trace` | - | mati | cetak isi frontier tiap langkah |
| `--runs` | bilangan >= 1 | `1` | pengulangan untuk rata-rata waktu |

## File input contoh
- `inputs/easy.txt`   : skenario mudah
- `inputs/medium.txt` : skenario menengah
- `inputs/hard.txt`   : skenario sulit
- `inputs/change.txt` : skenario dengan kondisi diubah

## Log eksperimen
Contoh membuat log:
python main.py --input inputs/hard.txt --runs 5 > results/hard.txt
python main.py --input inputs/medium.txt --runs 5 > results/cobayangmedium.txt