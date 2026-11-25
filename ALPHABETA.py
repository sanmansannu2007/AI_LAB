import math


def alphabeta(node, graph, values, node_type, alpha, beta):
    # Base case: leaf node
    if node in values:
        return values[node]

    if node_type[node] == "MAX":
        best = -math.inf
        for child in graph.get(node, []):
            best = max(
                best, alphabeta(child, graph, values, node_type, alpha, beta)
            )
            alpha = max(alpha, best)
            if beta <= alpha:
                print(
                    f"Beta cutoff at {node} (alpha={alpha}, beta={beta}) -> remaining children pruned"
                )
                break
        return best
    else:  # node_type[node] == "MIN"
        best = math.inf
        for child in graph.get(node, []):
            best = min(
                best, alphabeta(child, graph, values, node_type, alpha, beta)
            )
            beta = min(beta, best)
            if beta <= alpha:
                print(
                    f"Alpha cutoff at {node} (alpha={alpha}, beta={beta}) -> remaining children pruned"
                )
                break
        return best


# --- User Input ---
graph = {}
values = {}
node_type = {}

n = int(input("Enter number of internal nodes: "))
for _ in range(n):
    parent, role = (
        input("Enter parent node and type (e.g., A MAX): ").strip().split()
    )
    node_type[parent] = role.upper()
    children = input(f"Enter children of {parent} (space-separated): ").split()
    graph[parent] = children

m = int(input("\nEnter number of leaf nodes: "))
for _ in range(m):
    leaf, val = input("Enter leaf node and value (e.g., D 3): ").split()
    values[leaf] = float(val)

root = input("\nEnter root node: ").strip()

optimal_value = alphabeta(root, graph, values, node_type, -math.inf, math.inf)
print(f"\nOptimal value at {root}: {optimal_value}")