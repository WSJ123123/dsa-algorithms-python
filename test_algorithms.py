from fractional_knapsack import fractionalknapsack
from graph_coloring import build_graph, color_graph, find_chromatic_number, sample_graph
from astar_pathfinding import a_star, build_grid, sample_grid


# ---------- Fractional knapsack ----------

def test_knapsack_classic_example():
    value, weight = fractionalknapsack([60, 100, 120], [10, 20, 30], 50)
    assert abs(value - 240) < 1e-9
    assert abs(weight - 50) < 1e-9


def test_knapsack_takes_fraction_when_capacity_smaller_than_every_item():
    value, weight = fractionalknapsack([100], [50], 10)
    assert abs(value - 20) < 1e-9
    assert abs(weight - 10) < 1e-9


def test_knapsack_zero_capacity():
    assert fractionalknapsack([60, 100], [10, 20], 0) == (0.0, 0.0)


# ---------- Graph colouring ----------

def is_valid_coloring(graph, colors):
    return all(colors[u] != colors[v] for u in graph for v in graph[u])


def test_sample_graph_needs_three_colors():
    n, edges, _ = sample_graph()
    graph = build_graph(n, edges)
    assert color_graph(graph, 2, n) is None
    colors = color_graph(graph, 3, n)
    assert colors is not None and is_valid_coloring(graph, colors)


def test_chromatic_number_of_complete_graph():
    n = 4
    edges = [(u, v) for u in range(n) for v in range(u + 1, n)]
    m, colors = find_chromatic_number(build_graph(n, edges), n)
    assert m == 4


def test_bipartite_graph_is_two_colorable():
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]  # even cycle
    m, _ = find_chromatic_number(build_graph(4, edges), 4)
    assert m == 2


# ---------- A* path finding ----------

def test_astar_sample_grid_finds_shortest_path():
    grid, start, goal = sample_grid()
    path, cost = a_star(grid, start, goal)
    assert path[0] == start and path[-1] == goal
    assert cost == 10  # Manhattan distance; the wall has a gap on the direct route
    assert all(grid[r][c] == 0 for r, c in path)


def test_astar_no_path_when_blocked():
    grid = build_grid(3, 3, [(0, 1), (1, 1), (2, 1)])
    assert a_star(grid, (0, 0), (0, 2)) == (None, None)


def test_astar_start_equals_goal():
    grid = build_grid(2, 2, [])
    assert a_star(grid, (0, 0), (0, 0)) == ([(0, 0)], 0)
