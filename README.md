# Minimum Distance-2 Dominating Set on a Tree

**DAA Project · Question 5**

**Authors:** Sayan Bhadra (`bmat2419`) and Subhojit Maji (`bmat2434`)

**Date:** 27 October 2026

This project studies the problem of finding a **minimum distance-2 dominating set in a tree** using a bottom-up greedy algorithm. The problem can be interpreted as selecting a minimum-sized supervisory or coordination team such that every member of an organization is within two reporting links of at least one selected coordinator.

**Repository:** [SubhojitMaji/DAA-Project-Report](https://github.com/SubhojitMaji/DAA-Project-Report)

---

## 1. Problem Statement

Let $T=(V,E)$ be a rooted tree with $n=|V|$ vertices and a designated root $r$.

For any two vertices $u,v\in V$, let $\operatorname{dist}_T(u,v)$ denote the number of edges on the unique path connecting them.

We seek a subset $S\subseteq V$ of minimum cardinality such that every vertex lies within distance two of at least one vertex in $S$.

Formally, the optimization problem is

$$
\min |S|
$$

subject to

$$
\forall u\in V,\quad
\exists v\in S
\text{ such that }
\operatorname{dist}_T(u,v)\leq 2.
$$

Such a set is called a **distance-2 dominating set**.

The objective is to minimize the number of selected vertices while ensuring that every vertex in the tree is covered.

## 2. Greedy Algorithm

The algorithm follows a bottom-up greedy strategy.

The central idea is to process the deepest uncovered vertices first and select an ancestor that can cover the current vertex while also covering other vertices nearby.

### Algorithm Overview

1. Perform a breadth-first search (BFS) from the root to compute the depth and parent of every vertex.
2. Reverse the BFS traversal order to obtain a deepest-first processing order.
3. Process each vertex $u$ in this order.
4. If $u$ is already covered, skip it.
5. Otherwise, select its grandparent if one exists, its parent if only the parent exists, or $u$ itself if neither exists.
6. Mark every vertex at distance at most two from the selected vertex as covered.
7. Return the selected vertices and their count.

The set of selected vertices is the output of the algorithm.

### Pseudocode

```text
MIN-DISTANCE-2-DOMINATING-SET(T, r)

    Compute parent[u] and depth[u] using BFS from r
    L = reverse(BFS traversal order)

    S = empty set
    covered[u] = False for every vertex u

    for each vertex u in L:

        if covered[u] == False:

            v = u

            if parent[v] exists:
                v = parent[v]

                if parent[v] exists:
                    v = parent[v]

            Add v to S

            Mark every vertex w with dist_T(v, w) <= 2
            as covered

    return S
```

## 3. Correctness

The algorithm processes vertices in descending order of depth. Consequently, when an uncovered vertex is considered, all vertices deeper in the tree have already been processed.

For an uncovered vertex $u$, every valid distance-2 dominating set must contain some vertex within distance two of $u$.

The greedy strategy selects the highest ancestor of $u$ available within two edges. This choice covers $u$ and may additionally cover vertices closer to the root.

An exchange argument can be used to establish optimality: an appropriate solution containing a vertex that covers $u$ can be transformed to contain the greedy choice without increasing the cardinality of the dominating set or leaving any vertex uncovered.

Applying this argument successively to the greedy selections establishes that the resulting distance-2 dominating set has minimum cardinality.

## 4. Complexity Analysis

Let $n=|V|$. Since $T$ is a tree,

$$
|E|=n-1.
$$

### Time Complexity

**BFS:** Computing the parent pointers and depths requires

$$
O(|V|+|E|)=O(n).
$$

**Ordering:** Reversing the BFS traversal order takes $O(n)$ time and produces an order with non-increasing depths.

**Greedy selection:** Each vertex is considered once. When a vertex is selected, its distance-2 neighborhood is explored and marked as covered. The total neighborhood-exploration cost is $O(n)$ for a tree because the selected vertices are pairwise at distance greater than two, so their immediate neighborhoods do not overlap.

Therefore, the overall running time is

$$
\boxed{T(n)=O(n)}.
$$

### Space Complexity

The algorithm stores:

- An adjacency list representing the tree.
- Parent and depth arrays.
- A coverage array.
- The BFS traversal order.
- The set of selected vertices.

Each requires at most $O(n)$ space.

Hence, the total space complexity is

$$
\boxed{S(n)=O(n)}.
$$

## 5. Python Implementation

The implementation uses only Python's standard library, including `collections.deque` for BFS.

### Function Signature

```python
min_distance_2_dominating_set(n, edges, root=0)
```

**Parameters**

- `n`: Number of vertices, labelled from `0` to `n - 1`.
- `edges`: A collection of `(u, v)` pairs representing the tree edges.
- `root`: The root vertex, defaulting to `0`.

**Returns**

A pair `(size, vertices)`, where:

- `size` is the number of selected vertices.
- `vertices` is the sorted list of selected vertex labels.

The implementation assumes a valid tree with vertex labels in the prescribed range. For an empty tree, it returns `(0, [])`.

### Running the Program

Save the Python implementation in `main.py` and execute:

```bash
python main.py
```

### Example

Consider the tree with seven vertices

$$
V=\{0,1,2,3,4,5,6\}
$$

and edges

```python
edges = [
    (0, 1),
    (0, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 6)
]
```

Taking vertex `0` as the root, every vertex is within distance two of vertex `0`.

Thus, the minimum distance-2 dominating set contains just one vertex.

**Expected output:**

```text
Minimum Team Size: 1
Selected Team Members: [0]
```

## 6. Applications

The distance-2 domination problem has potential applications in:

- **Organizational networks:** Selecting a minimum number of coordinators so that every employee is within two reporting links of a coordinator.
- **Communication networks:** Placing monitoring or coordination nodes in tree-structured networks.
- **Hierarchical systems:** Identifying a small set of representatives that provides coverage across a hierarchy.

## 7. Conclusion

This project investigates a greedy algorithm for finding a minimum distance-2 dominating set in a rooted tree.

The algorithm combines BFS-based preprocessing, deepest-first vertex processing, and local neighborhood marking. Its intended running time and space requirements are both linear in the number of vertices.

The project connects a classical graph optimization problem with algorithm design techniques, including greedy selection, exchange arguments, and asymptotic complexity analysis.

---

**Project:** Design and Analysis of Algorithms (DAA)  
**Question:** 5  
**Repository:** [DAA-Project-Report](https://github.com/SubhojitMaji/DAA-Project-Report)
