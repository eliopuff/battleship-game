from typing import Optional
from game_display import GameDisplay
from const import *

class SnakeGame:
    '''this is a class for the game of snake, and is in charge of
    running the whole game (used in the snake main loop in another 
    .py file)'''

    def __init__(self, board, apples=3, walls=2, rounds=-1, width=WIDTH, height=HEIGHT) -> None:
        '''all values in the init method have a default value'''
        self.__snake = {}
        self.__board_width = width
        self.__board_height = height
        self.__key_clicked = None
        self.__apples = apples
        self.__walls = walls
        self.__board = board

        #we create a dictionary for locations of walls and apples.
        self.__walls_dict = {}
        self.__apples_dict = {}
        #self.__board = board



    def read_key(self, key_clicked: Optional[str])-> None:
        '''reads the key input of the player. this is an arrow direction'''
        self.__key_clicked = key_clicked

    def walls_dict(self, board):
        return board.get_walls_locations()

    
    def apples_dict(self, board):
        return 

    def snake_list(self, board):
        return board.get_snake_coordinates()



    def update_objects(self)-> None:
        if (self.__key_clicked == LEFT) and (self.__snake_x > 0):
            self.__snake_x -= 1
        elif (self.__key_clicked == RIGHT) and (self.__snake_x < 40):
            self.__snake_x += 1
        elif  (self.__key_clicked == UP) and (self.__snake_x < 30):
            self.__snake_y += 1
        elif  (self.__key_clicked == DOWN) and (self.__snake_x > 0):
            self.__snake_y -= 1

    def cell_in_game(self, cell):
        x, y = cell
        if x < self.__board_width and y < self.__board_height:
            return True
        return False      

    def update_wall(self) -> None:
        pass
        

    def draw_board(self, gd: GameDisplay) -> None:
        '''draws all cells on board according to moving objects.
        these are saved in dictionaries and updates constantly.
        snake is black, walls blue and apples green.'''
        #gd.draw_cell(self.__snake_x, self.__snake_y, "black")
        for cell in self.snake_list(self.__board) :
            if self.cell_in_game(cell):
                x, y = cell
                gd.draw_cell(x, y, BLACK)
        for wall in self.__walls_dict:
            for cell in wall:
                if self.cell_in_game(cell):
                    x, y = cell
                    gd.draw_cell(x, y, BLUE)
        for apple in self.__apples_dict:
            for cell in apple:
                if self.cell_in_game(cell):
                    x, y = apple
                    gd.draw_cell(x, y, GREEN)

        


    def end_round(self) -> None:
        pass


        
    def is_snake_dead(self, board, snake):
        if board.snake_hit_limit(snake) or snake.snake_hit_self():
            return True
        return False


    def is_over(self, snake) -> bool:
        if self.is_snake_dead(self.__board, snake):
            return True
        return False
