from heap import Heap

def find_path(start, goalset, walls_arr):
    closedset = set()    # The set of nodes already evaluated.
    openset = Heap([start], is_farther_out)    # The set of tentative nodes to be evaluated, initially containing the start node
    came_from = dict()   # The map of navigated nodes.

    g_score = {}
    f_score = {}

    g_score[start] = 0    # Cost from start along best known path.
    # Estimated total cost from start to goal through y.
    f_score[start] = g_score[start] + heuristic_cost_estimate(start, goalset)

    while openset.nodes: # while it's not empty
        current = openset.pop()
        if current in goalset:
            return reconstruct_path(came_from, current)

        openset.remove(current)
        closedset.add(current)
        for neighbor in neighbor_nodes(current):
            if neighbor in closedset:
                continue
            tentative_g_score = g_score[current] + dist_between(current,neighbor)

            if not openset.contains(neighbor) or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
                openset.push(neighbor)

    return failure


def dist_between(current, neighbor):
    return 1


def neighbor_nodes(current, walls_arr):
    neighbors = set()
    x, y = current
    xmax, ymax = walls_arr.shape

    if x+1 <= xmax and not walls_arr[x+1, y]: neighbors.add((x,y))
    if y+1 <= ymax and not walls_arr[x, y+1]: neighbors.add((x,y))
    if y-1 >= 0    and not walls_arr[x, y-1]: neighbors.add((x,y))

    return neighbors


def heuristic_cost_of_traveling(a, goalset):
    return abs(goalset.x_coord - a[0])

def is_farther_out(a, b):
    # x value is farther to the right in the transformed picture, i.e.,
    # farther out from the center in-game
    return a[0] > b[0]

def reconstruct_path(came_from, current_node):
    if current_node in came_from:
        p = reconstruct_path(came_from, came_from[current_node])
        p.append(current_node)
        return p
    else:
        return [current_node]