import chess
import datetime
import random

# print(board.legal_moves)

# print(board)

print("Time: " + str(datetime.datetime.now()))
color = input("Computer Player? (w=white/b=black):")
if color == "w":
    mod = 0
    bot = "white"
    player = "Black"
elif color == "b":
    mod = 1
    bot = "black"
    player = "White"
# case when this is invalid

position = input("Starting FEN position? (hit ENTER for standard starting postion): ")
if position == "":
    board = chess.Board()
# deal with case in which position is invalid
# deal with case in which position is another position

turn = 0
# check that it ends when it is checkmate
while not board.is_checkmate():
    if turn % 2 == mod: # computer's turn
        legal_moves_lst = [board.san(move) for move in board.legal_moves] # make this line nicer
        idx = random.randint(0, len(legal_moves_lst))
        board.push_san(legal_moves_lst[idx])
        leg_moves = list(board.legal_moves)
        print("Bot (as " + bot + "): " + str(leg_moves[idx]))
    else: # player's turn
        leg_moves = list(board.legal_moves)
        print(leg_moves)
        move = input(player + ": ")
        # check if in legal moves
        board.push_san(str(chess.Move.from_uci(move)))
    print("New FEN position: " + str(board.fen()))
    print(board)
    turn += 1