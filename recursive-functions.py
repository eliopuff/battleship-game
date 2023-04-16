from typing import Any, List
from ex7_helper import *



# PART A


def mult(x: N, y:int) -> N:
    '''this function is a simple one for solving 
    multiplication problems using recursion and no 
    mathematical operations. runtime is O(n)'''
    if y == 0:
        return 0
    sum = add(x, mult(x, subtract_1(y)))
    return sum



def is_even(n: int) -> bool:
    '''this function determines whether a positive
    integer is even or not, using recursion'''
    if n == 1:
        return False
    if n == 0:
        return True
    is_it_even = is_even(subtract_1(subtract_1(n)))
    return is_it_even
    


def log_mult(x: N, y: int) -> N:
    '''similar to mult(), this function receives two
    numbers and multiplies them recursively. this time,
    the runtime is O(logn)'''
    if y == 0:
        return 0
    if is_odd(y) == False:
        prev = log_mult(x, divide_by_2(y))
        sum = add(prev, prev)
        return sum
    else:
        prev = log_mult(x, divide_by_2(y))
        sum = add(add(x, prev), prev)
        return sum



def is_power(b: int, x: int) -> bool:
    '''this function calculates whether a given int x
    is a power of given int b. if so, returns True. else,
    it returns False. the runtime is O(logb x logx)'''
    if check_zero_one(b, x) == True:
        return is_power_zero_one(b, x)
    if x < b:
        return False
    if x == b:
        return True
    if x > b:
        y = is_power_helper(b, x, b)
        val = is_power(y, x)
    return val

def is_power_helper(b: int, x: int, n: int) -> int: 
    '''this function is a helper function for is_power() and
    assissts in calculating whether x is a power of b'''
    if n==0:
        return 1
    if n < x:
        n = is_power_helper(b, x, log_mult(n, b))
    return n

def check_zero_one(b: int, x: int) -> bool:
    '''checks if either b, x are 0, 1, checking for extreme
    cases. continued is is_power_zero_one().'''
    if b == 0 or x == 0 or b == 1 or x == 1:
        return True
    return False

def is_power_zero_one(b: int, x: int) -> bool:
    '''this function takes the extreme cases of b, x as 1, 0
    and determines whether there are viable options for each
    accordingly, return a bool value.'''
    if b == 0:
        if x == 0 or x == 1:
            return True
    if b == 1:
        if x == 1:
            return True
    if x == 1: #all numbers to the power of 0 == 1!
        return True
    if x == 0:
        if b == 0:
            return True
    return False #our default, to be safe




def reverse(s: str) -> str:
    '''this function receives as input a string and returns
    the string reversed.'''
    if len(s) <= 1:
        return s
    reverse = reverse_helper(s, '', len(s))
    return reverse


def reverse_helper(s: str, t: str, l: int) -> str:
    '''this function is a helper function for the recursive
    -based reverse() function.'''
    if len(t) == len(s):
        return t
    string = reverse_helper(s, 
    append_to_end(t, s[l - 1]), l - 1)
    return string


# PART B

def play_hanoi(hanoi: Any, n: int, \
     src: Any, dest: Any, temp: Any) -> None:
    '''this function runs the game hanoi, recursively.'''
    if n <= 0:
        return
    if n == 1:
        hanoi.move(src, dest)
        return
    play_hanoi(hanoi, n - 1, src, temp, dest)
    hanoi.move(src, dest)
    play_hanoi(hanoi, n - 1, temp, dest, src)
    



def number_of_ones(n: int) -> int:
    '''this functions counts the number of ones in a series
    of numbers from 0 to n, recursively'''
    if n != 0:
        return number_of_ones(n-1) + ones_helper(n)
    return ones_helper(n)


def ones_helper(num: int) -> int:
    '''this function counts the number of ones in a number
    using modulu and devision, recursively until reaching 0'''
    if num == 0:
        return 0
    if (num % 10) == 1:
        return ones_helper(num//10) + 1
    else:
        return ones_helper(num//10)



def compare_2d_lists(l1: List[List[int]], 
l2: List[List[int]]) -> bool:
    '''this function recursively checks if two 2d lists
    are identical or not.'''
    if (len(l1) != len(l2)):
        return False
    if len(l1) == 0 and len(l2) == 0:
        return True
    else:
        return compare_list(l1, l2, len(l1))



def compare_list(l1: List[List[int]], 
l2: List[List[int]], x: int) -> bool:
    '''helper function for previous comparing one. works
    recursively going over list indexes'''
    x -= 1
    if len(l1) != len(l2):
        return False
    else:
        if x > 0:
            return compare_list(l1, l2, x) and \
                compare_help(l1, l2, x, len(l1[x]) - 1)
    return compare_help(l1, l2, x, len(l1[x]) - 1)


def compare_help(l1: List[List[int]], 
l2: List[List[int]], x: int, y: int) -> bool:
    '''helper function for previous comparing ones. works
    recursively going over list indexes'''
    if len(l1[x]) != len(l2[x]):
        return False
    if len(l1[x]) == 0 and  len(l2[x]) == 0:
        return True
    if y > 0:
        return compare_help(l1, l2, x, y - 1) and\
            (l1[x][y] == l2[x][y])
    return (l1[x][y] == l2[x][y])




def magic_list(n: int) -> List[Any]:
    '''this function creates a magic list of empty lists,
    while the pattern is of an ordinal number type.'''
    if n == 0:
        return []
    else:
        l = magic_list(n-1)
        l.append(magic_list(n-1))
        return l
