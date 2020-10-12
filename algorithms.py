import queue


def get_neighbors(pos, cell_map):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    #if (pos[0] + pos[1]) % 2 == 0:  # this is to enable zick-zack movement,
    #    directions.reverse()       # only works for breadth first search (why?)
    neighbors = []
    for d in directions:
        neighbor = (pos[0] + d[0], pos[1] + d[1])
        if (neighbor in cell_map
                and cell_map[neighbor]["type"] == "walkable"):
            neighbors.append(neighbor)
    return neighbors


def distance(a, b):
    """Returns the manhattan distance between the two points a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def breadth_first_search(cell_map, start, finish):
    frontier = queue.Queue()
    frontier.put(start)
    came_from = {start: None}
    while not frontier.empty():
        pos = frontier.get()
        if pos == finish:
            break
        for new_pos in get_neighbors(pos, cell_map):
            if new_pos not in came_from:
                frontier.put(new_pos)
                came_from[new_pos] = pos
    frontier_list = []
    while not frontier.empty():
        frontier_list.append(frontier.get())
    return frontier_list, came_from


def dijkstras_algorithm(cell_map, start, finish):
    frontier = queue.PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    while not frontier.empty():
        pos = frontier.get()[1]
        if pos == finish:
            break
        for new_pos in get_neighbors(pos, cell_map):
            new_cost = cost_so_far[pos] + cell_map[new_pos]["cost"]
            if (new_pos not in cost_so_far
                    or new_cost < cost_so_far[new_pos]):
                cost_so_far[new_pos] = new_cost
                came_from[new_pos] = pos
                frontier.put((new_cost, new_pos))
    frontier_list = []
    while not frontier.empty():
        frontier_list.append(frontier.get()[1])
    return frontier_list, came_from


def greedy_best_first_search(cell_map, start, finish):
    frontier = queue.PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    while not frontier.empty():
        pos = frontier.get()[1]
        if pos == finish:
            break
        for new_pos in get_neighbors(pos, cell_map):
            if new_pos not in came_from:
                priority = distance(new_pos, finish)
                frontier.put((priority, new_pos))
                came_from[new_pos] = pos
    frontier_list = []
    while not frontier.empty():
        frontier_list.append(frontier.get()[1])
    return frontier_list, came_from


def a_star(cell_map, start, finish):
    frontier = queue.PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    while not frontier.empty():
        pos = frontier.get()[1]
        if pos == finish:
            break
        for new_pos in get_neighbors(pos, cell_map):
            new_cost = cost_so_far[pos] + cell_map[new_pos]["cost"]
            if (new_pos not in cost_so_far
                    or new_cost < cost_so_far[new_pos]):
                cost_so_far[new_pos] = new_cost
                priority = new_cost + distance(new_pos, finish)
                frontier.put((priority, new_pos))
                came_from[new_pos] = pos
    frontier_list = []
    while not frontier.empty():
        frontier_list.append(frontier.get()[1])
    return frontier_list, came_from
