# initial state and problem
distances = [
    [0,  12,  8, 15,  7, 11],
    [12,  0,  6,  9, 14,  5],
    [8,   6,  0, 10,  4, 13],
    [15,  9, 10,  0,  8,  6],
    [7,  14,  4,  8,  0,  9],
    [11,  5, 13,  6,  9,  0]
]

start = 0
unvisited = {1, 2, 3, 4, 5}

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

frontier = [
    {
        "current": start,
        "unvisited": set(unvisited),
        "path": [start],
        "g": 0,
        "h": heuristic(start, start, unvisited, distances)
    }
]

state = frontier.pop(0)

# loop through all cities and calculate their heuristic
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

    print(
        f"Current city: {new_current}\n"
        f"Unvisited: {new_unvisited}\n"
        f"Current g: {new_g}\n"
        f"Path travelled: {new_path}\n"
        f"Current h: {new_h}\n"
    )