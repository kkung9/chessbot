import chess
import datetime
import random
import re

# regex for a valid for uci input
uci_pattern = re.compile("[a-h][0-8][a-h][0-8]")

# print time before the game starts
print("Time: " + str(datetime.datetime.now()))

# set color of player and bot
color = ""
while color != "b" and color != "w":
    color = input("Computer Player? (w=white/b=black):").lower()
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
    if position == "": # if user enters nothing, start with default board
        pass
    else:
        try: # otherwise, make sure the state of the board can be created
            board.set_fen(position)
            assert board.is_valid()
        except:
            print("Invalid FEN position")
            position = None

print(board)

turn = 0
while not board.is_checkmate():
    if turn % 2 == mod: # computer's turn
        uci_moves = list(board.legal_moves)
        cap_list = []
        # go through moves and check for captures
        for move in uci_moves:
            if board.is_capture(move):
                cap_list.append(move)
        # if no captures available, choose random move
        if len(cap_list)==0:
            move = random.choice(uci_moves)
        # if captures are available, select from list of captures
        else:
            move = random.choice(cap_list)
        # make the mvoe
        board.push_san(str(chess.Move.from_uci(str(move))))
        print("Bot (as " + bot + "): " + str(move))
    else: # player's turn
        leg_moves = list(board.legal_moves)
        move = input(player + ": ")
        while not uci_pattern.match(move) or chess.Move.from_uci(move) not in board.legal_moves: # check that the move is valid
            print("Try again. Your valid moves are:")
            print(list(board.legal_moves))
            move = input(player + ": ")
        # make the move
        board.push_san(str(chess.Move.from_uci(move)))
        
    print("New FEN position: " + str(board.fen()))
    print(board)
    turn += 1

# print who won
print("Game Over")
if (board.outcome().winner and player == "White") or (not board.outcome().winner and player == "Black"):
    print("You won!")
else:
    print("You lost :(")