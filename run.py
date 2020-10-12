import os
import sys
import pygame as pg
import algorithms


FPS = 60
CELL_SIZE = 30

MAP_LEGEND = {"start": "S",
              "finish": "F",
              "wall": "#"}

COST = {".": 1,
        ":": 5,
        "/": 10}

COLORS = {"background": (255, 255, 255),
          "start": (128, 255, 128),
          "finish": (255, 145, 145),
          "wall": (0, 0, 0),
          "walkable": (130, 130, 130),
          "frontier": (150, 150, 255),
          "came_from": (210, 210, 255),
          "path": (0, 0, 0),
          1: (255, 255, 255),
          5: (200, 200, 200),
          10: (150, 150, 150)}


ALGORITHMS = (algorithms.breadth_first_search,
              algorithms.greedy_best_first_search,
              algorithms.dijkstras_algorithm,
              algorithms.a_star)


def read_map(filename):
    char_map = []
    with open(filename) as f:
        width, heigth = (int(i) for i in f.readline().split(","))
        for line in f:
            row = list(line)
            if "\n" in row:
                row.remove("\n")
            char_map.append(row)

    return width, heigth, char_map


def create_cell_map(char_map):
    cell_map = {}
    for y, row in enumerate(char_map):
        for x, char in enumerate(row):
            pos = (x, y)
            cell = {}
            if char == MAP_LEGEND["wall"]:
                cell["type"] = "wall"
            else:
                cell["type"] = "walkable"
                cell["cost"] = COST.get(char, 1)
            # add cell to map:
            cell_map[pos] = cell
    return cell_map


def find_start_finish(char_map):
    start, finish = None, None
    for y, row in enumerate(char_map):
        for x, char in enumerate(row):
            pos = (x, y)
            if char == MAP_LEGEND["start"]:
                start = pos
            elif char == MAP_LEGEND["finish"]:
                finish = pos
    return start, finish


def draw_map(screen, cell_map, start, finish, frontier, came_from, path):
    screen.fill(COLORS["background"])

    for pos, cell in cell_map.items():
        if cell["type"] == "walkable":
            pg.draw.rect(screen, COLORS[cell["cost"]],
                         (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE,
                          CELL_SIZE, CELL_SIZE), 0)
            width = 1  # draws only the border of the rect
        else:
            width = 0  # rect is filled
        pg.draw.rect(screen, COLORS[cell["type"]],
                     (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE,
                      CELL_SIZE, CELL_SIZE), width)

    offset = 2
    for pos in came_from:
        pg.draw.rect(screen, COLORS["came_from"],
                     (pos[0]*CELL_SIZE+offset, pos[1]*CELL_SIZE+offset,
                      CELL_SIZE-offset*2, CELL_SIZE-offset*2), offset * 2)
    for pos in frontier:
        pg.draw.rect(screen, COLORS["frontier"],
                     (pos[0]*CELL_SIZE+offset, pos[1]*CELL_SIZE+offset,
                      CELL_SIZE-offset*2, CELL_SIZE-offset*2), offset * 2)

    pg.draw.rect(screen, COLORS["start"],
                 (start[0]*CELL_SIZE, start[1]*CELL_SIZE,
                  CELL_SIZE, CELL_SIZE), 0)
    pg.draw.rect(screen, COLORS["finish"],
                 (finish[0]*CELL_SIZE, finish[1]*CELL_SIZE,
                  CELL_SIZE, CELL_SIZE), 0)

    offset = CELL_SIZE // 3
    for pos in path:
        pg.draw.rect(screen, COLORS["path"],
                     (pos[0]*CELL_SIZE+offset, pos[1]*CELL_SIZE+offset,
                      offset, offset), 0)


def move_cell(pos, button, cell_map, start, finish):
    # convert screen coords to cell coords:
    cell_pos = tuple([int(i/CELL_SIZE) for i in pos])

    if cell_map[cell_pos]["type"] == "walkable":
        if button == 1:
            start = cell_pos
        elif button == 3:
            finish = cell_pos
        else:
            return cell_map

    return start, finish


def find_path(start, finish, came_from):
    pos = finish
    path = [pos]
    while pos != start:
        pos = came_from[pos]
        path.append(pos)
    return path


def next_algorithm(algo):
    next_index = (ALGORITHMS.index(algo) + 1) % len(ALGORITHMS)
    new_algo = ALGORITHMS[next_index]
    print("Current algorithm: ", new_algo.__name__)
    return new_algo


def main_loop(map_name):
    width, heigth, char_map = read_map(map_name)
    cell_map = create_cell_map(char_map)
    start, finish = find_start_finish(char_map)
    screen = pg.display.set_mode([width*CELL_SIZE, heigth*CELL_SIZE])
    pg.display.set_caption("Pathfinding")
    algorithm = algorithms.breadth_first_search
    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    running = False
                elif e.key == pg.K_SPACE:
                    algorithm = next_algorithm(algorithm)
            elif e.type == pg.MOUSEBUTTONDOWN:
                start, finish = move_cell(e.pos, e.button, cell_map,
                                          start, finish)
        frontier, came_from = algorithm(cell_map, start, finish)
        path = find_path(start, finish, came_from)
        caption = "Path length = " + str(len(path))
        pg.display.set_caption(caption)
        draw_map(screen, cell_map, start, finish, frontier, came_from, path)
        pg.display.update()
        CLOCK.tick(FPS)
    pg.display.quit()


def console_loop():
    """choose map, execute main loop, exit program, maybe display other stuff"""
    while True:
        map_name = get_map_name()
        main_loop(map_name)


def get_map_name():
    while True:
        print("-"*33, "\n")
        name = input("Enter the name of the map.\n> ")
        filename = name + ".txt"
        if os.path.exists(filename):
            return filename
        else:
            print("There is no such file in the directory. Please try again.\n")


if __name__ == "__main__":
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pg.init()
    CLOCK = pg.time.Clock()
    console_loop()
    pg.quit()
    sys.exit()
