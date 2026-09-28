# Classic Algorithms in Python — Greedy, Backtracking & A* Search

Three algorithm-design paradigms implemented **from scratch in pure Python** (no external algorithm, graph, sorting-library or priority-queue packages), each as an interactive console program with input validation and a pytest suite.

| Paradigm | Problem | File | Time complexity |
|---|---|---|---|
| Greedy | Fractional Knapsack | [`fractional_knapsack.py`](fractional_knapsack.py) | O(n log n) |
| Backtracking | Graph Colouring (m-colouring + chromatic number) | [`graph_coloring.py`](graph_coloring.py) | O(mᵛ) worst case |
| Heuristic search | A* grid path finding | [`astar_pathfinding.py`](astar_pathfinding.py) | O(V²) with the list-based open set |

## Algorithms

### 1. Fractional Knapsack (Greedy)
Computes each item's value-to-weight ratio, sorts descending, then takes items whole while they fit and a fraction of the next one to fill the remaining capacity. Because items are divisible, the greedy choice is provably optimal.

```
Items (value, weight): (60,10) (100,20) (120,30)   Capacity: 50
→ 100% of item 1, 100% of item 2, 66.67% of item 3   Total value: 240.00
```

### 2. Graph Colouring (Backtracking)
Assigns colours vertex by vertex, checking that no neighbour shares the colour (`is_safe`), and backtracks when a later vertex gets stuck. Also finds the **chromatic number** by searching for the smallest `m` that yields a valid colouring, and verifies every edge of the result.

Applications: map colouring, exam/timetable scheduling, radio-frequency assignment, register allocation.

### 3. A* Path Finding (Heuristic)
Finds the shortest path on a grid with obstacles using `f(n) = g(n) + h(n)`, where `h` is the Manhattan distance (admissible for 4-directional movement, so the path is guaranteed optimal). The open set is a hand-written priority queue (linear scan for the lowest f-score) rather than `heapq`, so every part is built from first principles.

```
S . . . . .          S = start   G = goal
* . # . . .          # = obstacle
* . # . . .          * = path
* . # . . .
* . # . . .          Total steps: 10
* * * * * G
```

## Running

Requires Python 3.8+. No dependencies for the programs themselves.

```bash
python fractional_knapsack.py
python graph_coloring.py      # menu: custom graph / sample map / chromatic number
python astar_pathfinding.py   # menu: custom grid / sample grid
```

## Tests

```bash
pip install pytest
pytest -q
```

Covers the classic knapsack example, fractional-only and zero-capacity cases, 2-/3-/4-colourable graphs, and A* on open, blocked and trivial grids.

## Context

Built as a team project for **CSC2103 Data Structures & Algorithms** at Sunway University (April 2026 semester).
