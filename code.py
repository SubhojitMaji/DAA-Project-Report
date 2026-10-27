from collections import deque
import sys

def min_distance_2_dominating_set(n, edges, root=0):
    if n == 0:
        return 0, []
    if n == 1:
        return 1, [0]

    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Compute depth and parent array using BFS
    parent = [-1] * n
    depth = [0] * n
    visited = [False] * n
    order = []

    queue = deque([root])
    visited[root] = True

    while queue:
        curr = queue.popleft()
        order.append(curr)
        for nbr in adj[curr]:
            if not visited[nbr]:
                visited[nbr] = True
                parent[nbr] = curr
                depth[nbr] = depth[curr] + 1
                queue.append(nbr)

    # Reverse BFS order gives nodes sorted by depth descending
    order.reverse()

    covered = [False] * n
    S = set()

    # Function to mark nodes within distance 2 as covered
    def mark_covered_dist_2(start_node):
        covered[start_node] = True
        # Distance 1
        for d1 in adj[start_node]:
            covered[d1] = True
            # Distance 2
            for d2 in adj[d1]:
                covered[d2] = True

    # Greedy choice processing
    for u in order:
        if not covered[u]:
            # Select highest available ancestor up to distance 2 (grandparent)
            chosen = u
            if parent[chosen] != -1:
                chosen = parent[chosen]
                if parent[chosen] != -1:
                    chosen = parent[chosen]

            S.add(chosen)
            mark_covered_dist_2(chosen)

    return len(S), sorted(list(S))

# Example usage
if __name__ == "__main__":
    # Sample Tree Input: 7 nodes
    # Edges: (0,1), (0,2), (1,3), (1,4), (2,5), (2,6)
    n_nodes = 7
    tree_edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    size, team = min_distance_2_dominating_set(n_nodes, tree_edges)
    print(f"Minimum Team Size: {size}")
    print(f"Selected Team Members: {team}")
