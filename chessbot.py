import chess
import datetime
import random
import re

uci_pattern = re.compile("[a-h][0-8][a-h][0-8]")

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

position = None
while position == None:
    position = input("Starting FEN position? (hit ENTER for standard starting postion): ")
    board = chess.Board()
    if position == "":
        pass
    else:
        try:
            board.set_fen(position)
            assert board.is_valid()
        except:
            print("Invalid FEN position")
            position = None
# print(board)

turn = 0
# check that it ends when it is checkmate
while not board.is_checkmate():
    print(board.is_checkmate())
    if turn % 2 == mod: # computer's turn
        uci_moves = list(board.legal_moves)
        cap_list = []
        # go through moves and check for captures
        for move in uci_moves:
            if board.is_capture(move):
                cap_list.append(move)
        # if no captures, choose random
        if len(cap_list)==0:
            move = random.choice(uci_moves)
        # if captures, select from list
        else:
            move = random.choice(cap_list)
        board.push_san(str(chess.Move.from_uci(str(move))))
        print("Bot (as " + bot + "): " + str(move))
    else: # player's turn
        leg_moves = list(board.legal_moves)
        move = input(player + ": ")
        while not uci_pattern.match(move) or chess.Move.from_uci(move) not in board.legal_moves:
            print("Try again. Your valid moves are:")
            print(list(board.legal_moves))
            move = input(player + ": ")
        board.push_san(str(chess.Move.from_uci(move)))
        
    print("New FEN position: " + str(board.fen()))
    print(board)
    turn += 1
# output a message and quit
# say winner