from itemClasses import *


class Place:
    dead_bodies = []
    db_index = -1

    x = 0
    y = 0

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.character_here = None
        self.obstacle_here = None
        self.items_here = []
        self.print_format = '.'
        self.is_in_room = False
        self.is_door = False
        Place.x += 1
        if Place.x == size:
            Place.x = 0
            Place.y += 1

    def goto(self, character):
        if character.is_obstacle:
            self.obstacle_here = character
        else:
            self.character_here = character
        self.print_format = character.print_format

    def leave(self):
        self.character_here = None
        if self.is_in_room:
            self.print_format = " "
        elif self.is_door:
            self.print_format = "+"
        else:
            self.print_format = "."

    def died_here(self, character):
        Place.dead_bodies.append(Dead_body("dead " + character.name, character.print_format))
        Place.db_index += 1
        self.items_here.append(Place.dead_bodies[Place.db_index])
        for i in character.inv:
            self.items_here.append(i)

