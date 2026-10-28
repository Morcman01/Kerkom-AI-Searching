import sys
import os

file_path = "./inputs/easy.txt"

if not os.path.exists(file_path):
        print("something aint right with the file :/")
        sys.exit(1)

# =====================================================================
# initial state and problem using file reading
distances = []
with open(file_path, "r") as file:
    lines = file.readlines()

    city_amount = int(lines[0])
    cities = lines[1].split()

    for i in range(2, 2 + city_amount):
        bar = list(map(int, lines[i].split()))
        distances.append(bar)

start = 0
unvisited = set(range(city_amount)) - {start}


# =====================================================================
# prim's algorithm for Minimum Spanning Tree
def mst_cost(unvisited, distances):
    if len(unvisited) <= 1:
        return 0

    tree = {next(iter(unvisited))}
    remaining = set(unvisited) - tree
    total = 0

    while remaining:
        best_edge = min(
            (distances[a][b], b)
            for a in tree
            for b in remaining
        )

        cost, city = best_edge

        total = total + cost
        tree.add(city)
        remaining.remove(city)

    return total

# calculates heuristic 
def heuristic(current, start, unvisited, distances):
    if not unvisited:
        return distances[current][start]

    enter_cost = min(
        distances[current][city]
        for city in unvisited
    )

    return_cost = min(
        distances[city][start]
        for city in unvisited
    )

    mst = mst_cost(unvisited, distances)
    return enter_cost + mst + return_cost


# =====================================================================
frontier = [
    {
        "current": start,
        "unvisited": set(unvisited),
        "path": [start],
        "g": 0,
        "h": heuristic(start, start, unvisited, distances)
    }
]

nodes_expanded = 0
max_frontier_size = len(frontier)

while frontier:
    state = min(
        frontier, key=lambda f: f["h"] + f["g"]
    )

    frontier.remove(state)

    if not state["unvisited"]:
        total_distance = (
            distances[state["current"]][start] + state["g"]
        )
        final_path = state["path"] + [start]
        break

    nodes_expanded = nodes_expanded + 1

    for next_city in state["unvisited"]:
        new_current = next_city
        new_unvisited = state["unvisited"] - {next_city}
        new_g = state["g"] + distances[state["current"]][next_city]
        new_path = state["path"] + [next_city]
        new_h = heuristic(new_current, start, new_unvisited, distances)

        new_state = {
            "current" : new_current,
            "unvisited" : new_unvisited,
            "g" : new_g,
            "path" : new_path,
            "h" : new_h
        }

        frontier.append(new_state)
        max_frontier_size = max(max_frontier_size, len(frontier))

        #  [DEBUGGING], BUAT NGELIAT SEMUA STATES DALAM FRONTIER YANG DIBUAT SELAMA NYARI JALUR
        # print(
        #     f"Current city: {new_current}\n"
        #     f"Unvisited: {new_unvisited}\n"
        #     f"Current g: {new_g}\n"
        #     f"Path travelled: {new_path}\n"
        #     f"Current h: {new_h}\n"
        # )

city_names = [cities[index] for index in final_path]
final_route = " -> ".join(city_names)

print("======================================")
print(f"Max frontier size: {max_frontier_size}")
print(f"Nodes expanded: {nodes_expanded}")
print(f"Final path: {final_route}")
print(f"Final distance travelled: {total_distance}")
print("======================================")