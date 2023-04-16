from game_display import GameDisplay as gd
from game_utils import UP, DOWN, RIGHT, LEFT, HEIGHT, WIDTH
from const import *

class Board:
    '''this class represents the board for the game snake, in which
    the objects of the game move. these are the snake, apples and walls.'''

    def __init__(self, width=WIDTH, height=HEIGHT):
        self.__width = width
        self.__height = height
        self.__apples = {}
        self.__walls = {}
        self.__snake_body = []
        self.__board_status = dict()

    def get_snake_coordinates(self) -> list[tuple]:
        """
        :return: tuples list of the snake's body
        """
        return self.__snake_body

    def get_apples_locations(self) -> dict[tuple]:
        """
        :return: dict of apples
        """
        return self.__apples


    def get_walls_locations(self) -> dict[tuple]:
        """
        :return: dict of walls, each with list of tuple locations of form (x,y)
        """
        return self.__walls


    def is_cell_in_board(self, coordniate):
        if coordniate[0] >= self.__height or coordniate[0] < 0 :
            return False
        if coordniate [1] >= self.__width or coordniate[1] < 0 :
            return False
        return True 


    def cell_content(self, coordinate):
        '''returns content of the cell'''
        return self.__board_status[coordinate]



    def update_cell_content(self, coordinates, new_content):
        for coord in coordinates : 
            if self.is_cell_in_board(coord):
                self.__board_status[coord] = new_content


    def place_apple(self, apple):
        coordinate = apple.get_apple_location()
        if self.cell_content(coordinate) == None :
            self.update_cell_content(coordinate, APPLE)
            return True
        return False 

    def place_snake(self, snake):
        coordinates = snake.all_snake_coordinates()
        for coord in coordinates :
            if self.cell_content(coord) == None :
                self.update_cell_content(coord, SNAKE)
                return True
        return False 

    def remove_apple(self, apple):
        coordinate = apple.get_apple_location()
        self.update_cell_content[coordinate] = None

    
    def is_cell_in_board(self, coordinate):
        if coordinate[0] >= self.__height or coordinate[0] < 0 :
            return False
        if coordinate [1] >= self.__width or coordinate[1] < 0 :
            return False
        return True        

 

    def add_wall(self, wall):
        coordinates = wall.get_wall_locatins()
        for coord in coordinates :
            if self.cell_content(coord) == None or self.cell_content(coord) == WALL:
                self.update_cell_content(coord, WALL)
            else : 
                return False
        return True

    def wall_location(self):
        return self.__walls



    def snake_hit_wall (self, snake, wall):
        head_location = snake.get_head_location() 
        wall_coordinates = wall.get_wall_locations()
        for coord in wall_coordinates :
            if coord == head_location:
                return True
        return False
    
    def snake_hit_apple (self, coordinare):
        if self.__board_status[coordinare] == APPLE:
            return True
        return False

    def snake_hit_limit(self, snake):
        '''checks if snake hit the board limit, ending the game. the input of this
        method are the board limit coordinates.'''

        if snake.get_head_location()[0] == WIDTH or snake.get_head_location()[1] == HEIGHT:
            return True
        return False
