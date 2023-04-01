def manhattan_distance(current, goal):
    # Compute the Manhattan distance between two points
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def a_star(grid, start, goal):
    # Set of nodes already evaluated
    closed_set = set()
    # The set of currently discovered nodes that are not evaluated yet.
    open_set = {start}
    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually contain the
    # most efficient previous step.
    came_from = dict()
    # For each node, the cost of getting from the start node to that node.
    g_score = {start: 0}
    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    h_score = {start: manhattan_distance(start, goal)}
    f_score = {start: manhattan_distance(start, goal)}

    while open_set:
        # current = min(open_set, key=lambda x: f_score[x])
        current = min({k: v for k, v in f_score.items() if v <=
                       min(f_score.values())}, key=lambda x: h_score[x])
        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in neighbors(grid, current):
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + \
                movement_cost(current, neighbor)

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            h_score[neighbor] = manhattan_distance(neighbor, goal)
            f_score[neighbor] = g_score[neighbor] + h_score[neighbor]

    return None


def my_a_star(grid, start, end):
    open_set = {start}
    close_set = set()
    came_from = dict()
    g_score = {start: 0}
    h_score = {start: manhattan_distance(start, end)}
    f_score = {start: manhattan_distance(start, end)}

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        open_set.remove(current)

        for successor in neighbors(grid, current):
            if successor == end:
                return reconstruct_path(came_from, successor)

            successor_g = g_score[current]+movement_cost(current, successor)
            successor_h = manhattan_distance(successor, end)
            successor_f = successor_g+successor_h
            if successor in open_set:
                if successor_f >= f_score[successor]:
                    continue
            if successor in close_set:
                if successor_f >= f_score[successor]:
                    continue
            open_set.add(successor)
            came_from[successor] = current
            g_score[successor] = successor_g
            h_score[successor] = successor_h
            f_score[successor] = successor_f

            close_set.add(current)

    return None


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return list(reversed(total_path))


def neighbors(grid, current):
    x, y = current
    width, height = len(grid[0]), len(grid)
    results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
    results = filter(lambda x: 0 <= x[0] < width and 0 <=
                     x[1] < height and grid[x[1]][x[0]] != 'x', results)
    return results


def movement_cost(current, neighbor):
    return 1


grid = [[0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6],
        [0, 1, 2, 3, 4, 5, 6]]
print(a_star(grid, (1, 0), (2, 3)))
# print(my_a_star(grid, (0, 0), (3, 4)))
# open = ((2, 0), (3, 1))
# a = {(1, 1): 5, (1, 0): 5, (2, 0): 3, (2, 1): 4, (3, 1): 3}
# h = {(1, 1): 3, (1, 0): 3, (2, 0): 1, (2, 1): 2, (3, 1): 0}
# min_a_ = min(a.values())

# # print(type(min_a_))
# b = {k: v for k, v in a.items() if v <= min_a_}
# print(min(b, key=lambda x: h[x]))
