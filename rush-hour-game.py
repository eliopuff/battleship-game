import sys
import json
from board import Board
from car import Car



class Game:
    """
    This is game class built to model and run the game 'rush-hour'
    all relevant attributes and methods are listed bellow
    and enabled for any object of this class when called upon.
    """


    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board

    def __single_turn(self):
        '''this is method representing a turn in the game. it checks
        wether the input is valid, and then whether the game is over
        yet. when game is over, no return value. otherwise returns True.'''
        print(self.board)
        while True:
            player_input = input('enter move:')
            legal = self.__legal_input(player_input)
            legal, split_list = legal
            if not legal:
                if player_input == '!':
                    return
                else:
                    print('illegal input.')
                    continue
            else:
                board = self.board
                car_name = split_list[0]
                move = split_list[1]
                if board.move_car(car_name, move):
                    if board.cell_content(board.target_location()) != None:
                        print(board)
                        return
                    return True
                else:
                    print('illegal input.')
                    continue
        
                
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        pass

    def play(self):
        '''return none, when game is over. run the game, turn by turn.
        if the game is over, the turn loop returns None and game 'breaks', 
        ending method.'''
        if self.board.cell_content(self.board.target_location()) != None:
            print(self.board)
            return
        running = True
        while running:
            if not self.__single_turn():
                break
        return



    def __legal_input(self, player_input):
        '''checks input is legal. returns status of input and list of input'''
        input_list = list(player_input)
        if ',' in input_list:
            input_list.remove(',')
            if len(input_list) == 2:
                if input_list[0] in ['Y', 'B', 'O', 'G', 'W', 'R']:
                    if input_list[1] in ['u', 'd', 'l', 'r']:
                        return True, input_list
        return False, []




def load_json(filename):
    '''loads the car configurations from json file'''
    json_file = filename
    with open(json_file, 'r') as file:
        car_config = json.load(file)
    # now car_config is a dictionary equivalent to the JSON file
    return car_config


def sort_cars(unsorted_cars, cell_list):
    '''sorts cars from those valid for game and those not. returns
    sorted dict of cars that are valid'''
    sorted = {}

    for car in unsorted_cars:
        row, col = tuple(unsorted_cars[car][1])
        orientation = unsorted_cars[car][2]
        length = unsorted_cars[car][0]
        if car in ['Y', 'B', 'O', 'G', 'W', 'R'] and \
            length in [2, 3, 4] and (row, col) \
                in cell_list and orientation in [0, 1]:
                sorted[car] = [length, (row, col), orientation]
    return sorted


def place_cars(board, cars):
    '''place cars on board. return board ready for the game!'''
    for car in cars:
        length, location, orientation = tuple(cars[car])
        car_obj = Car(car, length, location, orientation)
        board.add_car(car_obj)
    return board



if __name__== "__main__":
    '''main function containing all __init__s of objects and runs the game.
    no return value, but you get a nice game out of it :D'''
    board = Board()
    unsorted_cars = load_json(sys.argv[1])
    sorted_cars = sort_cars(unsorted_cars, board.cell_list())
    game_board = place_cars(Board(), sorted_cars)
    game = Game(game_board)
    while True:
        game.play()
        print('game over')
        break
