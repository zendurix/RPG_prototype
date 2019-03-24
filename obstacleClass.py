
class Obstacle:

    def __init__(self, x, y, height, field):
        self.x = x
        self.y = y
        self.height = height
        self.print_format = '#'
        self.is_obstacle = True
        field[y][x].goto(self)



