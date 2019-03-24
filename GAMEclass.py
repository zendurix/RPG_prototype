from Map_randomizer import *
from itemClasses import *
from instructions import *
from AI import AI
from termcolor import colored
from os import system
import math


class Game:

    def __init__(self, Place, size=20):
        self.field = [[Place(Place.x, Place.y, size) for x in range(size)] for y in range(size)]
        self.turn = 0

    def make_random_map(self, size=20):
        # ROOM RANDOM SIZE
        # From:
        a = 4  # (a > 3)
        # To:
        b = 8
        random_map(size, self.field, b + 1, a, b)

    def distance_meter1(self, obj1, obj2):
        x_1 = obj1.pos_x
        y_1 = obj1.pos_y
        x_2 = obj2.pos_x
        y_2 = obj2.pos_y
        return math.floor(math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2))

    def print_hp(self, character):
        print(character.name, " HP: [", end='')
        if character.alive:
            for i in range(character.hp):
                print(colored("O", 'red'), end='')
            for i in range(character.hp_max - character.hp):
                print("O", end='')
        else:
            print("DEAD", end="")

        print("]", end="")
        print("(", character.hp, "/", character.hp_max, ")", end="")

    def your_turn(self, you):
        direction = input()
        while direction not in ['1','2','3','4','5','6','7','8','9']:
            if direction == "s":
                you.search(self.field[you.pos_y][you.pos_x])

            elif direction == "i":
                you.print_inv()

            elif direction == "p":
                name = input("Write item to pick up name:")
                you.pick_up(self.field[you.pos_y][you.pos_x], name)

            elif direction == "e":
                name = input("Write item to equip name:")
                you.equip(name)

            elif direction == "d":
                name = input("Write item to deequip name:")
                you.deequip(name, self.field[you.pos_y][you.pos_x])

            elif direction == "help":
                print_help()
                system("cls")

            direction = input()

        you.move(direction, self.field)


    def enemy_turn(self, you, enemy):
        if enemy.alive:
            dist = math.floor(self.distance_meter1(you, enemy))
            ai = AI()
            ai.do_smth(enemy, you, dist, self.field)

    def distance_meter(self, obj1, obj2):
        x_1 = obj1.pos_x
        y_1 = obj1.pos_y
        x_2 = obj2.x
        y_2 = obj2.y
        return math.floor(math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2))





    def print_field_and_hp(self, character_list, you):
        system("cls")
        print('')
        x = 0
        for line in self.field:
            for spot in line:
                printed = False
                if spot.character_here is not None:
                    if not spot.character_here.ai:
                        print(colored(spot.print_format, 'green'), " ", end=' ')
                        printed = True
                    else:
                        print(colored(spot.print_format, 'red'), " ", end=' ')
                        printed = True
                if not printed:
                    for item in spot.items_here:
                        if type(item) == Dead_body:
                            if not printed:
                                print(colored(item.print_format, 'grey'), " ", end=' ')
                            printed = True
                    if (not printed) and (len(spot.items_here) > 0):
                        print(colored("!", 'yellow'), " ", end=' ')
                        printed = True
                if not printed:
                    try:
                        if self.distance_meter(you, spot)<= you.view:
                            print(colored(spot.print_format, "yellow"), " ", end=' ')
                        else:
                            print(spot.print_format, " ", end=' ')
                    except AttributeError:
                        print(spot.print_format, " ", end=' ')

                    printed = True
            if x < len(character_list):
                self.print_hp(character_list[x])
            if x == len(character_list):
                self.print_hp(you)
            if x == len(character_list)+1:
                print("EQ: ", end='')
                for item in you.equipment:
                    print(item.name, end=", ")

            print('')
            x += 1












# old, real time fight, can be used to test 1v1 fights :
'''          
def fight(char1, char2):
    clock_1 = time.time()
    clock_2 = time.time()
    while 1:
        if round(time.time() - clock_1, 3) == char1.atk_speed:
            char1.attack(char2)
            clock_1 = time.time()

        if round(time.time() - clock_2, 3) == char2.atk_speed:
            char2.attack(char1)
            clock_2 = time.time()

        if (not char1.alive) or (not char2.alive):
            print(char1.name, " is alive : ", char1.alive, " HP: ", char1.hp)
            print(char2.name, " is alive  : ", char2.alive, " HP: ", char2.hp)
            break
'''


