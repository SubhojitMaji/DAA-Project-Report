from itertools import product
from math import inf


def minimum_team(manager):
    size = len(manager)
    if size == 0:
        return []

    roots = [employee_id for employee_id, boss in enumerate(manager) if boss == -1]
    if len(roots) != 1:
        raise ValueError("Expected exactly one CEO")
    children = [[] for _ in manager]
    for employee, boss in enumerate(manager):
        if boss == -1:
            continue
        if boss < 0 or boss >= size or boss == employee:
            raise ValueError("Invalid manager index")
        children[boss].append(employee)

    root = roots[0]
    order = [root]
    for employee in order:
        order.extend(children[employee])
    if len(order) != size:
        raise ValueError("The hierarchy is not a connected tree")

    def best_down(table, parent_flag, grandparent_flag,
                  co_worker_flag, root_flag):
        value0 = table[parent_flag, grandparent_flag,
                       co_worker_flag, root_flag, 0]
        value1 = table[parent_flag, grandparent_flag,
                       co_worker_flag, root_flag, 1]
        return (value0, 0) if value0 <= value1 else (value1, 1)

    tables = [None] * size
    decisions = [None] * size

    for employee in reversed(order):
        child_list = children[employee]
        table = {state: inf for state in product((0, 1), repeat=5)}
        saved = {}

        for state in product((0, 1), repeat=5):
            parent_flag, grandparent_flag, co_worker_flag, root_flag, down_flag = state
            if root_flag and not down_flag:
                continue
            best_cost, best_plan = inf, None

            if down_flag == root_flag:
                costs = [0, inf]
                back = []
                for child in child_list:
                    next_costs = [inf, inf]
                    previous = [None, None]
                    for old_or in (0, 1):
                        for child_down in (0, 1):
                            new_or = old_or | child_down
                            value = tables[child][root_flag, parent_flag,
                                                  0, 0, child_down]
                            candidate = costs[old_or] + value
                            if candidate < next_costs[new_or]:
                                next_costs[new_or] = candidate
                                previous[new_or] = (old_or, child_down)
                    costs, back = next_costs, back + [previous]

                valid_or = (0, 1) if (root_flag or parent_flag or
                                      grandparent_flag or co_worker_flag) else (1,)
                final_or = min(valid_or, key=lambda flag: costs[flag])
                candidate = costs[final_or]
                if candidate < inf:
                    child_flags = [0] * len(child_list)
                    current_or = final_or
                    for index in range(len(child_list) - 1, -1, -1):
                        current_or, child_flags[index] = back[index][current_or]
                    best_cost = candidate
                    best_plan = [(0, 0, flag) for flag in child_flags]

            if down_flag:
                unselected_costs, unselected_down_flags, selected_costs = [], [], []
                for child in child_list:
                    child_table = tables[child]
                    value, flag = best_down(child_table, root_flag,
                                             parent_flag, 1, 0)
                    unselected_costs.append(value)
                    unselected_down_flags.append(flag)
                    selected_costs.append(
                        child_table[root_flag, parent_flag, 0, 1, 1]
                    )

                prefix = [0]
                for value in unselected_costs:
                    prefix.append(prefix[-1] + value)
                suffix = [0] * (len(child_list) + 1)
                for index in range(len(child_list) - 1, -1, -1):
                    suffix[index] = suffix[index + 1] + unselected_costs[index]

                one_cost, one_index = inf, None
                for index in range(len(child_list)):
                    candidate = (selected_costs[index] + prefix[index] +
                                 suffix[index + 1])
                    if candidate < one_cost:
                        one_cost, one_index = candidate, index
                if one_cost < best_cost:
                    best_cost = one_cost
                    best_plan = [
                        (1, 0, 1) if other == one_index else
                        (0, 1, unselected_down_flags[other])
                        for other in range(len(child_list))
                    ]

                counts, back = [0, inf, inf], []
                for child in child_list:
                    child_table = tables[child]
                    free_cost, unselected_down_flag = best_down(
                        child_table, root_flag, parent_flag, 1, 0
                    )
                    options = [
                        (0, unselected_down_flag, free_cost),
                        (1, 1, child_table[root_flag, parent_flag, 1, 1, 1])
                    ]
                    next_counts = [inf, inf, inf]
                    previous = [None, None, None]
                    for old_count in range(3):
                        for child_flag, child_down, value in options:
                            new_count = min(2, old_count + child_flag)
                            candidate = counts[old_count] + value
                            if candidate < next_counts[new_count]:
                                next_counts[new_count] = candidate
                                previous[new_count] = (
                                    old_count, child_flag, child_down
                                )
                    counts, back = next_counts, back + [previous]

                if counts[2] < best_cost:
                    plan = [(0, 1, 0)] * len(child_list)
                    count = 2
                    for index in range(len(child_list) - 1, -1, -1):
                        count, child_flag, child_down = back[index][count]
                        plan[index] = (child_flag, 1, child_down)
                    best_cost, best_plan = counts[2], plan

            if best_cost < inf:
                table[state] = root_flag + best_cost
                saved[state] = best_plan

        tables[employee], decisions[employee] = table, saved

    _, root_flag, down_flag = min(
        (tables[root][0, 0, 0, root_flag, down_flag], root_flag, down_flag)
        for root_flag in (0, 1) for down_flag in (0, 1)
    )
    team, stack = [], [(root, 0, 0, 0, root_flag, down_flag)]
    while stack:
        employee, parent_flag, grandparent_flag, co_worker_flag, root_flag, down_flag = stack.pop()
        if root_flag:
            team.append(employee)
        plan = decisions[employee][
            parent_flag, grandparent_flag, co_worker_flag, root_flag, down_flag
        ]
        for child, (child_flag, child_co_worker, child_down) in zip(
                children[employee], plan):
            stack.append((child, root_flag, parent_flag, child_co_worker,
                          child_flag, child_down))
    return team


if __name__ == "__main__":
    manager = [-1, 0, 0, 1, 1, 2]
    print("Selected employees:",
          [employee + 1 for employee in minimum_team(manager)])
