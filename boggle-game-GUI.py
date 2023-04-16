from tkinter import *
from typing import List


#constant colors, something that is rather handy to use
BUTTON_COLOR = 'white'
HOVER_COLOR = 'gray13'
BUTTON_ACTIVE_COLOR = 'gray'
BACKGROUND_COLOR = 'black'


#default values for the buttons on the board of the game
#i borrowed this idea from the slides in the lectre of week 11!

BUTTON_STYLE = {'font': ('Small Fonts', 15), 
'borderwidth': 1, 'relief': RAISED,  
'bg': BUTTON_COLOR, 'height': 3, 
'activebackground': BUTTON_ACTIVE_COLOR,
'width': 3}


class BoggleGUI:

    '''this class is responsible for tall the boggle game GUI, which is
    graphical user interface. the main thing it does is take care of the main
    root of the game, the window where it's all happening, and manage all
    the graphical changes according to the logic behind the scenes'''
    
    buttons = {} #the buttons of the game that will be useful to keep track of


    def __init__(self, letters=[]):
        '''this is the init method of class BoggleGUI, and it is very long
        because GUI is a complicated thing with lots of... stuff.
        i'll try to put as much as i can here, for clarity - 
        - graphical attributes:
        root (or main_window) = the main window of our application
        arcade_photo, label = cute pixel art background for the lower frame
        top_frame = a frame containing score and timer: timer_label, 
        score_label word display and functional buttons: remove_word_button, 
        enter_word_button.
        saved_words_frame = where the saved words are displayed
        lower_frame = frame where the letter buttons or board are
        start_button = button to press to start the game. falls away on press
        play_again_button = same as above, but shows when timer runs out

        - technical attributes:
        letters_on_board = 'flattened' list of all our letters, in order
        button_locations = dictionary of buttons and their row, col locations
        buttons_selected = list containing all cur selected letters
        buttons_selected_locations = list as above, but the locations
        score = current score display
        saved_words = contains all saved words

        '''

        root = Tk()
        root.title('Boggle')
        root.resizable(False, False)
        self.__main_window = root

        self.__letters_on_board = [x for y in letters for x in y]
        

        self.__main_window.geometry('500x350')
        self.__main_window['bg'] = BACKGROUND_COLOR

        # self.__arcade_photo = PhotoImage(file='moon.png')
        # self.__label = Label(root, image=self.__arcade_photo)
        # self.__label.place(x=0, y=0, relwidth=1, relheight=1)


        self.button_locations = dict()
        self.__buttons_selected = []
        self.__buttons_selected_locations = []

        self.__top_frame = Frame(bg=BACKGROUND_COLOR, 
        highlightbackground=BACKGROUND_COLOR)

        self.__top_frame.pack(fill=BOTH)

        self.__remove_word_button = Button(self.__top_frame, text='clear',
        command=self.enter_word_callback, font=('Small Fonts', 10), 
        bg=BACKGROUND_COLOR, fg='white', borderwidth=2)

        self.__remove_word_button.pack(side=RIGHT)

        self.buttons['clear'] = self.__remove_word_button


        self.__enter_word_button = Button(self.__top_frame, text='save word',
        command=self.enter_word_callback, font=('Small Fonts', 10),
         bg=BACKGROUND_COLOR, fg='white', borderwidth=2)

        self.__enter_word_button.pack(side=RIGHT)

        self.buttons['save word'] = self.__enter_word_button




        self.__timer_label = Label(self.__top_frame, font=('Small Fonts', 10), 
        bg='white', fg='black', width=7, height=2, relief='sunken', 
        highlightcolor='white')
        self.__timer_label.pack()


        self.__score = '0'
        self.__score_label = Label(self.__top_frame, text=self.__score, 
        font=('Small Fonts', 10), width=3, borderwidth=2,
        relief='groove', highlightcolor='white')
        self.__score_label.pack()



        self.__display_label = Label(self.__top_frame, 
        font=('Small Fonts', 15), bg=BACKGROUND_COLOR, fg='white', width=20, 
        height=3, borderwidth=2)
        self.__display_label.pack()

        self.__save_word_frame = Frame(height=300, width=150, bg=BUTTON_COLOR)
        self.__save_word_frame.pack(side=RIGHT)

        self.__saved_words = Label(self.__save_word_frame, height=300, 
        width=16, font=('Small Fonts', 11), relief='sunken',
         highlightcolor='white')
        self.__saved_words.pack()
        
        

        self.__lower_frame = Frame(bg=BACKGROUND_COLOR, height=120, width=100)
        self.__lower_frame.pack()

        self.__create_buttons()
        self.__main_window.bind('<Key>', self.__key_pressed)



        self.__start_button = Button(self.__top_frame, 
        text='MWAHAHAHAHAHA!\nyou fell into my trap!\nnow you must defeat me'+
        '\nin a game of boggle.\nHAAHAAA...\n'+' \nwell, unless you want to'+
        ' be\ntrapped here forever...\nyou have no chance.\nclick to start'+
        ', you FOOL!',
        command=self.start_countdown, font=('Small Fonts', 10),
         bg=BACKGROUND_COLOR, fg='white', borderwidth=2, width=20, height=20)
        self.__start_button.pack()
        self.__start_button.tkraise()


        self.__play_again_button = Button(self.__top_frame, 
        text='PFFFFFFT.\nthats all you scored?? \nfoolish of you to' +
            '\nbelieve you are good\nenough to defeat me!\nclick to play ' +
            'again,\n YOU PLEB!\nand stop shrinking my\nrows and columns >:('
        , font=('Small Fonts', 10), bg=BACKGROUND_COLOR,
         fg='white', borderwidth=2, width=20, height=20)
        self.buttons['play again'] = self.__play_again_button



        
        
 
    def run(self) -> None:
        '''runs the game, starts the application and opens the app window'''

        self.__main_window.mainloop()

    def clear_all(self):
        '''destroys the play again button frame.
        clears all parameters of the game (for new game), and creates
        all new buttons for the new board of the new game. also starts the
        timer'''
        
        self.__play_again_button.destroy()
        self.__create_buttons()
        self.countdown('3', '00')
        self.__score = 0
        self.__saved_words = ''

        #we must make a new play again button in case game is played a 3rd time
        self.__play_again_button = Button(self.__top_frame, 
        text=f'game over.\nyour score:{self.__score} \nplay again?'
        , font=('Small Fonts', 10), bg=BACKGROUND_COLOR,
         fg='white', borderwidth=2, width=20, height=20)
        self.buttons['play again'] = self.__play_again_button


    def set_display(self, display_text='____') -> None:
        '''sets display for top frame, showing current typed'''

        self.__display_label['text'] = display_text

    def set_words_saved(self, word_to_save=None) -> None:
        '''adds a word the string of displayed saved words'''

        self.__saved_words['text'] += word_to_save + '\n'


    def set_button_command(self, button_name: str, comm) -> None:
        '''sets a command for a button, edited in the configuration
        of the button.'''

        self.buttons[button_name].configure(command=comm)


    def get_button_chars(self) -> List[str]:
        '''returns list of button chars'''

        return list(self.buttons.keys())

    def get_buttons_selected_locations(self):
        '''return locations of slected buttons'''

        return self.__buttons_selected_locations

    def set_new_board(self, board):
        '''sets a new board, when game is new, flattened list of letters'''

        self.__letters_on_board = [x for y in board for x in y]

    def set_score_display(self, score):
        '''changed the score label display according to updated score'''

        self.__score_label.configure(text=score)
        self.__score = score



    def set_button_as_selected(self, button):
        '''button is shown as selected and the font goes small to show this'''

        button.configure(font= ('Small Fonts', 8))
        self.__buttons_selected_locations.append(self.button_locations[button])
        self.__buttons_selected.append(button)



    def clear_buttons_as_selected(self):
        '''clears button as selected, font size goes back to normal'''

        for button in self.__buttons_selected:
            button.configure(font= ('Small Fonts', 15))
        self.__buttons_selected_locations = []
        self.__buttons_selected = []

        




    def countdown(self, minute, second):
        '''initiates the countdown of the game, using the after method of tk.
        the label is updated every 1000 miliseconds, giving the illusion
        of a regular clock! except this one was built up manually...
        i'm actually really proud of this method.'''

        self.__timer_label['text'] = f'{minute}:{second}'
        if int(minute) > 0 or (int(minute) == 0 and int(second) > 0):
            if int(second) == 0:
                self.__top_frame.after(1000, self.countdown, 
                str(int(minute) - 1), '59')
            else:
                if int(second) > 10:
                    self.__top_frame.after(1000, self.countdown, 
                    minute, str(int(second)- 1))
                else:
                    self.__top_frame.after(1000, self.countdown, 
                    minute, '0' + str(int(second)- 1))

        # it's a new game
        else:
            self.__create_play_again_frame()

    def start_countdown(self):
        '''starts the countdown, reveals the board. game has started!'''

        self.countdown('5', '00')
        self.__start_button.destroy()
        

    def __create_play_again_frame(self):
        '''when countdown is over, this frame is raised to ask if you want
        to play again?'''

        self.__play_again_button.pack()
        self.__play_again_button.tkraise()



    def __create_buttons(self) -> None:
        '''creates the buttons of the letters on the board in a grid.
        each button has the same weight of 1.'''

        for i in range(4):
            Grid.columnconfigure(self.__lower_frame, i , weight=1)
        for i in range(4):
            Grid.rowconfigure(self.__lower_frame, i , weight=1)
        
        # created by button style here
        grid_coordinates = [(i, j) for i in range(4) for j in range(4)]
        for i, letter in enumerate(self.__letters_on_board):
            y, x = grid_coordinates[i]
            self.__make_button(letter, y, x)



    def __make_button(self, button_char: str, row: int, col: int,
        rowspan: int = 1, columnspan: int = 1):
        '''here happens the big meat, the big button creation factory.
        it all goes back to create_buttons() method.
        in the second part of the function we bind it to certain events.'''

        button = Button(self.__lower_frame, text=button_char, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, 
        columnspan=columnspan, sticky=NSEW) #place the button in the grid
        self.buttons[button_char, (row, col)] = button #save button data
        self.button_locations[button] = (row, col) #save button location

        def __on_enter(event) -> None:
            button['background'] = HOVER_COLOR
            button['fg'] = 'white'

        def __on_leave(event) -> None:
            button['background'] = BUTTON_COLOR
            button['fg'] = BACKGROUND_COLOR

        def __key_pressed(event) -> None:
            if button['text'] not in {'save word', 'clear'}:
                button['fg'] = 'red'
                self.set_button_as_selected(button)

        button.bind('<Enter>', __on_enter)
        button.bind('<Leave>', __on_leave)
        button.bind('<ButtonRelease>', __key_pressed)
        return button

    
    def __key_pressed(self, event) -> None:
        '''the event of a key being pressed'''

        if event.char in self.buttons and event.char not in \
        {'save word', 'clear'}:
            self.set_button_as_selected(event.char)
            print(event.char)

    
    def enter_word_callback(self):
        '''the event of when the word is saved.'''

        self.set_words_saved(self.__display_label['text'])
        self.__display_label['text'] = ''
