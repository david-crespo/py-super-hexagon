from heap import Heap
import random

random.seed()

def find_path(start, goal_r, walls_arr):
    closedset = set()    # The set of nodes already evaluated.
    openset = Heap([start], build_comparer(walls_arr))    # The set of tentative nodes to be evaluated, initially containing the start node
    came_from = dict()   # The map of navigated nodes.

    g_score = {}
    f_score = {}

    g_score[start] = 0    # Cost from start along best known path.
    # Estimated total cost from start to goal through y.
    f_score[start] = g_score[start] + heuristic_cost_estimate(start, goal_r)

    while openset.array: # while it's not empty
        current = openset.pop()
        # print 'current: (%d, %d)' % current
        if current[1] == goal_r:
            return reconstruct_path(came_from, current)

        closedset.add(current)
        for neighbor in neighbor_nodes(current, walls_arr):
            if neighbor in closedset:
                continue
            tentative_g_score = g_score[current] + dist_between(current,neighbor)

            if not openset.contains(neighbor) or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal_r)
                openset.push(neighbor)

    return None


def dist_between(current, neighbor):
    return 1


def wall_proximity(point, walls_arr, r=3):
    xbound, ybound = walls_arr.shape
    x, y = point
    xmin = max(0, x-r)
    ymin = max(0, y-r)
    xmax = min(xbound, x+r)
    ymax = min(ybound, y+r)

    total = 0
    for i in range(xmin, xmax):
        for j in range(ymin, ymax):
            if walls_arr[i,j]: total += 1

    return float(total) / ((ymax-ymin)*(xmax-xmin))


def neighbor_nodes(current, walls_arr):
    neighbors = set()
    x, y = current
    xmax, ymax = walls_arr.shape

    if x == xmax - 1: # wrap around
        x_up = 0
    else:
        x_up = x + 1

    if x == 0: # wrap around
        x_down = xmax - 1
    else:
        x_down = x - 1

    if y+1 < ymax  and not walls_arr[x, y+1]: neighbors.add((x,y+1))
    if not walls_arr[x_up, y]: neighbors.add((x_up,y))
    if not walls_arr[x_down, y]: neighbors.add((x_down,y))

    return neighbors


def heuristic_cost_estimate(a, goal_r):
    return abs(goal_r - a[1])

def build_comparer(walls_arr):
    def comparer(a, b):
        is_farther_out = int(a[1] > b[1])
        has_more_space = int(wall_proximity(a, walls_arr) < wall_proximity(b, walls_arr))
        r_var = random.randint(0,1)
        return (0.2 * is_farther_out + 0.6 * has_more_space + 0.2 * r_var) > 0.5

    return comparer

def reconstruct_path(came_from, current_node):
    if current_node in came_from:
        p = reconstruct_path(came_from, came_from[current_node])
        p.append(current_node)
        return p
    else:
        return [current_node]