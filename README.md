# DAA Project Report

This repository contains our group project submission for **Design and Analysis of Algorithms (DAA)**, a course in Semester 5.

## About the Project

The project involves finding a minimum-cost team from a company hierarchy, where each employee reports to a manager and the CEO is at the top.

We use **tree dynamic programming** to solve the problem. The main idea is to process employees from the bottom of the hierarchy upwards, so that whenever we consider a manager, we have already computed the results for everyone reporting to them.

For each possible state, we calculate the minimum cost and keep track of the choices that produced it. This allows us to reconstruct the actual team after finding the optimal cost.

## How the Algorithm Works

We first build the hierarchy using the manager information given for each employee. Starting from the CEO, we generate an ordering in which managers appear before their reports.

We then process this order in reverse. This ensures that all the children of an employee have been processed before we compute the employee's DP states.

Each state is represented by five flags, `(a, b, s, x, t)`. Depending on their values, we consider three different cases:

- **Case 1:** When `t = x`, we use a two-state table to combine the results of the children. If the employee is not already covered by another condition, we require at least one child to have `t_c = 1`.
- **Case 2:** When `t = 1`, we use prefix and suffix sums to evaluate the possible choices efficiently.
- **Case 3:** Also when `t = 1`, we use a count-based table with three states (`0`, `1`, and `2+`) to keep track of the required number of children.

In each case, we compare the possible costs and save the choices corresponding to the minimum.

## Pseudocode

```text
Minimum-Team(manager[0..n-1])

    Build a list of children for each employee.

    Build an order starting from the CEO, with
    every manager appearing before their reports.

    For each employee u in reverse order:

        For each flag tuple (a, b, s, x, t):

            If x = 1 and t = 0:
                Skip this state.

            best = infinity

            If t = x:

                Evaluate Case 1 using a two-state
                table over the values t_c.

                Require at least one t_c = 1
                only if nothing else covers u.

                Save the minimum cost and its choices.

            If t = 1:

                Evaluate Case 2 using prefix
                and suffix sums.

                Save the minimum cost and its choices.

                Evaluate Case 3 using a count
                table over states 0, 1, and 2+.

                Save the minimum cost and its choices.

            If best is finite:

                D_u = x + best

                Save the choices that give D_u.

    At the CEO, set a = b = s = 0.

    Choose the smallest finite value over x and t.

    Follow the saved choices to reconstruct the team.

    Return the team.
```

## Reconstructing the Team

Finding the minimum cost is only one part of the problem. We also need to identify which employees belong to the team.

To do this, we store the decisions made while calculating each DP state. Once all states have been evaluated, we go back to the CEO and set `a = b = s = 0`.

We then choose the combination of `x` and `t` that gives the smallest finite cost. Starting from this state, we follow the saved choices down the hierarchy to recover the employees selected for the team.

This way, we get both the minimum cost and the corresponding team without having to solve the problem again.

---

**Course:** Design and Analysis of Algorithms (DAA)  
**Semester:** 5  
**Project:** Group Submission
