# Lab Report 1 — Artificial Intelligence
## Search, Problem Solving & Backtracking

**Subject:** Artificial Intelligence
**Topic:** Backtracking, Constraint Satisfaction Problems (CSP), and Search Strategies

---

## 1. Objective

To understand the fundamental concepts of problem solving in AI — backtracking, well-defined problems, constraint satisfaction problems, and search strategies (uninformed, informed, adversarial) — and to implement and visualize these concepts through three practical programs: a **Maze Solver**, a **Sudoku Solver**, and a **Path Optimization (Route Finder)** simulation.

## 2. Theory Covered

- **Backtracking:** A trial-and-error technique — try a choice, and if it leads to a dead end or violates a constraint, undo it and try the next option ("Try → Fail → Undo → Try Again").
- **Backpropagation** (studied for comparison): a neural-network training method that adjusts weights by propagating error backwards; unlike backtracking, it involves learning rather than undoing choices.
- **Well-Defined Problems:** Have a fixed initial state and goal state (e.g., maze, route finding, path optimization).
- **Constraint Satisfaction Problems (CSP):** Defined by variables, domains, and constraints; a solution is a complete and consistent assignment (e.g., Sudoku, N-Queens, map colouring).
- **Search Strategies:**
  - *Uninformed Search* — BFS, DFS, UCS (no knowledge of goal distance).
  - *Informed Search* — A*, Greedy Best-First, Hill Climbing (uses a heuristic).
  - *Adversarial Search* — Minimax, Alpha-Beta Pruning (used in two-player games).

## 3. Programs Implemented

### 3.1 Maze Solver (`maze.py`)
A Pygame visualization that solves a maze using **recursive backtracking (DFS-based)**. The "agent" explores in four directions (down, right, up, left); visited cells are marked, dead ends are flagged and colored (yellow → purple), and successful paths turn green. This directly demonstrates backtracking on a well-defined problem: fixed start `(0,0)` and goal (bottom-right cell).

### 3.2 Sudoku Solver (`suduko.py`)
A Pygame visualization that solves a 9×9 Sudoku puzzle using **backtracking with constraint checking**. For each empty cell, digits 1–9 are tried; `is_valid()` checks row, column, and 3×3 box constraints. Valid entries are shown in green, invalid attempts are discarded, and backtracked cells flash red before resetting. This is a classic CSP example: variables = cells, domain = 1–9, constraints = no repeats in row/column/box.

### 3.3 Path Optimization / Route Finder (`path_optimization.py`)
A Tkinter GUI simulating a 12-node road network (Kathmandu-area localities) with adjustable edge distances and traffic multipliers. It uses **Dijkstra's Algorithm** (via a priority queue / `heapq`) to compute the shortest weighted path between a selected start and destination, then animates an agent moving along the calculated route. This demonstrates **informed/uninformed weighted-graph search** applied to a well-defined shortest-path problem.

## 4. Observations

| Program | Problem Type | Technique Used | Key Demonstration |
|---|---|---|---|
| Maze Solver | Well-Defined Problem | Backtracking (DFS) | Undoing failed paths, marking dead ends |
| Sudoku Solver | CSP | Backtracking + Constraint Checking | Row/column/box constraint validation |
| Path Optimization | Well-Defined Problem | Dijkstra's Algorithm (UCS-style) | Shortest path on a weighted graph |

- Backtracking was clearly visualized in both the maze and Sudoku solvers, showing how invalid states are abandoned and previous states restored.
- The route finder illustrated how uninformed weighted search (Dijkstra) guarantees the lowest-cost path, factoring in both distance and traffic multipliers.
- Together, the three programs cover both major problem categories from the theory: **well-defined problems** (maze, path optimization) and **CSPs** (Sudoku).

## 5. Conclusion

This lab provided hands-on understanding of how AI search techniques solve real problems. Backtracking proved effective for constraint-based and maze-navigation problems, while Dijkstra's algorithm efficiently solved the shortest-path (well-defined) problem. The visualizations reinforced the theoretical distinction between blind/uninformed search, constraint satisfaction, and cost-based pathfinding covered in the lab notes.
