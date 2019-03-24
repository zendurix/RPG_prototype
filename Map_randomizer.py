from obstacleClass import Obstacle
from random import randint
from fieldClass import *
from os import system


testing = False  # set this to True, to test only Map randomizer

if testing:
    # RANDOMIZER FOR WALLS (entire field is empty)
    # ROOM RANDOM SIZE
    # From:
    a = 4    # (a > 3)
    # To:
    b = 14
    # MAP SIZE (> b):
    size = 40

# not yet used
class Corridor:
    def __init__(self):
        self.width = 1
        self.connections = 2


class Room:
    count = 0

    def __init__(self, size, a, b):
        if Room.count == int(int(size / b)/2):
            a /= 2
            if a < 4:
                a = 4
            b /= 2
            if b < 4:
                b = 4
        self.size = randint(a, b)
        self.entrances = randint(1, 3)
        self.placed = False
        Room.count += 1

    def place_entrance(self, field, x_start, y_start):
        entrances_placed = 0
        for i in range(self.entrances):
            while entrances_placed != i+1:
                x = randint(x_start, x_start + self.size - 1)
                y = randint(y_start, y_start + self.size - 1)

                if field[y][x].obstacle_here:
                    field[y][x].obstacle_here = None
                    field[y][x].is_door = True
                    field[y][x].leave()
                    entrances_placed += 1


    def make_room(self, field, x , y):
        x_start = x
        y_start = y
        counter = 0
        collision = False


        try:
            field[y+self.size][x+self.size]
        except IndexError:
            return 0

        for yy in range(self.size+4):
            for xx in range(self.size+4):
                try:
                    if field[yy+y_start-2][xx+x_start-2].obstacle_here is not None or field[yy+y_start-2][xx+x_start-2].is_in_room:
                        collision = True
                except IndexError:
                    pass

        if not collision:
            for yy in range(self.size):
                if counter == 0 or counter == self.size - 1:
                    for xx in range(self.size):
                        field[y][x].obstacle_here = Obstacle(x, y, 1, field)
                        x += 1
                elif counter > 0 and counter < self.size - 1:
                    for xx in range(self.size):
                        field[y][x].is_in_room = True
                        field[y][x].print_format = ' '
                        x += 1
                    field[y][x_start].obstacle_here = Obstacle(x_start, y, 1, field)
                    field[y][x_start].is_in_room = False
                    field[y][x_start].print_format = '#'
                    field[y][x_start + self.size - 1].obstacle_here = Obstacle(x_start + self.size - 1, y, 1, field)
                    field[y][x_start + self.size - 1].is_in_room = False
                    field[y][x_start + self.size - 1].print_format = '#'

                x = x_start
                y += 1
                counter += 1
            self.placed = True
            self.place_entrance(field, x_start, y_start)
        else:
            return 0


def random_map(size, field, maximum, a, b):

    rooms_quantinty = int(size / maximum) * 2
    rooms = []
    for i in range(rooms_quantinty):
        rooms.append(Room(size, a, b))

    for room in rooms:
        while not room.placed:
            x = randint(0, size)
            y = randint(0, size)
            room.make_room(field, x, y)

    return field


def print_field(field):
    system("cls")
    print('')
    for line in field:
        for spot in line:
            print(spot.print_format, " ", end=' ')
        print('')



if testing:

    field = [[Place(Place.x, Place.y, size) for x in range(size)] for y in range(size)]


    random_map(size, field, b+1, a , b)
    print_field(field)











# Randomizer for empty rooms (all field is wall)
'''
from obstacleClass import Obstacle
from random import randint
from fieldClass import *
from os import system

# ROOM RANDOM SIZE
# From:
a = 3    # (a > 2)
# To:
b = 8

# MAP SIZE (> b):
size = 40

# not yet used
class Corridor:
    def __init__(self):
        self.width = 1
        self.connections = 2


class Room:
    count = 0

    def __init__(self, size, a, b):
        if Room.count == int(int(size / b )/2):
            a /= 2
            if a < 3:
                a = 3
            b /= 2
        self.size = randint(a, b)
        self.entrances = 1
        self.placed = False
        Room.count += 1

    def make_room(self, field, x , y):
        x+=1
        y+=1
        x_start = x
        y_start = y
        collision = False

        try:
            field[y+self.size][x+self.size]
        except IndexError:
            return 0

        for yy in range(self.size):
            for xx in range(self.size):
                if field[yy+y_start][xx+x_start].obstacle_here is None or field[yy+y_start][xx+x_start].is_in_room:
                    collision = True

        if not collision:
            for yy in range(self.size-1):
                for xx in range(self.size-1):
                    field[y][x].obstacle_here = None
                    field[y][x].leave()
                    field[y][x].is_in_room = True
                    x += 1

                x = x_start
                y += 1

            self.placed = True
        else:
            return 0


def random_map(size, field, maximum, a, b):

    rooms_quantinty = int(size / maximum) * 2
    rooms = []
    for i in range(rooms_quantinty):
        rooms.append(Room(size, a, b))

    for room in rooms:
        while not room.placed:
            x = randint(0, size)
            y = randint(0, size)
            room.make_room(field, x, y)

    return field


def print_field(field):
    system("cls")
    print('')
    for line in field:
        for spot in line:
            print(spot.print_format, " ", end=' ')
        print('')



field = [[Place(Place.x, Place.y, size) for x in range(size)] for y in range(size)]
for xx, line in enumerate(field):
    for yy, place in enumerate(line):
        place.obstacle_here = Obstacle(xx, yy, 1, field)

random_map(size, field, b+1, a, b)
print_field(field)
'''

