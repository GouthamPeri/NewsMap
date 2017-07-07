moves, turn = input().split()
moves = moves.split('/')

nextMove = 1
pawn = 'p'
black = True

if turn == 'w':
    nextMove = -1
    pawn = 'P'
    black = False


def moveToRow(move):
    row = []
    for char in move:
        try:
            count = int(char)
            for i in range(count):
                row.append('e')
        except:
            if char == pawn:
                row.append(char)
            elif not black and ord(char) >= ord('A') and ord(char) <= ord('Z'):
                row.append(1)
            elif black and ord(char) >= ord('a') and ord(char) <= ord('z'):
                row.append(1)
            else:
                row.append(0) # enemy pieces

    return row


def movesToChessBoard():
    board = []
    for move in moves:
        board.append(moveToRow(move))
    return board


board = movesToChessBoard()

pawnMoves = []


def generateMove(row, index, nextRow, index2):
    return chr(index + ord('a')) + str(row) + chr(index2 + ord('a')) + str(nextRow)


for i in range(len(board)):
    if pawn in board[i]:
        currentRow = i
        try:
            pawnIndex = board[i].index(pawn)
            nextRow = currentRow + nextMove
            nextRow = nextRow if nextRow < 8 and nextRow >= 0 else None
            if nextRow:
                if pawn == 'P' and currentRow == 6 and board[currentRow - 2][pawnIndex] == 'e':
                    pawnMoves.append(generateMove(8 - currentRow, pawnIndex, 8 - currentRow + 2, pawnIndex))
                elif pawn == 'p' and currentRow == 1 and board[currentRow + 2][pawnIndex] == 'e':
                    pawnMoves.append(generateMove(8 - currentRow, pawnIndex, 8 - currentRow - 2, pawnIndex))
                if board[nextRow][pawnIndex] == 'e':
                    pawnMoves.append(generateMove(8 - currentRow, pawnIndex, 8 - nextRow, pawnIndex))
                if pawnIndex == 0:
                    if board[nextRow][pawnIndex + 1] == 0:
                        pawnMoves.append(generateMove(8 - currentRow, pawnIndex, 8 - nextRow, pawnIndex + 1))
                elif pawnIndex == 7:
                    if board[nextRow][pawnIndex - 1] == 0:
                        pawnMoves.append(generateMove(8 - currentRow, pawnIndex, 8 - nextRow, pawnIndex - 1))
                else:
                    if board[nextRow][pawnIndex + 1] == 0:
                        pawnMoves.append(generateMove(8 - currentRow, pawnIndex, 8 - nextRow, pawnIndex + 1))
                    if board[nextRow][pawnIndex - 1] == 0:
                        pawnMoves.append(generateMove(8 - currentRow, pawnIndex, 8 - nextRow, pawnIndex - 1))
        except:
            pass

representation = repr(pawnMoves).replace("'", "")
print(representation)
