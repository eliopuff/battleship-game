import helper
import copy


def init_board(rows, columns):
    #this function creates a board grid (list of lists) for the game
    board = [[helper.WATER for j in range(columns)] for i in range(rows)]
    return board


def cell_loc(name):
    #this function receives as input a coordinate, interprets it into 
    #list indexes and returns the row and column indexes of the coordinate
    if helper.is_int(name[1:]) == False:
        return
    column = int(ord(name[0])) - 65
    #the ASCII index does nor correspond with our interpration
    #of letter indexing. the function fixes this by subtracting
    #the index on ASCII by 65
    row = int(name[1:]) - 1
    if column > 25 or row > 99:
        return 
    return row, column


def valid_ship(board, size, loc):
    #this function checks if a particular location is 
    #suitable for placing a ship. If it is, it returns True
    #otherwise, it returns False
    if len(board) < loc[0] or len(board[0]) < loc[1]:
        return False
    for i in range(loc[0], loc[0] + size):
        if loc[0] + size > len(board):
            return False
        if board[i][loc[1]] != helper.WATER:
            return False
    return True



def create_player_board(rows, columns, ship_sizes):
    #this function is responsible for creating a board for the human player
    #it receives input of rows, columns and a set of ships in three sizes
    #via input, the human player enters coordinates to place ships
    #using other functions, it checks if the coordinates are valid
    #once the ships are all placed, the final board is returned
    board = init_board(rows, columns)
    ship_list = list(ship_sizes)
    not_valid = "Not a valid location."
    while len(ship_list) > 0:
        helper.print_board(board)
        #for each iteration of the loop, the board is printed
        size = ship_list[0]
        loc = helper.get_input("Enter top coordinate for ship " +
        "of size " + str(size) + ":")
        loc = loc.capitalize()
        if cell_loc(loc) != None: #the location entered is valid!
            row, column = cell_loc(loc)
            if valid_ship(board, size, cell_loc(loc)) == True:
                for row_index in range(row, row + size):
                    board[row_index][column] = helper.SHIP
                del ship_list[0]
            else:
                print(not_valid)
        else:
            print(not_valid)
            continue
    return board


def fire_torpedo(board, loc):
    #this function is responsible for firing the torpedo
    #it recieves as input a board and location to fire at
    #if it hits a ship or water, it will change to the relevant tile
    #it then returns the board
    if loc[0] not in range(len(board)) or loc[1] not in range(len(board[0])):
        return board
    elif board[loc[0]][loc[1]] != helper.WATER:
        return board
    if valid_ship(board, 1, loc) == True:
        board[loc[0]][loc[1]] = helper.HIT_WATER
    elif valid_ship(board, 1, loc) == False:
        board[loc[0]][loc[1]] = helper.HIT_SHIP
    return board


def locations(rows, columns):
    #just a locations function, containing all the locations on the board
    locations = [(i, j) for j in range(columns) for i in range(rows)]
    return locations


def pc_generated_locations(ship_sizes, board, locations):
    #this function generates a board for the computer
    #a set of possible locations is created from all locations
    #a random map is built, andvfrom the possible locations 
    # a sorted set of the actual ship locations is returned
    board = board
    all_locations = locations
    possible_locations = set()
    for loc in all_locations:
        if valid_ship(board, min(ship_sizes) , loc) == True:
            possible_locations.add(loc)
    pc_ship_list = list(ship_sizes)
    all_ship_locations = set()
    while len(pc_ship_list) > 0:
        size = pc_ship_list[0]
        loc = helper.choose_ship_location(board, size, possible_locations)
        if valid_ship(board, size, loc) == True: #there's no ship there yet
            row, column = loc
            for row_index in range(row, row + size):
                all_ship_locations.add((row_index, column))
                board[row_index][column] = helper.SHIP
            del pc_ship_list[0] #goodbye ship size
            possible_locations.remove(loc)
        else:
            continue #we try placing that ship size again
    return sorted(all_ship_locations)


def game_is_over(board1, board2):
    #function is executed when the while loop of the game is broken. meaning - 
    #the game is over, and the player is asked if they want to play again
    helper.print_board(board1, board2)
    want_to_play = helper.get_input("Game over. Want to play again?")
    if want_to_play != "Y" and want_to_play != "N":
        print(want_to_play)


def main():
    #this is the game! brining all functions togther
    #the function initiates three boards, as well as calling upon the functions
    #that are relevent for doing so, including the player-built board function.
    all_locations = {(i, j) for j in range(helper.NUM_COLUMNS) for i in range(helper.NUM_ROWS)}
    player_board = create_player_board(helper.NUM_ROWS, helper.NUM_COLUMNS, helper.SHIP_SIZES)
    empty_player_board = init_board(helper.NUM_ROWS, helper.NUM_COLUMNS) 
    #this is the board the computer will see
    pc_board = init_board(helper.NUM_ROWS, helper.NUM_COLUMNS)
    hidden_board = copy.deepcopy(pc_board)
    all_ship_locations = pc_generated_locations(\
        helper.SHIP_SIZES, hidden_board, all_locations)
    #this board will be hidden so the player cannot see it until the game is over
    #for each action taken on the pc's visible board that contains only water -
    #the same action is taken on the hidden board, and marked accordingly
    helper.print_board(player_board, pc_board)
    #a command line i used a lot to help me follow through testing the function
    game_over = False #not yet! we're just getting started
    pc_hit_ships = 0 #we want to count how many ship spots are hit
    #at the end of each turn, if a ship spot was hit, one is added to this sum
    #if the full sum of all ship spaces is reached, the game is over. the loop ends.
    player_hit_ships = 0 #same as above
    ship_loc_sum = sum(list(helper.SHIP_SIZES)) #see above
    while game_over == False: #game loop, two turns start
        loc_input = helper.get_input("Choose target:")
        loc = loc_input.capitalize() #"letternumber" input. 
        #lower case letter is valid, we
        #don't want an error on the receiving end of the coordinates
        if cell_loc(loc) != None:
            hidden_board = fire_torpedo(hidden_board, cell_loc(loc))#this is a valid place to hit a torpedo 
        else:
            print("Invalid target.")
            continue #it's not valid, back to top of the loop.
        if hidden_board == board_before_firing:
            print("Invalid target.")
            continue #it's not valid, back to top of the loop.
        if cell_loc(loc) in all_ship_locations:
            pc_board[cell_loc(loc)[0]][cell_loc(loc)[1]] = helper.HIT_SHIP
            hidden_board[cell_loc(loc)[0]][cell_loc(loc)[1]] = helper.HIT_SHIP
            pc_hit_ships += 1 #if a ship was hit we count, explained above
        else:
            pc_board[cell_loc(loc)[0]][cell_loc(loc)[1]] = helper.HIT_WATER
            hidden_board[cell_loc(loc)[0]][cell_loc(loc)[1]] = helper.HIT_WATER
        pc_hit_loc = helper.choose_torpedo_target(empty_player_board,
        all_locations) #random location
        player_board = fire_torpedo(player_board, pc_hit_loc) #hit player board
        all_locations.remove(pc_hit_loc) #remove used location from location pool
        if player_board[pc_hit_loc[0]][pc_hit_loc[1]] == helper.HIT_SHIP:
            empty_player_board[pc_hit_loc[0]][pc_hit_loc[1]] = helper.HIT_SHIP
            player_hit_ships += 1 #see above
        else:
            empty_player_board[pc_hit_loc[0]][pc_hit_loc[1]] = helper.HIT_WATER
        if player_hit_ships == ship_loc_sum or\
            pc_hit_ships == ship_loc_sum:
            game_over = True #see above
            break
        helper.print_board(player_board, pc_board) #see turn results
    game_is_over(player_board, hidden_board)

if __name__ == "__main__":
    main()
