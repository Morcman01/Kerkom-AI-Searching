import argparse
import os
import sys

from algorithms import search
# =====================================================================
# Membaca dan memvalidasi input
def read_problem(file_path):
    """Baca file input. Format:
            baris 1 : jumlah kota (n)
            baris 2 : nama kota (n nama dipisah spasi)
            baris 3+: matriks jarak n x n
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File tidak ditemukan: {file_path}")

    with open(file_path, "r") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    if len(lines) < 2:
        raise ValueError("File terlalu pendek: butuh jumlah kota, nama kota, dan matriks.")

    try:
        n = int(lines[0])
    except ValueError:
        raise ValueError("Baris pertama harus berupa bilangan bulat (jumlah kota).")
    if n < 1:
        raise ValueError("Jumlah kota harus minimal 1.")

    names = lines[1].split()
    if len(names) != n:
        raise ValueError(f"Jumlah nama kota ({len(names)}) tidak sama dengan n ({n}).")
    if len(set(names)) != n:
        raise ValueError("Nama kota tidak boleh ada yang sama.")

    rows = lines[2:]
    if len(rows) != n:
        raise ValueError(f"Matriks harus punya {n} baris, ditemukan {len(rows)}.")

    distances = []
    for i, row in enumerate(rows):
        try:
            values = [int(x) for x in row.split()]
        except ValueError:
            raise ValueError(f"Baris matriks ke-{i + 1} berisi nilai yang bukan bilangan bulat.")
        if len(values) != n:
            raise ValueError(f"Baris matriks ke-{i + 1} harus punya {n} nilai, ditemukan {len(values)}.")
        if any(v < 0 for v in values):
            raise ValueError(f"Baris matriks ke-{i + 1} berisi jarak negatif.")
        distances.append(values)

    for i in range(n):
        if distances[i][i] != 0:
            raise ValueError(f"Diagonal matriks harus 0 (baris {i + 1}).")

    return names, distances


def is_symmetric(distances):
    n = len(distances)
    return all(distances[i][j] == distances[j][i] for i in range(n) for j in range(n))


def resolve_start(start_arg, names):
    if start_arg in names:
        return names.index(start_arg)
    if start_arg.isdigit() and int(start_arg) < len(names):
        return int(start_arg)
    raise ValueError(f"Kota asal '{start_arg}' tidak ada. Pilihan: {', '.join(names)}")
# =====================================================================
# Menjalankan dan mencetak hasil
def run(algo, distances, start, names, trace, runs):
    result = search(distances, start, algo, names, trace)
    if result is None:
        print(f"[{algo.upper()}] Tidak ditemukan solusi.")
        return

    # ukur waktu eksekusi: rata-rata dari beberapa kali jalan (tanpa trace)
    times = [result["time"]]
    for _ in range(runs - 1):
        times.append(search(distances, start, algo, names, False)["time"])
    avg_time = sum(times) / len(times)

    label = "A*" if algo == "astar" else "GBFS"
    route = " -> ".join(names[i] for i in result["path"])
    print("======================================")
    print(f"Algoritma          : {label}")
    print(f"Rute               : {route}")
    print(f"Total jarak        : {result['distance']}")
    print(f"Node expanded      : {result['nodes_expanded']}")
    print(f"Max frontier size  : {result['max_frontier_size']}")
    print(f"Waktu eksekusi     : {avg_time * 1000:.3f} ms (rata-rata {runs} run)")
    print("======================================")


def main():
    parser = argparse.ArgumentParser(description="TSP dengan A* dan GBFS")
    parser.add_argument("--input", default="inputs/easy.txt", help="path file input")
    parser.add_argument("--algo", choices=["astar", "gbfs", "both"], default="both")
    parser.add_argument("--start", default="0", help="kota asal (nama atau indeks, default indeks 0)")
    parser.add_argument("--trace", action="store_true", help="tampilkan isi frontier tiap langkah")
    parser.add_argument("--runs", type=int, default=1, help="jumlah pengulangan untuk rata-rata waktu")
    args = parser.parse_args()

    if args.runs < 1:
        print("Error: --runs minimal 1.")
        sys.exit(1)

    try:
        names, distances = read_problem(args.input)
        start = resolve_start(args.start, names)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not is_symmetric(distances):
        print("Peringatan: matriks tidak simetris. Heuristik MST mengasumsikan "
                "simetris, jadi optimalitas A* tidak dijamin.")

    algos = ["astar", "gbfs"] if args.algo == "both" else [args.algo]
    for algo in algos:
        run(algo, distances, start, names, args.trace, args.runs)


if __name__ == "__main__":
    main()