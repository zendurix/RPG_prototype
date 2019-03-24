from itemClasses import *
from GAMEclass import *
import sys


class CHARACTER:

    def __init__(self, hp, atk, atk_speed, inv_max, armor,
                 print_format, pos_x, pos_y, view, ai, game, level, items):

        self.hp = hp
        self.hp_max = hp
        self.atk = atk
        self.atk_speed = atk_speed
        self.inv = []
        self.equipment = []
        self.inv_max = inv_max
        self.armor = armor
        self.print_format = print_format
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.view = view
        self.alive = True
        self.is_obstacle = False
        self.ai = ai
        self.level = level
        self.moved = False
        game.field[self.pos_y][self.pos_x].goto(self)
        for i in items:
            self.inv.append(i)

    def take_dmg(self, damage, name, field):
        if (damage - self.armor) > 0:
            self.hp -= (damage - self.armor)
        print(name, " hit ", self.name, " for ", damage - self.armor, " damage")
        if self.hp < 0:
            self.hp = 0
        self.is_alive(field)

    def attack(self, field,  *targets):
        total_attack = self.atk
        for i in range(0, len(targets)):
            targets[i].take_dmg(total_attack, self.name, field)

       # print("YOU( ", self.pos_x,", ", self.pos_y,")  AI( ", targets[0].pos_x,", ", targets[0].pos_y,")" )

    def is_alive(self, field):
        if self.hp <= 0:
            self.alive = False
            print(self.name, " is dead")
            field[self.pos_y][self.pos_x].character_here = None
            field[self.pos_y][self.pos_x].died_here(self)
            # field[self.pos_y][self.pos_x].print_format = '.'
            if not self.ai:
                print("      YOU DIED !")
                input("\n\nType anything to exit")
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

    def search(self, place):
        for item in place.items_here:
            if type(item) in [Weapon, Chest, Dead_body]:
                print(item.name, end=", ")
            else:
                print(item, end=", ")

    def pick_up(self, place, name_given):
        x = 0
        for item in place.items_here:
            if item.name == name_given:
                if len(self.inv) < self.inv_max:
                    self.pick_item(item)
                    place.items_here.remove(item)
                    break
                else:
                    print("Inventory is full!")
            else:
                 x += 1
        if x == len(place.items_here):
            print("Wrong item name!")

    def print_inv(self):
        for item in self.inv:
            if type(item) in [Weapon, Chest, Dead_body]:
                print(item.name, end=", ")
            else:
                print(item, end=", ")


    def equip(self, name):
        is_in_inv = False
        for item in self.inv:
            if name == item.name:
                is_in_inv = True
                that_item = item
        if is_in_inv:
            that_item.equipping(self)

    def deequip(self, name, place):
        is_in_eq = False
        for item in self.equipment:
            if name == item.name:
                is_in_eq = True
                that_item = item
        if is_in_eq:
            that_item.deequipping(self, place)




class Dwarf(CHARACTER):

    def __init__(self, game, ai, level, hp=12, atk=5, atk_speed=1.0, inv_max=5, armor=3,
                 print_format="D", pos_x=3, pos_y=1, view=4, items=[]):
        self.name = "dwarf"
        if level == 1:
            CHARACTER.__init__(self, hp, atk, atk_speed, inv_max, armor,
                               print_format, pos_x, pos_y, view, ai, game, level, items= [])


class Goblin(CHARACTER):

    def __init__(self, game, ai, level, hp=5, atk=4, atk_speed=0.2, inv_max=2, armor=0,
                 print_format="G", pos_x=9, pos_y=2, view=5, items=[dagger, shirt]):
        if level >= 2:
            hp += 1
            atk += 1
        if level >= 3:
            hp += 1
            atk += 1
            armor += 1

        CHARACTER.__init__(self, hp, atk, atk_speed, inv_max, armor,
                           print_format, pos_x, pos_y, view, ai, game, level, items)

        for i in items:
            self.inv.append(i)
        for i in items:
            i.equipping(self)
        self.name = "goblin"


class Troll(CHARACTER):
    def __init__(self, game, ai, level, hp=20, atk=9, atk_speed=0.2, inv_max=2, armor=0,
                 print_format="T", pos_x=9, pos_y=9, view=3, items=[]):

        CHARACTER.__init__(self, hp, atk, atk_speed, inv_max, armor,
                           print_format, pos_x, pos_y, view, ai, game, level, items)
        self.name = "troll"


