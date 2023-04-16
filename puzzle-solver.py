from typing import List, Tuple, Set, Optional


# We define the types of a partial picture and a constraint 
# (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


# PART A

# 1.1

def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    '''this function receives as input a picture (2d list),
    and the returns the amount of squares 'visible' to the
    specific square in the desired row and column, including
    undetermined squares. if the square is black, returns 0.'''

    if picture[row][col] == 0:
        return 0
    return min_max_seen_cells(picture, row, col, [0])


# 1.2

def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    '''this function receives as input a picture (2d list),
    and the returns the amount of squares 'visible' to the
    specific square in the desired row and column, not including
    undetermined squares. if the square is black, returns 0.'''

    if picture[row][col] != 1:
        return 0
    return min_max_seen_cells(picture, row, col, [0, -1])


def min_max_seen_cells(picture: Picture, row: int, col: int,
illegal) -> int:
    '''this function executes the code for min_seen_cells() and
    max_seen_cells(), catering to the small differences in
    what is required for each function, namely which squares
    are not visible (i named these 'illegal'). it returns the
    amount of visible squares that aren't illegal according
    to the given function's standards.'''

    visible = 0
    for i in range(row, -1, -1): #iterating backwards
        if picture[i][col] not in illegal:
            visible += 1
        else:
            break #until we hit a block in the view!

    for i in range(row + 1, len(picture)):
        if picture[i][col] not in illegal:
            visible += 1
        else:
            break

    for j in range(col - 1, -1, -1):
        if picture[row][j] not in illegal:
            visible += 1
        else:
            break

    for j in range(col + 1, len(picture[row])):
        if picture[row][j] not in illegal:
            visible += 1
        else:
            break

    return visible #all visible squares are returned



# PART B


def check_constraints(picture: Picture, constraints_set:
     Set[Constraint]) -> int:
    '''this function receives a picture (2-d list) and a set of 
    constraints for some of the squares in the picture. if all 
    constraints are fully satisfied (legal, that is), the function
    returns 1. If at least one is violated, the function returns 0.
    otherwise, it returns 2 - in this case we aren't yet sure wether
    the constraints are satisfied or not due to uncertaintly in
    some of the picture's squares.'''

    legal = 0 #we will count constraints satisfied
    for constraint in constraints_set:
        row, col, seen = constraint #unpack vars
        max_seen = max_seen_cells(picture, row, col)
        min_seen = min_seen_cells(picture, row, col)
        if check_black(picture, row, col):
            if seen != 0:
                return 0
            else:
                legal += 1
        if check_question(picture, row, col):
            if seen >= min_seen and seen <= max_seen:
                continue
            else:
                return 0
        if check_white(picture, row, col):
            if seen == min_seen:
                legal +=1
            elif seen > max_seen or seen < min_seen:
                return 0
            else:
                continue
    return legal_value(len(constraints_set), legal)



def legal_value(set_length, legal):
    '''function assisting constraints checking, if all in
    the set are legal returns 1, else returns 2'''
    if legal == set_length:
        return 1
    else:
        return 2



def check_black(picture: Picture, row: int, col: int) -> bool:
    '''checks if a square is black in a picture (2d list)'''
    if picture[row][col] == 0:
        return True
    return False

def check_question(picture: Picture, row: int, col: int) -> bool:
    '''checks if a square is uncertain (?) in a picture (2d list)'''
    if picture[row][col] == -1:
        return True
    return False

def check_white(picture: Picture, row: int, col: int) -> bool:
    '''checks if a square is white in a picture (2d list)'''
    if picture[row][col] == 1:
        return True
    return False



# PART C

def empty_board(n: int, m: int) -> Picture:
    '''creates empty puzzle board'''
    return [[-1 for i in range(m)] for j in range(n)]

def solve_puzzle(constraints_set: Set[Constraint],
 n: int, m: int) -> Optional[Picture]:
    '''this function receives picture dimensions and a set
    of constraints, and returns one solution picture. this
    is solved recursively with backtracking. good luck to me.'''
    board = empty_board(n, m)
    solved = solve_puzzle_helper(board, constraints_set, 0)
    return solved

def ok_to_place(board, value, constraints, row, col):
    '''checks if a placement of a value is legal'''
    board[row][col] = value
    if check_constraints(board, constraints) == 0:
        return False
    return True



def solve_puzzle_helper(board, constraints_set, ind):
    '''this is a helper function for solve_puzzle().'''
    if ind == (len(board)) * (len(board[0])):
        return board
    row, col = (ind // len(board[0])), (ind % len(board[0]))

    for value in range(0, 2):
        if ok_to_place(board, value, constraints_set, row, col):
            other_board = solve_puzzle_helper(board,
             constraints_set, ind + 1)
            if other_board !=None:
                return other_board #the single board we return

    board[row][col] = -1
    



# PART D



def how_many_solutions(constraints_set: Set[Constraint],
 n: int, m: int) -> int:
    '''this function checks how many solutions there are to
    a given board of this game. similar to the previous
    function solve_puzzle(), except this time it finds all
    possible solutions.'''
    board = empty_board(n, m)
    solution_count = how_many_solutions_helper(
        board, constraints_set, 0, 0)
    return solution_count



def how_many_solutions_helper(board, constraints_set, ind, count) -> int:
    '''this is a helper function for how_many_solutions().'''
    if ind == (len(board)) * (len(board[0])):
        return count +1 #counting solutions
    row, col = (ind // len(board[0])), (ind % len(board[0]))

    for value in range(0, 2):
        if ok_to_place(board, value, constraints_set, row, col):
            count = how_many_solutions_helper(
                board, constraints_set, ind + 1, count)

    board[row][col] = -1
    return count #we are keeping track of the count in recursion




#PART E



def generate_puzzle(picture: Picture) -> Set[Constraint]:
    '''this function generates a function given certain constraints,
    working opposite to the previous functions'''
    rows = len(picture)
    columns = len(picture[0])
    all_constraints = all_constraints_list(picture)
    needed_constraints = generate_checker(
        picture, all_constraints, rows, columns)
    return set(needed_constraints)


def all_constraints_list(picture: Picture) -> List[Constraint]:
    '''this function finds all the constraints for each square in
    a given solved board'''
    constraints = []
    for i in range(len(picture)):
        for j in range(len(picture[0])):
            square_seen = max_seen_cells(picture, i, j)
            constraints.append((i, j, square_seen))
    return constraints

    
            

def generate_checker(picture, constraints, rows, columns):
    '''this function goes through all the constraints
    found for a given picture, and sifts through them to
    find only those that are absolutely necessary'''
    shallow = constraints[::-1]
    for constraint in constraints:
        shallow.remove(constraint)
        if (how_many_solutions(shallow, rows, columns)) == 1 \
            and solve_puzzle({(1, 0, 4)}, 2, 3) == picture:
            continue
        else:
            shallow.append(constraint)
    return shallow



# THE END
