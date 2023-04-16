from tkinter import *
from boggle_board_randomizer import *
from boggle_model import *
from boggle_GUI import *




class BoggleController:

    '''the class that brings our boggle game app together, bringing boggle_GUI
    and boggle_model into one place. they interact to create a harmonious game
    for all to enjoy, in this controller class!'''

    def __init__(self) -> None:
        '''the boggle controler class init method. attributes are:
        game_board = 2d list of letters - board randomized for the game
        gui = our object bogglegui for the game, containing the design 
        model = our object bogglemodel for the game, containing the logic
        cur_score = a number representing the current score
        words_saved = a set of all words entered already'''

        self.__game_board = self.set_game_board()
        self.__gui = BoggleGUI(self.__game_board)
        self.__model = BoggleModel(self.__game_board)
        self.__cur_score = 0
        self.__words_saved = set()
        self.init_button_action() #assigns buttons to their logical events

        self.__gui.set_display('_____')

    def init_button_action(self):
        '''this method initializes and sets the logic-driven actions that
        are assigned to each button in the GUI.'''

        for button_text in self.__gui.get_button_chars():
            if len(button_text) == 2:
                action = self.create_button_action(button_text[0])
            else:
                action = self.create_button_action(button_text)
            self.__gui.set_button_command(button_text, action)

        

    def create_button_action(self, button_text):
        '''helper for init_button_action(). contains an inner function 
        which it returns and it is set according to desired action of the
        input button we are currently setting an action for.
        elements from gui and model are brought together. the buttons in gui 
        are assigned the type_in() method of the model, and the save word
        button is given the logical value from model of remembering a word.
        score is updated according to square of current word if its legal,
        the legal word is saved etc.'''

        def inner():

            self.__model.type_in(button_text)
            self.__gui.set_display(self.__model.get_display())

            if button_text == 'save word' and self.__model.get_last_word():
                if self.does_path_pass_vibe_check() and \
                    (self.__model.get_last_word() not in self.__words_saved):


                    self.__gui.set_words_saved(self.__model.get_last_word())
                    self.__words_saved.add(self.__model.get_last_word())
                    self.__cur_score += (len(self.__model.get_last_word()))**2
                    self.__gui.clear_buttons_as_selected()
                    self.word_checker()
                else:
                    self.__gui.clear_buttons_as_selected()
                    self.__model.reset_last_word()

            if button_text == 'clear':
                self.__gui.clear_buttons_as_selected()

            if button_text == 'play again':
                self.play_again()

        return inner

    def word_checker(self):
        '''updates score from word and updates it on GUI score label text'''

        score = self.__cur_score
        self.__gui.set_score_display(score)

    def play_again(self):
        '''method determines wether the player wanted to play again.
        if yes, all game attributed are cleared and a new board is
        randomized and fed to model and gui, to start a new game!'''

        self.__game_board = self.set_game_board()
        self.__gui.set_new_board(self.__game_board)
        self.__model.set_new_board(self.__game_board)

        self.__gui.clear_all()
        self.__model.clear_all()
        self.init_button_action()


    def set_game_board(self):
        '''returns and sets a random game board from board randomizer'''

        return randomize_board()

    def does_path_pass_vibe_check(self):
        '''a kind of funny name for a method that checks whether a selected
        word and path passes what is desired from it in bogglemodel.'''

        if self.__model.check_if_valid_path(
            self.__gui.get_buttons_selected_locations(), self.open_words_dict(
                len(self.__gui.get_buttons_selected_locations()))):
            return True
        return False

    def open_words_dict(self, length):
        '''opens the text file of the dictionary, and creates a set of words
        in the file that are only of the relevant length of the word in
        question, to save space and time'''

        with open('boggle_dict.txt', 'r') as f:
            word_set = set(word.strip() for word in f if len(
                word.strip()) == length)
        return word_set

        

        
    def run(self) -> None:
        '''runs the game, app, from GUI'''

        self.__gui.run()

 



if __name__ == '__main__':
    '''this will allow the boggle app to run when called in command line'''

    the_game = BoggleController()
    the_game.run()
