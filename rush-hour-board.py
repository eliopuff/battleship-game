class Board:
    """
    this is a class describing the object of a Board for the game
    rush-hour. all relevant attributes and methods are listed bellow
    and enabled for any object of this class when called upon.
    
    it's size is 7*7 not including decorative side and extra exit cell.
    """

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # implement your code and erase the "pass"
        self.length = 7
        self.width = 7
        self.board = self.__alter_board([[None for _ in range(self.width + 1)] for _ in range(self.length)])
        self.cars = {}
        self.car_in_target = None

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        board = ''
        for i in range(self.length):
            row = ''
            for j in range(self.width + 1):
                if self.board[i][j] == '*':
                    row += ' * '
                elif self.board[i][j] == None:
                    row += ' _ '
                else:
                    row += f' {self.board[i][j]} '
            board += row + '\n'
        return board

    def __alter_board(self, board):
        '''alters board to represent one that is relevant to the game'''
        for i in range(self.length):
            if i != 3:
                board[i][self.width] = '*'
        return board
        

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        all_coordinates = []
        for i in range(self.length):
            for j in range(self.width):
                all_coordinates.append((i, j))
        all_coordinates.append(self.target_location())
        return sorted(all_coordinates)

        

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description)
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        # implement your code and erase the "pass"
        move_list = []
        for name in self.cars:
            car = self.cars[name]
            for move in car.possible_moves():
                required = car.movement_requirements(move)
                legal_count = 0
                for location in required:
                    if location in self.cell_list() and self.cell_content(location) == None:
                        legal_count += 1
                if legal_count == len(required):
                    move_list.append((name, move, f'car can move {move}'))
        return move_list

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        return (3, 7)

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row, col = coordinate[0], coordinate[1]
        if self.board[row][col] == None:
            return
        return self.board[row][col]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        coordinates = car.car_coordinates() #location spread of given car
        if car.get_name() in self.cars or coordinates[0][0] < 0 \
            or coordinates[0][1] < 0: #reasons car may be illegal
            return False
        for cell in coordinates:
            if cell not in self.cell_list():
                return False
        legal_spots = 0
        if 'u' in car.possible_moves():
            orientation = 0
        if 'r' in car.possible_moves():
            orientation = 1
        for coordinate in coordinates:
            row, col = coordinate[0], coordinate[1]
            if self.board[row][col] == None:
                legal_spots += 1
        if len(coordinates) == legal_spots:
            for coordinate in coordinates:
                row, col = coordinate[0], coordinate[1]
                self.board[row][col] = car.get_name()
            self.cars[car.get_name()] = car
            return True
        return False #car not fit to be added

    def move_car(self, name, move_key):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        for move in self.possible_moves():
            if move[0] == name:
                if move[1] == move_key:
                    car = self.cars[name]
                    old_coordinates = car.car_coordinates()
                    if car.move(move_key):
                        for (i, j) in old_coordinates:
                            self.board[i][j] = None
                        for (i, j) in car.car_coordinates():
                            self.board[i][j] = name
                        return True
        return False
