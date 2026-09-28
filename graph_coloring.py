"""
Problem 2: Graph Coloring Problem (Backtracking)

Assigns colors to graph vertices such that no two adjacent vertices
share the same color, using recursive backtracking with constraint checking.
"""

import sys


# Turns the list of edges into a dictionary of {vertex: [connected vertices]}
def build_graph(num_vertices, edges):
    graph = {v: [] for v in range(num_vertices)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph


# Checks if a vertex can use this color (no neighbours are using the same colour)
def is_safe(vertex, graph, colors, color):
    for neighbour in graph[vertex]:
        if colors[neighbour] == color:
            return False
    return True


# The actual backtracking: tries to color each vertex one by one undoing a colour and trying the next one whenever a later vertex gets stuck
def color_graph_util(graph, m, colors, vertex, num_vertices):
    if vertex == num_vertices:
        return True

    for color in range(1, m + 1):
        if is_safe(vertex, graph, colors, color):
            colors[vertex] = color
            if color_graph_util(graph, m, colors, vertex + 1, num_vertices):
                return True
            colors[vertex] = 0  # backtrack

    return False


# Wrapper that sets up an empty coloring and starts the backtracking from vertex 0
def color_graph(graph, m, num_vertices):
    colors = [0] * num_vertices
    if color_graph_util(graph, m, colors, 0, num_vertices):
        return colors
    return None


# Keeps trying more colors (1, 2, 3...) until one amount works, which gives the minimum number of colors needed
def find_chromatic_number(graph, num_vertices):
    """Bonus feature: find the smallest m for which the graph can be colored."""
    for m in range(1, num_vertices + 1):
        result = color_graph(graph, m, num_vertices)
        if result:
            return m, result
    return num_vertices, list(range(1, num_vertices + 1))


# Keeps asking the user for a whole number until a valid one is entered
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


# Asks the user to type in each edge (as two vertex numbers) and validates it
def read_edges(num_vertices, num_edges):
    edges = []
    print(f"Enter {num_edges} edges as: vertex1 vertex2  (vertices numbered 0 to {num_vertices - 1})")
    while len(edges) < num_edges:
        raw = input(f"Edge {len(edges) + 1}: ").split()
        if len(raw) != 2:
            print("Please enter exactly two vertex numbers separated by a space.")
            continue
        try:
            u, v = int(raw[0]), int(raw[1])
        except ValueError:
            print("Vertices must be whole numbers.")
            continue
        if not (0 <= u < num_vertices) or not (0 <= v < num_vertices):
            print(f"Vertices must be between 0 and {num_vertices - 1}.")
            continue
        if u == v:
            print("Self-loops are not allowed.")
            continue
        edges.append((u, v))
    return edges


# Returns a ready-made test graph (5 regions) so you don't have to type one in
def sample_graph():
    num_vertices = 5
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
    names = ["Region A", "Region B", "Region C", "Region D", "Region E"]
    return num_vertices, edges, names


# Prints each vertex's assigned color, then checks every edge to confirm no two connected vertices share the same color
def display_result(colors, graph, names=None):
    print("\n--- Coloring Result ---")
    for v in range(len(colors)):
        label = names[v] if names else f"Vertex {v}"
        print(f"{label}: Color {colors[v]}")

    print("\n--- Verification (edges) ---")
    ok = True
    checked = set()
    for u in graph:
        for v in graph[u]:
            edge = tuple(sorted((u, v)))
            if edge in checked:
                continue
            checked.add(edge)
            lu = names[u] if names else f"V{u}"
            lv = names[v] if names else f"V{v}"
            same = colors[u] == colors[v]
            if same:
                ok = False
            print(f"{lu} - {lv}: colors {colors[u]} vs {colors[v]}  {'CONFLICT' if same else 'OK'}")
    print("All constraints satisfied." if ok else "Conflicts found!")


# Shows the menu, reads the user's choice, and runs the matching option
def main():
    print("=" * 50)
    print(" Graph Coloring Problem - Backtracking Algorithm")
    print("=" * 50)

    while True:
        print("\nMenu:")
        print("1. Enter a custom graph and try a fixed number of colors")
        print("2. Use a sample graph (5-region map)")
        print("3. Find the minimum number of colors needed (chromatic number)")
        print("4. Exit")
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            num_vertices = read_int("Enter number of vertices: ", min_value=1)
            num_edges = read_int("Enter number of edges: ", min_value=0)
            edges = read_edges(num_vertices, num_edges)
            graph = build_graph(num_vertices, edges)
            m = read_int("Enter number of colors to try: ", min_value=1)

            result = color_graph(graph, m, num_vertices)
            if result:
                print(f"\nSuccess! The graph can be colored using {m} colors.")
                display_result(result, graph)
            else:
                print(f"\nNo valid coloring exists using only {m} colors.")

        elif choice == "2":
            num_vertices, edges, names = sample_graph()
            graph = build_graph(num_vertices, edges)
            m = read_int("Enter number of colors to try (this sample needs at least 3): ", min_value=1)
            result = color_graph(graph, m, num_vertices)
            if result:
                print(f"\nSuccess! The sample graph can be colored using {m} colors.")
                display_result(result, graph, names)
            else:
                print(f"\nNo valid coloring exists using only {m} colors.")

        elif choice == "3":
            print("\n1. Custom graph  2. Sample graph")
            sub = input("Choose graph source (1-2): ").strip()
            if sub == "1":
                num_vertices = read_int("Enter number of vertices: ", min_value=1)
                num_edges = read_int("Enter number of edges: ", min_value=0)
                edges = read_edges(num_vertices, num_edges)
                graph = build_graph(num_vertices, edges)
                names = None
            else:
                num_vertices, edges, names = sample_graph()
                graph = build_graph(num_vertices, edges)

            m, result = find_chromatic_number(graph, num_vertices)
            print(f"\nMinimum number of colors required (chromatic number): {m}")
            display_result(result, graph, names)

        elif choice == "4":
            print("Goodbye, See You Again!")
            sys.exit(0)

        else:
            print("Invalid option. Please choose 1-4.")


if __name__ == "__main__":
    main()
