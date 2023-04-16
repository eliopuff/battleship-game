class Car:
    """
    this is a class describing the object of a Car for the game
    rush-hour. all relevant attributes and methods are listed bellow
    and enabled for any object of this class when called upon.
    """
    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.name = name
        self.length = length
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coordinates = [self.location]
        row, col = self.location
        for num in range(1, self.length):
            if self.orientation == 0:
                coordinates.append((row + num, col))
            if self.orientation == 1:
                coordinates.append((row, col + num))
        return sorted(coordinates)

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.
        # implement your code and erase the "pass"
        move_dict = {}
        if self.orientation == 0:
            move_dict['u'] = 'car goes up one space'
            move_dict['d'] = 'car goes down one space'
        if self.orientation == 1:
            move_dict['l'] = 'car goes left one space'
            move_dict['r'] = 'car goes right one space'
        return move_dict

    def movement_requirements(self, move_key):
        """ 
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        # implement your code and erase the "pass"
        row_for, col_for = self.car_coordinates()[-1][0], self.car_coordinates()[-1][1]
        row_back, col_back = self.car_coordinates()[0][0], self.car_coordinates()[0][1]
        if self.orientation == 0:
            if move_key == 'u':
                return [(row_back - 1, col_back)]
            if move_key == 'd':
                return [(row_for + 1, col_for)]
        if self.orientation == 1:
            if move_key == 'l':
                return [(row_back, col_back - 1)]
            if move_key == 'r':
                return [(row_for, col_for + 1)]

    def move(self, move_key):
        """ 
        :param move_key: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        coordinates = self.car_coordinates()
        if not self.movement_requirements(move_key):
            return False
        moved_to = self.movement_requirements(move_key)[0]
        if self.orientation == 0 and move_key in ['u', 'd']:
            if move_key == 'u' and self.location[0] != 0:
                self.location = moved_to
            if move_key == 'd':
                self.location = coordinates[1]
            return True
        if self.orientation == 1 and move_key in ['r', 'l']:
            if move_key == 'l' and self.location[1] != 1:
                self.location = moved_to
            if move_key == 'r':
                self.location = coordinates[1]
            return True
        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.name
