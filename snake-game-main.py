import argparse
import game_utils
from snake_game import SnakeGame
from game_display import GameDisplay
from board import Board
from const import *
from snake import Snake
from apple import Apple



def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:
  
    # INIT OBJECTS

    board = Board(args.width, args.height)
    snake = Snake(BLACK, UP, (args.width//2, args.height//2), (args.width//2, args.height//2 - 2))
    game = SnakeGame(board, args.apples, args.walls, args.rounds, args.width, args.height)
    gd.show_score(0)
    # DRAW BOARD
    game.draw_board(gd)
    board.place_snake(snake)

    # END OF ROUND 0
    while not game.is_over(snake):
        # CHECK KEY CLICKS
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        # UPDATE OBJECTS
        game.update_objects()
        # DRAW BOARD
        game.draw_board(gd)
        # WAIT FOR NEXT ROUND:
        game.end_round()
        gd.end_round()
