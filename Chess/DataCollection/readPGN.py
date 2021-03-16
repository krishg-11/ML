import chess.pgn as cpgn
import os

files = sorted(os.listdir("Images"), key= lambda x: os.path.getmtime(f"Images/{x}"))

pgnFile = open("Anderssen.pgn")
first_game = cpgn.read_game(pgnFile)

board = first_game.board()
num = 0
for i,move in enumerate(first_game.mainline_moves()):
    if(i==13): break
    FEN = board.fen().split(" ")[0].replace("/","_")
    print(FEN)
    for _ in range(8):
        file = files.pop(0)
        os.rename(f"Images/{file}", f"Images/{FEN}_{num}.jpg")
        num += 1
    board.push(move)