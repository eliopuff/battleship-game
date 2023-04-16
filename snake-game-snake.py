from game_display import GameDisplay as gd
from const import *


class Snake:

    '''this is a class representing the snake in the game snake.'''

    def __init__(self, color, direction, head_location, tail_location, length = SNAKE_LENGTH):
        ''' class snake builder, requiting init attributes.
        :attribute length: = number of cells in snake
        :attribute head_location: = coordinates x,y (col,row) of snake's head'''
        
        self.color = color
        self.direction = direction
        self.head_location = head_location
        self.tail_location = tail_location
        self.length = length
        self.snake_coordinates = []
        


    def snake_move(self):
        '''moves the snake in a manner supporting the continuous loop of the game.
        a snake head tile is added in the direction of movement, and the tail tile 
        is removed. this is how the snake 'moves' in the loop.
        :params x, y: = representing new coordinates for head
        :params a, b: representing new coordinates for tail'''

        if self.direction == RIGHT:
            x, y = self.head_location[0] + 1, self.head_location[1]
            a, b = self.tail_location[0] + 1, self.tail_location[1]
        if self.direction == LEFT:
            x, y = self.head_location[0] - 1, self.head_location[1]
            a, b = self.tail_location[0] - 1, self.tail_location[1]
        if self.direction == UP:
            x, y = self.head_location[0], self.head_location[1] + 1
            a, b = self.tail_location[0], self.tail_location[1] + 1
        if self.direction == DOWN:
            x, y = self.head_location[0], self.head_location[1] - 1
            a, b = self.tail_location[0], self.tail_location[1] - 1

        
        self.snake_coordinates.remove(self.head_location)
        self.snake_coordinates.remove(self.tail_location)
    
        self.head_location = (x, y)
        self.tail_location = (a, b)



    def change_direction(self, direction, arrow_input):
        '''updates direction of snake movement according to the arrow input of
        the player. can only change direction '''

        if (arrow_input == RIGHT and direction != LEFT) or \
        (arrow_input == LEFT and direction != RIGHT) or \
        (arrow_input == UP and direction != DOWN) or \
        (arrow_input == DOWN and direction != UP):
            self.direction = arrow_input
        
    def get_snake_length(self):
        '''returns snake's current length, how many tiles it takes up'''

        return self.length

    def get_snake_direction(self):
        '''returns snake's current direction. '''
        return self.direction
    

    def all_snake_coordinates(self):
        '''returns list of locations of all tiles taken up by the snake'''
        
        return self.snake_coordinates

    

    def snake_hit_self(self):
        '''checks if snake hit itself, ending the game.'''

        if self.head_location in self.all_snake_coordinates():
            return True
        return False




    def get_head_location(self):
        '''returns head coordinates (col, row)'''

        return self.head_location


    def get_tail_location(self):
        '''returns tail coordinates (col, row)'''

        return self.tail_location
