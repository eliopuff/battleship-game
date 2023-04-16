class BoggleModel:

    '''this is the class for the model of the logic in our game of Boggle.
    things like word memory, score, clearing display and ost importantly,
    checking if a given word and path is valid for the game!'''

    

    def __init__(self, board=[]) -> None:

        '''init method, which contains the following attributes:
        current_display = what is currently displayed on the game screen
        last_word = the last word saved
        words_set = set of words containing all words already saved in game
        buttons_pressed = dict of buttons pressed, with their board coordinates
        cur_score = int representing the player's current score
        game_board = a 4x4 2-d list containg letters of the board. starts w/'''

        self.__do_clear() #start game model with clean slate
        self.__current_display = ''
        self.__last_word = ''
        self.__words_set = set()
        self.buttons_pressed = dict()
        self.__cur_score = 0
        self.__game_board = board


    def clear_all(self):
        '''method is responsible for clearing all the values saved in the last
        game. this method is useful for a new game. all is reset to empty.'''

        self.__current_display = ''
        self.__words_set = set()
        self.buttons_pressed = dict()
        self.__cur_score = 0

    def get_display(self) -> str:
        '''returns current display of the game model (what has been typed)'''

        return self.__current_display

    def get_saved_words_set(self):
        '''returns the set of saved valid words already entered in the game'''

        return self.__words_set

    def get_last_word(self):
        '''returns last word saved'''

        return self.__last_word

    def get_cur_score(self):
        '''returns the current score'''

        return self.__cur_score

    def reset_last_word(self):
        '''resets the last word to None, so there is no saved word (clear)'''

        self.__last_word = None

    def set_cur_score(self, score):
        '''sets the current score based off addition of words'''

        self.__cur_score = score

    def __do_clear(self) -> None:
        '''clears the current display when the 'clear' method is used'''

        self.__current_display = ''
        self.buttons_pressed = None

    def __do_letter_clicked(self, letter: str) -> None:
        '''recognises the click of a board letter, and adds 
        letter to display'''

        self.__set_display(letter)

    def set_new_board(self, board):
        '''sets a new board, upon a second round of the game!'''

        self.__game_board = board

    def __set_display(self, letter: str) -> None:
        '''sets the current display of the game model, updating 
        it depending on what is typed in. because we treat the save word and
        clear buttons as actions too, they have seperate uses.'''

        if letter not in {'save word', 'clear', 'play again'}:
            self.__current_display += letter

        #if the button was one to save word, the word is saved
        elif letter == 'save word':
            if self.__last_word not in self.__words_set:
                self.__words_set.add(self.__last_word)


    def type_in(self, letter) -> None:
        '''a letter is typed in, although this letter simply reresents buttons.
        if this button is not a letter onthe board it can be save word or 
        clear, which have other functions. save word saves the word and clears
        display. clear omly clears display'''

        if letter == 'save word':
            self.__last_word = self.__current_display
            if self.__last_word not in self.__words_set:
                self.__words_set.add(self.__last_word)
            self.__do_clear()

        if letter == 'clear':
            self.__last_word = None
            self.__do_clear()

        else:
            self.__do_letter_clicked(letter)
    

    def check_if_valid_path(self, path, words):
        '''checks whether a given path taken along the board is legal based off
        of the game requirements. a path may only be done through straight or
        diagonal movements, and the word in the path must be in the iterable 
        of words.'''

        board = self.__game_board
        word = ''
        if len(path) == 0:
            return
        for ind, step in enumerate(path): #keep track of index and path step
            y, x = step
            if self.out_of_bounds(board, y, x):
                return
            if ind == 0:
                word += board[y][x]
                continue
            if not self.legal_move(y, x, path[ind - 1]):
                return
            word += board[y][x]
        if word in words: # we're good to go!
            return word
        return None


    def legal_move(self, y, x, prev_step):
        '''a helper function for check_if_valid_path(). it checks whether one
        given move is legal according to the previous position in the path.
        parameters are:
        prev_y, prev_x = position of previous step
        returns bool according to whether requirements are met'''

        prev_y, prev_x = prev_step
        if y in {prev_y, prev_y + 1, prev_y - 1} and x in \
                {prev_x, prev_x + 1, prev_x - 1} and (y, x) != prev_step:
            return True
        return False

    def out_of_bounds(self, board, y, x):
        '''helper function for check_if_valid_path(). makes sure the step
        being taken is not out of bounds of the board. 
        returns bool according to met requirements'''

        if 0 > y or y > len(board)-1 or 0 > x or x > len(board)-1:
            return True
        return False
