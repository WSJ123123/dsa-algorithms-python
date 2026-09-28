"""
Problem 3: A* Search Algorithm for Path Finding (Heuristic Algorithm)

Finds the shortest path between a start and goal cell on a grid, using
the estimated distance to the goal (a heuristic) to search more efficiently
than a blind search like plain Dijkstra's algorithm.

The priority queue (open set) used to pick the next cell to explore is
implemented manually with a plain list, instead of a built-in library, so
that every part of the algorithm is written from scratch.
"""

import sys


# Estimates the distance from one cell to another
# "heuristic" part of A* - it never overestimates the real distance on a grid where only up/down/left/right moves are allowed.
def heuristic(a, b):
    (r1, c1), (r2, c2) = a, b
    return abs(r1 - r2) + abs(c1 - c2)


# Returns the walkable neighbouring cells (up, down, left, right) of a cell
def get_neighbours(grid, cell):
    rows, cols = len(grid), len(grid[0])
    r, c = cell
    candidates = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    neighbours = []
    for nr, nc in candidates:
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
            neighbours.append((nr, nc))
    return neighbours


# Walks backwards through the came_from map to build the final path in order
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


# Manually finds and removes the cell with the lowest f-score from the open set, by scanning through it - this replaces a built-in priority queue.
def pop_lowest_f(open_set, f_score):
    best_index = 0
    for i in range(1, len(open_set)):
        if f_score[open_set[i]] < f_score[open_set[best_index]]:
            best_index = i
    return open_set.pop(best_index)


# The core A* search: explores cells in order of (distance so far + estimated distance remaining), always expanding the most promising cell next
def a_star(grid, start, goal):
    open_set = [start]

    came_from = {}
    g_score = {start: 0}          # cost of the best known path from start to this cell
    f_score = {start: heuristic(start, goal)}  # g_score + heuristic estimate to goal

    while open_set:
        current = pop_lowest_f(open_set, f_score)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, g_score[goal]

        for neighbour in get_neighbours(grid, current):
            tentative_g = g_score[current] + 1  # each move costs 1 step

            if tentative_g < g_score.get(neighbour, float("inf")):
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g
                f_score[neighbour] = tentative_g + heuristic(neighbour, goal)
                if neighbour not in open_set:
                    open_set.append(neighbour)

    return None, None  # no path exists


def read_int(prompt, min_value=None):
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Please enter a value >= {min_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def read_cell(prompt, rows, cols):
    while True:
        raw = input(prompt).split()
        if len(raw) != 2:
            print("Please enter exactly two numbers: row col")
            continue
        try:
            r, c = int(raw[0]), int(raw[1])
        except ValueError:
            print("Row and column must be whole numbers.")
            continue
        if not (0 <= r < rows) or not (0 <= c < cols):
            print(f"Row must be 0-{rows - 1} and column must be 0-{cols - 1}.")
            continue
        yield (r, c)
        return


def read_obstacles(rows, cols, num_obstacles):
    obstacles = []
    print(f"Enter {num_obstacles} obstacle cells as: row col")
    while len(obstacles) < num_obstacles:
        cell = next(read_cell(f"Obstacle {len(obstacles) + 1}: ", rows, cols))
        obstacles.append(cell)
    return obstacles


def build_grid(rows, cols, obstacles):
    grid = [[0] * cols for _ in range(rows)]
    for r, c in obstacles:
        grid[r][c] = 1
    return grid


def sample_grid():
    """A ready-made 6x6 grid with a wall, for quick testing."""
    rows, cols = 6, 6
    obstacles = [(1, 2), (2, 2), (3, 2), (4, 2)]  # a vertical wall with a gap
    start = (0, 0)
    goal = (5, 5)
    grid = build_grid(rows, cols, obstacles)
    return grid, start, goal


def display_grid(grid, start, goal, path=None):
    path_cells = set(path) if path else set()
    print()
    for r, row in enumerate(grid):
        line = []
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == start:
                line.append("S")
            elif pos == goal:
                line.append("G")
            elif cell == 1:
                line.append("#")
            elif pos in path_cells:
                line.append("*")
            else:
                line.append(".")
        print(" ".join(line))
    print()
    print("Legend: S = start, G = goal, # = obstacle, * = path, . = open cell")


def run_search(grid, start, goal):
    path, cost = a_star(grid, start, goal)
    if path:
        print(f"\nPath found! Total steps (cost): {cost}")
        print("Path coordinates:", path)
        display_grid(grid, start, goal, path)
    else:
        print("\nNo path exists between start and goal on this grid.")
        display_grid(grid, start, goal)


def main():
    print("=" * 50)
    print(" A* Search Algorithm - Path Finding")
    print("=" * 50)

    while True:
        print("\nMenu:")
        print("1. Enter a custom grid, obstacles, start and goal")
        print("2. Use a sample grid")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            rows = read_int("Enter number of rows: ", min_value=1)
            cols = read_int("Enter number of columns: ", min_value=1)
            num_obstacles = read_int("Enter number of obstacle cells: ", min_value=0)
            obstacles = read_obstacles(rows, cols, num_obstacles)
            grid = build_grid(rows, cols, obstacles)
            print(f"Enter start cell (row col), 0-{rows - 1} and 0-{cols - 1}:")
            start = next(read_cell("Start: ", rows, cols))
            print(f"Enter goal cell (row col), 0-{rows - 1} and 0-{cols - 1}:")
            goal = next(read_cell("Goal: ", rows, cols))
            run_search(grid, start, goal)

        elif choice == "2":
            grid, start, goal = sample_grid()
            run_search(grid, start, goal)

        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid option. Please choose 1-3.")


if __name__ == "__main__":
    main()
