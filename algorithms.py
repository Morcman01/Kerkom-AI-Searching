import time
from itertools import count
# =====================================================================
# Heuristik
def mst_cost(unvisited, distances):
    """Biaya Minimum Spanning Tree (algoritma Prim) atas kota-kota unvisited."""
    if len(unvisited) <= 1:
        return 0

    nodes = sorted(unvisited)
    tree = {nodes[0]}
    remaining = set(nodes[1:])
    total = 0

    while remaining:
        cost, city = min(
            (distances[a][b], b)
            for a in tree
            for b in remaining
        )
        total += cost
        tree.add(city)
        remaining.remove(city)

    return total

def heuristic(current, start, unvisited, distances):
    """
    h(n) = jarak terdekat dari kota sekarang ke kota unvisited
        + MST kota unvisited
        + jarak terdekat dari kota unvisited kembali ke kota asal
    Admissible: sisa tur sungguhan minimal sebesar nilai ini.
    (Mengasumsikan matriks jarak simetris.)
    """
    if not unvisited:
        return distances[current][start]

    enter_cost = min(distances[current][c] for c in unvisited)
    return_cost = min(distances[c][start] for c in unvisited)
    return enter_cost + mst_cost(unvisited, distances) + return_cost
# =====================================================================
# Pencarian (A* dan GBFS memakai kerangka yang sama)
def _fmt_node(node, names, use_g):
    route = "->".join(names[i] for i in node["path"])
    if use_g:
        return (f"{route:<28} g={node['g']:<4} h={node['h']:<4} "
                f"f={node['g'] + node['h']}")
    return f"{route:<28} g={node['g']:<4} h={node['h']}"

def search(distances, start, algo="astar", names=None, trace=False):
    """
    Jalankan pencarian TSP.
    algo : "astar" (prioritas g + h) atau "gbfs" (prioritas h saja)
    Mengembalikan dict hasil, atau None kalau tidak ada solusi.
    """
    if algo not in ("astar", "gbfs"):
        raise ValueError("algo harus 'astar' atau 'gbfs'")

    n = len(distances)
    if names is None:
        names = [str(i) for i in range(n)]
    use_g = algo == "astar"

    def priority(node):
        return node["g"] + node["h"] if use_g else node["h"]

    start_unvisited = frozenset(range(n)) - {start}
    order = count()

    root = {
        "current": start,
        "unvisited": start_unvisited,
        "path": [start],
        "g": 0,
        "h": heuristic(start, start, start_unvisited, distances),
        "order": next(order),
    }

    # frontier: key (kota, unvisited) -> node.  explored: key -> g terbaik
    frontier = {(start, start_unvisited): root}
    explored = {}
    nodes_expanded = 0
    max_frontier_size = 1
    t0 = time.perf_counter()

    while frontier:
        key = min(frontier,
                    key=lambda k: (priority(frontier[k]), frontier[k]["order"]))
        state = frontier.pop(key)

        if trace:
            print(f"\n[pop] {_fmt_node(state, names, use_g)}")

        # goal test: semua kota sudah dikunjungi
        if not state["unvisited"]:
            return {
                "algo": algo,
                "path": state["path"] + [start],
                "distance": state["g"] + distances[state["current"]][start],
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "time": time.perf_counter() - t0,
            }

        explored[key] = state["g"]
        nodes_expanded += 1

        for city in sorted(state["unvisited"]):
            new_unvisited = state["unvisited"] - {city}
            new_g = state["g"] + distances[state["current"]][city]
            ckey = (city, new_unvisited)

            if use_g:
                # A*: abaikan jalur yang tidak lebih murah ke state yang sama
                if ckey in explored and explored[ckey] <= new_g:
                    continue
                if ckey in frontier and frontier[ckey]["g"] <= new_g:
                    continue
            else:
                # GBFS: state yang sudah pernah dilihat tidak dibangkitkan lagi
                if ckey in explored or ckey in frontier:
                    continue

            frontier[ckey] = {
                "current": city,
                "unvisited": new_unvisited,
                "path": state["path"] + [city],
                "g": new_g,
                "h": heuristic(city, start, new_unvisited, distances),
                "order": next(order),
            }
            max_frontier_size = max(max_frontier_size, len(frontier))

        if trace:
            print(f"  explored: {nodes_expanded} node | "
                    f"frontier: {len(frontier)} node")
            for node in sorted(frontier.values(),
                                key=lambda x: (priority(x), x["order"])):
                print("   ", _fmt_node(node, names, use_g))

    return None