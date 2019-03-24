from obstacleClass import Obstacle
from characterClasses import *
from termcolor import colored
from Map_randomizer import *
from instructions import *
from itemClasses import *
from fieldClass import *
from GAMEclass import *
from os import system
import time


game = Game(Place)
game.make_random_map()

dwarf = Dwarf(game, False, 1)
goblin1 = Goblin(game, True, 1)
goblin2 = Goblin(game, True, 1, pos_x=8, pos_y=7)
goblin3 = Goblin(game, True, 1, pos_x=5, pos_y=8)
troll = Troll(game, True, 1)
characters_in_game = []

for i in game.field:
    for j in i:
        if j.character_here is not None:
            if j.character_here.ai:
                characters_in_game.append(j.character_here)
            else:
                you = j.character_here


# GAME START:

print_instructions()

given = False
while 1:

    game.print_field_and_hp(characters_in_game, you)

    game.your_turn(you)
    for x in characters_in_game:
        game.enemy_turn(you, x)

    game.turn += 1



    # time.sleep(0.5)

    if not troll.alive:
        ending()
        break


