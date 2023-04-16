import const

class Apple:

    """
    this class represents the apples in the snake game
    """


    def __init__(self, location) -> None:

        """
        class apple builder:
        :attribute size: = A number of cells of the apple
        :attribute color: = A string representing the color of the apple (green)
        :attribute location: = A tuple represnting the apple's (row,col) location
        """
        self.__size = const.APPLE_SIZE
        self.__color = const.GREEN
        self.__location = location
        


    def get_apple_location(self):
        """
        :return: returns the apple location
        """
        return self.__location 
    
    def get_apple_size(self):
        """
        :return: returns the apple's size
        """
        return self.__size
