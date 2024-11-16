import chess
import datetime
import random
import re


def scoreMove(board, move):
    if board.is_capture(move):
        if board.is_en_passant(move):
            return 1
        else:
            piece_taken = board.piece_at(move.to_square)
            if piece_taken is not None:
                match piece_taken.piece_type:
                    case chess.PAWN:
                        return 1
                    case chess.KNIGHT:
                        return 3
                    case chess.BISHOP:
                        return 3
                    case chess.ROOK:
                        return 5
                    case chess.QUEEN:
                        return 9
    return 0

def maxMove(board, depth, prevScore):
    # base case
    if depth < 0 or board.is_game_over():
        return None, 0
    #else
    bestScore = float("-inf")
    bestMove = None
    for move in board.legal_moves:
        moveScore = scoreMove(board, move)
        board.push(move)
        score = minMove(board, depth-1, moveScore)[1] + prevScore
        board.pop()
        if score > bestScore:
            bestScore = score
            bestMove = move
    return bestMove, bestScore


def minMove(board, depth, prevScore):
   # base case
    if depth < 0 or board.is_game_over():
        return None, 0
    # else
    bestScore = float("inf")
    bestMove = None
    for move in board.legal_moves:
        moveScore = - scoreMove(board, move)
        board.push(move)
        score = maxMove(board, depth-1, moveScore)[1] + prevScore
        # undoes change
        board.pop()
        # compare the scores 
        if score < bestScore:
            bestScore = score
            bestMove = move
    return bestMove, bestScore




def main():
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
            move, score = maxMove(board, 2, 0)
            print("Best score: " + str(score))
            # make the mvoe
            board.push(move)
            print("Bot (as " + bot + "): " + str(move))
        else: # player's turn
            leg_moves = list(board.legal_moves)
            move = input(player + ": ")
            while not uci_pattern.match(move) or chess.Move.from_uci(move) not in board.legal_moves: # check that the move is valid
                print("Try again. Your valid moves are:")
                print(list(board.legal_moves))
                move = input(player + ": ")
            # make the move
            board.push(chess.Move.from_uci(move))
            
        print("New FEN position: " + str(board.fen()))
        print(board)
        turn += 1

    # print who won
    print("Game Over")
    if (board.outcome().winner and player == "White") or (not board.outcome().winner and player == "Black"):
        print("You won!")
    else:
        print("You lost :(")


main()