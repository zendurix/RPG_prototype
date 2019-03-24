from fieldClass import *
import math
from characterClasses import *


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

