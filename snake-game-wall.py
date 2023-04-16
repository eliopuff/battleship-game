from const import *


class Wall:
    '''this is a wall class for the wall in the game snake.
    walls move, and can kill or cut our moving snake'''

    def __init__(self, length, direction, mid_location):
        self.__length = length
        self.__direction = direction
        self.__mid_location = mid_location
        self.__wall_coordinates = self.init_wall_location([])


    def get_direction(self):
        '''returns wall direction'''

        return self.__direction
    
    def get_mid_location(self):
        '''returns middle location of wall'''

        return self.__mid_location



    def init_wall_location(self, wall):
        ''''''

        direction = self.__direction
        mid_x, mid_y = self.__mid_location

        if direction in [RIGHT, LEFT]:
            self.__wall_coordinates.append((mid_x + 1, mid_y))
            self.__wall_coordinates.append((mid_x - 1, mid_y))
        if direction in [UP, DOWN]:
            self.__wall_coordinates.append((mid_x, mid_y + 1))
            self.__wall_coordinates.append((mid_x, mid_y - 1))


    def update_wall_coordinates(self):
        ''''''

        direction = self.__direction
        x, y = self.__mid_location

        if direction == RIGHT:
            self.__wall_coordinates.remove((x - 2, y))
            self.__wall_coordinates.append((x + 1, y))
        if direction == LEFT:
            self.__wall_coordinates.remove((x + 2, y))
            self.__wall_coordinates.append((x - 1, y))
        if direction == UP:
            self.__wall_coordinates.remove((x, y - 2))
            self.__wall_coordinates.append((x, y + 1))
        if direction == DOWN:
            self.__wall_coordinates.remove(((x, y + 2)))
            self.__wall_coordinates.append((x, y - 1))

    def move_wall_mid(self):
        '''moves the middle point of a wall'''

        x, y = self.__mid_location

        direction = self.direction
        if direction == RIGHT:
            self.__mid_location = (x + 1, y)
        if direction == LEFT:
            self.__mid_location = (x - 1, y)
        if direction == UP:
            self.__mid_location = (x, y + 1)
        if direction == DOWN:
            self.__mid_location = (x, y - 1)
