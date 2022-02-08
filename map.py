import random
import copy
import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (item, priority))

    def get(self):
        return heapq.heappop(self.elements)[0]


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def neighbors(dist, point):
    ddx = [0, 1, 0, -1]
    ddy = [-1, 0, 1, 0]
    y, x = point
    neighbors = []
    for i in range(len(ddy)):
        if 0 < y + ddy[i] < len(dist) and 0 < x + ddx[i] < len(dist[0]):
            neighbors.append((y + ddy[i], x + ddx[i]))
    return neighbors


def a_star_search(dist, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    while frontier.empty() is False:
        current = frontier.get()
        if current == goal:
            break
        for next in neighbors(dist, current):
            y, x = next
            new_cost = cost_so_far[current] + dist[y][x]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from


class Map:
    def __init__(self, width=100, height=32):
        self.width = width
        self.height = height
        self.cost_wall = 10
        self.cost_room = 5
        self.cost_room_wall = 15
        self.cost_frontier = 100000
        self.map = self.generate_map()

    def draw_in_terminal(self):
        print('-' * 150)
        for y in range(self.height):
            for x in range(self.width):
                print('@' if self.map[y][x] is True else '#', end=' ')
            print()
        print('-' * 150)

    def generate_map(self):
        def draw_in_terminal_dist():
            print('-' * 150)
            for y in range(len(dist)):
                for x in range(len(dist[0])):
                    print(' ' if dist[y][x] == self.cost_room else '$' if dist[y][x] == self.cost_frontier or dist[y][
                        x] == self.cost_room_wall else '#', end=' ')
                print()
            print('-' * 150)

        def init_dist():
            width_d = self.width + 2
            height_d = self.height + 2
            dist = [[self.cost_frontier] * width_d if i == 0 or i == height_d - 1
                    else [self.cost_frontier] + [self.cost_wall] * self.width + [self.cost_frontier] for i in
                    range(height_d)]
            return dist

        def get_all_coord():
            coords = []
            for y in range(len(dist)):
                for x in range(len(dist[0])):
                    coords.append((y, x))
            return coords

        def get_field_coord():
            coords = []
            for y in range(len(dist)):
                for x in range(len(dist[0])):
                    if dist[y][x] == self.cost_room:
                        coords.append((y, x))
            return coords

        def make_room(max_width_rect=8, max_height_rect=8):
            count_rect = random.randint(2, 5)
            room = [[-1] * (max_width_rect * count_rect + 2) if i == 0 or i == (max_height_rect * count_rect + 1) else
                    [-1] + [0] * max_width_rect * count_rect + [-1] for i in range(max_height_rect * count_rect + 2)]
            field_room = []

            def make_rectangle():
                width = random.randint(3, max_width_rect)
                height = random.randint(3, max_height_rect)

                rect = [[1] * width for _ in range(height)]

                return rect

            def gluing(room, field_room, rect):
                if len(field_room) == 0:
                    for y in range(1, len(rect[0]) + 1):
                        for x in range(1, len(rect) + 1):
                            room[y][x] = 1
                            field_room.append((y, x))
                else:
                    new_room = copy.deepcopy(room)
                    new_field_room = field_room
                    local_field_room = field_room
                    gluing_finish = False
                    while len(local_field_room) and gluing_finish is False:
                        var = random.randint(0, len(local_field_room) - 1)
                        i = local_field_room[var][0]
                        j = local_field_room[var][1]
                        flag = True
                        for y in range(len(rect[0])):
                            for x in range(len(rect)):
                                if y + i < len(room) and x + j < len(room[0]) and room[y + i][x + j] != -1:
                                    new_room[y + i][x + j] = 1
                                    if ((y + i, x + j) in new_field_room) is False:
                                        new_field_room.append((y + i, x + j))
                                else:
                                    flag = False
                        if flag is False:
                            new_room = room
                            new_field_room = field_room
                            local_field_room.remove(local_field_room[var])
                        else:
                            gluing_finish = True
                            field_room = new_field_room
                            room = new_room

            for _ in range(count_rect):
                rect = make_rectangle()
                gluing(room, field_room, rect)

            return field_room

        def lock_neighbors(y, x):
            for i in range(len(ddy)):
                if 0 < y + ddy[i] < len(dist) and 0 < x + ddx[i] < len(dist[0]) \
                        and dist[y + ddy[i]][x + ddx[i]] == self.cost_wall:
                    dist[y + ddy[i]][x + ddx[i]] = self.cost_room_wall

        def paste_room_to_dist(dist, field_dist):
            new_dist = copy.deepcopy(dist)
            new_field_dist = copy.deepcopy(field_dist)
            lc_field_dist = []
            paste_finish = False
            while len(coords) and paste_finish is False:
                var = random.randint(0, len(coords) - 1)
                flag = True
                i = coords[var][0]
                j = coords[var][1]
                for coord in field_room:
                    y = coord[0]
                    x = coord[1]
                    if y + i < len(dist) and x + j < len(dist[0]) and new_dist[y + i][x + j] != self.cost_frontier and \
                            new_dist[y + i][x + j] != self.cost_room_wall:
                        new_dist[y + i][x + j] = self.cost_room
                        new_field_dist.append((y + i, x + j))
                        lc_field_dist.append((y + i, x + j))
                    else:
                        flag = False
                if flag is False:
                    coords.remove(coords[var])
                    new_dist = copy.deepcopy(dist)
                    new_field_dist = copy.deepcopy(field_dist)
                    lc_field_dist = []
                else:
                    paste_finish = True
                    dist = copy.deepcopy(new_dist)
                    field_dist = copy.deepcopy(new_field_dist)

                    # coords_field_dist = get_field_coord()
                    # if len(coords_field_dist):
                    #     create_tunnel(i, j, coords_field_dist)
            return dist, field_dist, lc_field_dist

        def recovery_road(came_from, current, road):
            if came_from[current] is None:
                return road
            road.append(came_from[current])
            return recovery_road(came_from, road[-1], road)

        def create_tunnel(coords_field_dist, lc_field_dist):
            # coords_field_dist = get_field_coord()
            start = lc_field_dist[random.randint(0, len(lc_field_dist) - 1)]
            goal = coords_field_dist[random.randint(0, len(coords_field_dist) - 1)]
            came_from = a_star_search(dist, start, goal)
            road = recovery_road(came_from, goal, [])
            for coord in road:
                y, x = coord
                dist[y][x] = self.cost_room
                lock_neighbors(y, x)
                # draw_in_terminal_dist()
            # draw_in_terminal_dist()
            # print(road)

        dist = init_dist()
        field_dist = []
        coords = get_all_coord()
        ddx = [0, 1, 0, -1]
        ddy = [-1, 0, 1, 0]

        count_room = 10
        for i in range(count_room):
            field_room = make_room()
            coords_field_dist = get_field_coord()
            dist, field_dist, lc_field_dist = paste_room_to_dist(dist, field_dist)
            for coord in lc_field_dist:
                lock_neighbors(coord[0], coord[1])
            if i != 0 and len(lc_field_dist):
                create_tunnel(coords_field_dist, lc_field_dist)
        # draw_in_terminal_dist()
        map = [[0] * len(dist[0]) for _ in range(len(dist))]
        for y in range(len(dist)):
            for x in range(len(dist[0])):
                map[y][x] = (True if dist[y][x] == self.cost_room else False)

        return map


map = Map()