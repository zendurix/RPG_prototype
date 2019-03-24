from termcolor import colored
from os import system
import sys
import math



class Game:

    def __init__(self, Place, size=10):
        self.field = [[Place(Place.x, Place.y, size) for x in range(size)] for y in range(size)]
        self.turn = 0

    def distance_meter(self, obj1, obj2):
        x_1 = obj1.pos_x
        y_1 = obj1.pos_y
        x_2 = obj2.pos_x
        y_2 = obj2.pos_y
        return math.floor(math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2))

    def print_field(self):
        system("cls")
        print('')
        for line in self.field:
            for spot in line:
                if spot.character_here is not None:
                    if not spot.character_here.ai:
                        print(colored(spot.print_format, 'green'), " ", end=' ')
                    else:
                        print(colored(spot.print_format, 'red'), " ", end=' ')
                else:
                    print(spot.print_format, " ", end=' ')
            print('')

    def your_turn(self, you):
        direction = input()
        you.move(direction, self.field)

    def enemy_turn(self, you, field, enemy):
        if enemy.alive:
            dist = math.floor(self.distance_meter(you, enemy))
            ai = AI()
            ai.do_smth(enemy, you, dist, field)

class Place:

    x = 0
    y = 0

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.character_here = None
        self.obstacle_here = None
        self.print_format = '.'
        x += 1
        if x == size:
            x = 0
            y += 1

    def goto(self, character):
        if character.is_obstacle:
            self.obstacle_here = character
        else:
            self.character_here = character
        self.print_format = character.print_format

    def leave(self):
        self.character_here = None
        self.print_format = "."

class AI:

    def distance_meter(self, obj1, obj2):
        x_1 = obj1.pos_x
        y_1 = obj1.pos_y
        x_2 = obj2.pos_x
        y_2 = obj2.pos_y
        return math.floor(math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2))

    def do_smth(self, ai, you, distance, field):

        if distance == 1:
            ai.attack(field, you)
        elif distance <= ai.view:
            self.move_to_target(ai, you, field)

    def move_to_target(self, ai, you, field):

        options = {'8': 0, '6': 0, '2': 0, '4': 0, '9': 0, '3': 0, '1': 0, '7': 0}
        field[ai.pos_y][ai.pos_x].leave()

        ai.pos_y -= 1
        options['8'] = self.distance_meter(ai, you)
        ai.pos_y += 1

        ai.pos_y += 1
        options['2'] = self.distance_meter(ai, you)
        ai.pos_y -= 1

        ai.pos_x -= 1
        options['4'] = self.distance_meter(ai, you)
        ai.pos_x += 1

        ai.pos_x += 1
        options['6'] = self.distance_meter(ai, you)
        ai.pos_x -= 1

        ai.pos_y -= 1
        ai.pos_x += 1
        options['9'] = self.distance_meter(ai, you)
        ai.pos_y += 1
        ai.pos_x -= 1

        ai.pos_y += 1
        ai.pos_x += 1
        options['3'] = self.distance_meter(ai, you)
        ai.pos_y -= 1
        ai.pos_x -= 1

        ai.pos_y += 1
        ai.pos_x -= 1
        options['1'] = self.distance_meter(ai, you)
        ai.pos_y -= 1
        ai.pos_x += 1

        ai.pos_y -= 1
        ai.pos_x -= 1
        options['7'] = self.distance_meter(ai, you)
        ai.pos_y += 1
        ai.pos_x += 1

        ai.moved = False
        timer = 0
        best = ''
        while 1:
            if ai.moved:
                break
            if timer > 0 and (not ai.moved):
                options.pop(best)

            for dir in options:
                if options.get(dir) == min(options.values()):
                    best = dir
                    break

            ai.move(best, field)

            timer += 1

class CHARACTER:

    def __init__(self, hp, atk, atk_speed, inv_max, armor,
                 print_format, pos_x, pos_y, view, ai, game, *items):

        self.hp = hp
        self.atk = atk
        self.atk_speed = atk_speed
        self.inv = []
        self.inv_max = inv_max
        self.armor = armor
        self.print_format = print_format
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.view = view
        self.alive = True
        self.is_obstacle = False
        self.ai = ai
        self.moved = False
        game.field[self.pos_y][self.pos_x].goto(self)
        for i in range(len(items)-1):
            self.inv.append(ittems[i])

    def take_dmg(self, damage, name, field):
        if (damage - self.armor) > 0:
            self.hp -= (damage - self.armor)
        print(name, " hit ", self.name, " for ", damage - self.armor, " damage")
        self.is_alive(field)

    def attack(self,field,  *targets):
        total_attack = self.atk
        for i in range(0, len(targets)):
            targets[i].take_dmg(total_attack, self.name, field)

    def is_alive(self, field):
        if self.hp <= 0:
            self.alive = False
            print(self.name, " is dead")
            field[self.pos_y][self.pos_x].character_here = None
            # field[self.pos_y][self.pos_x].print_format = '.'
            if not self.ai:
                print(" YOU DIED !")
                sys.exit()

    def pick_item(self, item):
        if len(self.inv) <= self.inv_max:
            self.inv.append(item)
        else:
            print("Inventory is full!")

    def move(self, direction, field):
        self.moved = False
        field[self.pos_y][self.pos_x].leave()
        if direction in ('w', "W", '8'):
            self.pos_y -= 1
        elif direction in ('d', "D", '6'):
            self.pos_x += 1
        elif direction in ('s', "S", '2'):
            self.pos_y += 1
        elif direction in ('a', "A", '4'):
            self.pos_x -= 1
        elif direction in ('9'):
            self.pos_y -= 1
            self.pos_x += 1
        elif direction in ('3'):
            self.pos_y += 1
            self.pos_x += 1
        elif direction in ('1'):
            self.pos_y += 1
            self.pos_x -= 1
        elif direction in ('7'):
            self.pos_y -= 1
            self.pos_x -= 1
        elif direction in ('5'):
            field[self.pos_y][self.pos_x].goto(self)
            return 0

        if (field[self.pos_y][self.pos_x].character_here is None) and (field[self.pos_y][self.pos_x].obstacle_here is None):
            field[self.pos_y][self.pos_x].goto(self)
            self.moved = True

        else:
            if field[self.pos_y][self.pos_x].character_here:
                if not (self.ai and field[self.pos_y][self.pos_x].character_here):
                    self.attack(field, field[self.pos_y][self.pos_x].character_here)

            if direction in ('w', "W", '8'):
                self.pos_y += 1
            elif direction in ('d', "D", '6'):
                self.pos_x -= 1
            elif direction in ('s', "S", '2'):
                self.pos_y -= 1
            elif direction in ('a', "A", '4'):
                self.pos_x += 1
            elif direction in ('9'):
                self.pos_y += 1
                self.pos_x -= 1
            elif direction in ('3'):
                self.pos_y -= 1
                self.pos_x -= 1
            elif direction in ('1'):
                self.pos_y -= 1
                self.pos_x += 1
            elif direction in ('7'):
                self.pos_y += 1
                self.pos_x += 1

            field[self.pos_y][self.pos_x].goto(self)


class Dwarf(CHARACTER):

    def __init__(self, game, ai, hp=12, atk=5, atk_speed=1.0, inv_max=5, armor=3,
                 print_format="D", pos_x=3, pos_y=2, view=5):

        CHARACTER.__init__(self, hp, atk, atk_speed, inv_max, armor,
                           print_format, pos_x, pos_y, view, ai, game)
        self.name = "dwarf"


class Goblin(CHARACTER):

    def __init__(self, game, ai, hp=7, atk=4, atk_speed=0.2, inv_max=2, armor=0,
                 print_format="G", pos_x=9, pos_y=2, view=5):

        CHARACTER.__init__(self, hp, atk, atk_speed, inv_max, armor,
                           print_format, pos_x, pos_y, view, ai, game)
        self.name = "goblin"


class Troll(CHARACTER):
    def __init__(self, game, ai,  hp=20, atk=9, atk_speed=0.2, inv_max=2, armor=0,
                 print_format="T", pos_x=9, pos_y=9, view=3):

        CHARACTER.__init__(self, hp, atk, atk_speed, inv_max, armor,
                           print_format, pos_x, pos_y, view, ai, game)
        self.name = "troll"



class Obstacle:

    def __init__(self, x, y, height, field):
        self.x = x
        self.y = y
        self.height = height
        self.print_format = '#'
        self.is_obstacle = True
        field[y][x].goto(self)



game = Game(Place)

dwarf = Dwarf(game, False)
goblin1 = Goblin(game, True)
goblin2 = Goblin(game, True, pos_x=8, pos_y=7)
goblin3 = Goblin(game, True, pos_x=5, pos_y=8)
troll = Troll(game, True)



# GAME START:
print("WELCOME TO THE DUNGEON")
print("CONTROLS:"
      "\n8 - up"
      "\n6 - right"
      "\n2 - down"
      "\n4 - left"
      "\n9, 3, 1, 7 diagonally movement"
      "\n5 - weit"
      "\nto move, write number of direction, and hit enter"
      "\nto attack an enemy simply \"walk\" on him")
input("type anything to proceed")

while 1:
    guaz = Obstacle(2, 3, 1, game.field)
    guaz2 = Obstacle(2, 4, 1, game.field)
    game.print_field()
    game.your_turn(dwarf)
    game.enemy_turn(dwarf, game.field, goblin1)
    game.enemy_turn(dwarf, game.field, goblin2)
    game.enemy_turn(dwarf, game.field, goblin3)
    game.enemy_turn(dwarf, game.field, troll)
    game.turn += 1

