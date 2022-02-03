import random
import copy


class Map:
    def __init__(self, width=100, height=32):
        self.width = width
        self.height = height
        self.map = self.generate_map()

    def draw_in_terminal(self):
        print('-' * 150)
        for y in range(self.height):
            for x in range(self.width):
                print('@' if self.map[y][x] is True else '#', end='')
            print()
        print('-' * 150)

    def generate_map(self):
        def draw_in_terminal_dist(dist):
            print('-' * 150)
            for y in range(len(dist)):
                for x in range(len(dist[0])):
                    print(' ' if dist[y][x] == 1 else '$' if dist[y][x] == -1 else '#', end=' ')
                print()
            print('-' * 150)

        def init_dist(width, height):
            width_d = width + 2
            height_d = height + 2
            dist = [[-1] * width_d if i == 0 or i == height_d - 1 else [-1] + [0] * width + [-1] for i in
                    range(height_d)]
            return dist

        def get_all_coord(dist):
            coords = []
            for y in range(len(dist)):
                for x in range(len(dist[0])):
                    coords.append((y, x))
            return coords

        def make_room(distance=1, max_width_rect=8, max_height_rect=8):
            count_rect = random.randint(2, 5)
            room = [[-1] * (max_width_rect * count_rect + 2) if i == 0 or i == (max_height_rect * count_rect + 1) else [-1] +
                        [0] * max_width_rect * count_rect + [-1] for i in range(max_height_rect * count_rect + 2)]
            field_room = []

            def make_rectangle(max_width=max_width_rect, max_height=max_height_rect):
                width = random.randint(3, max_width)
                height = random.randint(3, max_height)

                # print("width_rect = ", width)
                # print("height_rect = ", height)
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

            return room, field_room

        def lock_neighbors(dist, x, y):
            for i in range(len(ddy)):
                for j in range(len(ddx)):
                    if dist[y + ddy[i]][x + ddx[j]] == 0:
                        dist[y + ddy[i]][x + ddx[j]] = -1

        def paste_room_to_dist(dist, field_dist, coords):
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
                    if y + i < len(dist) and x + j < len(dist[0]) and new_dist[y + i][x + j] != -1:
                        new_dist[y + i][x + j] = 1
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

            for coord in lc_field_dist:
                lock_neighbors(dist, coord[1], coord[0])

            return dist

        dist = init_dist(self.width, self.height)
        field_dist = []
        coords = get_all_coord(dist)
        ddx = [0, 1, 0, -1]
        ddy = [-1, 0, 1, 0]

        count_room = 10
        for _ in range(count_room):
            room, field_room = make_room()
            dist = paste_room_to_dist(dist, field_dist, coords)
        draw_in_terminal_dist(dist)
        # draw_in_terminal_dist(room)


map = Map()
