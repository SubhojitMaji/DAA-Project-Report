# Minimum Distance-2 Dominating Set on a Tree

**DAA Project · Question 5**  
**Authors:** Sayan Bhadra (`bmat2419`) and Subhojit Maji (`bmat2434`)  
**Date:** 27 October 2026

This project implements a greedy algorithm for finding a **minimum distance-2 dominating set** in a tree. The model can represent a supervisory or coordination network: each vertex is a person, each edge is a direct reporting relationship, and a selected vertex can cover everyone at graph distance at most two.

Repository: [SubhojitMaji/DAA-Project-Report](https://github.com/SubhojitMaji/DAA-Project-Report)

## Problem statement

Let \(T=(V,E)\) be a tree with \(n=|V|\) vertices and a designated root \(r\). For vertices \(u,v\in V\), let \(\operatorname{dist}_T(u,v)\) be the number of edges on their unique path.

Find a set \(S\subseteq V\) of minimum cardinality such that every vertex is within distance two of at least one selected vertex:

\[
\min |S| \qquad\text{subject to}\qquad
\forall u\in V,\ \exists v\in S:\operatorname{dist}_T(u,v)\leq 2.
\]

Such a set is called a **distance-2 dominating set**. The goal is to minimize the number of selected vertices, not merely to find any feasible set.

## Algorithm

The solution uses a bottom-up greedy strategy.

1. Run breadth-first search (BFS) from the root to compute each vertex's depth and parent.
2. Process vertices in descending order of depth, so deeper vertices are considered first.
3. When an uncovered vertex \(u\) is encountered, select its grandparent if one exists. If not, select its parent if one exists; otherwise select \(u\) itself.
4. Mark every vertex at distance at most two from the selected vertex as covered.
5. Return the selected vertices and their count.

The key idea is to handle the deepest uncovered vertices first. An exchange argument shows why choosing the highest ancestor available within two edges is an optimal greedy choice: it covers the current vertex while also reaching vertices nearer the root. The selected vertices are kept far enough apart that the distance-2 marking work has linear total cost.

## Complexity

For a tree represented by adjacency lists, the algorithm uses:

- **Time:** \(O(n)\)
- **Auxiliary space:** \(O(n)\)

BFS computes the parent/depth information in linear time. Because vertex depths lie between \(0\) and \(n-1\), reversing BFS order gives a deepest-first order in linear time without comparison sorting. The marking procedure explores only distance-2 neighborhoods; across the full greedy run, this work is linear in the size of the tree.

## Implementation

The implementation uses only Python's standard library, specifically `collections.deque` for BFS.

The main function has the following interface:

```python
min_distance_2_dominating_set(n, edges, root=0)
```

**Parameters**

- `n`: number of vertices, labelled `0` through `n - 1`.
- `edges`: an iterable of `(u, v)` pairs, one for each tree edge.
- `root`: the root vertex, defaulting to `0`.

**Returns**

A pair `(size, vertices)`, where `size` is the number of selected vertices and `vertices` is the sorted list of selected vertex labels.

The function assumes that the input is a valid tree, that vertex labels are in range, and that `root` is a valid vertex when `n > 0`. The empty-tree case returns `(0, [])`.

## Running the example

Save the Python implementation in `main.py` (or use the filename in your checkout), then run:

```bash
python main.py
```

The example tree in the implementation has seven vertices and edges

```text
(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)
```

Its root, vertex `0`, is within distance two of every vertex. The expected output is therefore:

```text
Minimum Team Size: 1
Selected Team Members: [0]
```

## Correctness outline

The algorithm processes vertices from greatest depth to least depth. When it reaches an uncovered vertex \(u\), all deeper vertices have already been covered. Every valid distance-2 dominating set must include some vertex within distance two of \(u\). By replacing an appropriate such choice with the highest ancestor of \(u\) available within two edges, an optimal solution can be transformed to include the greedy choice without increasing the number of selected vertices or leaving any still-uncovered vertex undominated. Applying this exchange step at each selection shows that the greedy choices can be part of an optimal solution. Since the algorithm eventually covers every vertex, the returned set is a minimum distance-2 dominating set.

## Project report

The accompanying report develops the tree model, greedy strategy, pseudocode, correctness argument, complexity analysis, and Python implementation.
