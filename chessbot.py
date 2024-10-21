import chess
import datetime
import random

print("Time: " + str(datetime.datetime.now()))
color = ""
while color != "b" and color != "w":
    color = input("Computer Player? (w=white/b=black):")
    if color == "w":
        mod = 0
        bot = "white"
        player = "Black"
    elif color == "b":
        mod = 1
        bot = "black"
        player = "White"
    else:
        print("Enter b or w")

position = input("Starting FEN position? (hit ENTER for standard starting postion): ")
board = chess.Board()
if position == "":
    pass
else:
    board.set_fen(position)
    print(board)
# deal with case in which position is invalid

turn = 0
# check that it ends when it is checkmate
while not board.is_checkmate():
    if turn % 2 == mod: # computer's turn
        uci_moves = list(board.legal_moves)
        move = random.choice(uci_moves)
        board.push_san(str(chess.Move.from_uci(str(move))))
        print("Bot (as " + bot + "): " + str(move))
    else: # player's turn
        leg_moves = list(board.legal_moves)
        print(leg_moves)
        move = input(player + ": ")
        # check if in legal moves
        while chess.Move.from_uci(move) not in board.legal_moves:
            print("Try again.")
            move = input(player + ": ")
        board.push_san(str(chess.Move.from_uci(move)))
        
    print("New FEN position: " + str(board.fen()))
    print(board)
    turn += 1