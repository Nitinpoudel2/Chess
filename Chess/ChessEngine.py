"""This class is responsible for storing all the information
about the current state of a chess game.
It will also be responsible for determining the valid moves at the current state. It will also keep
a moving log.
"""
class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B' : self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves} # dictionary for all the moves
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.stateMate = False

# using the nested class which is not usually recommended unless you have a reason to do it
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove# swapping players
        if move.pieceMoved == 'wk': #  updating the kings location if moved
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0: # make sure that it has a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] =  move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switching the turns back

    """All the moves considering check"""
    def getValidMoves(self):
        # first we have to generate all the possible moves
        moves = self.getAllPossibleMoves()
        # for each move, make the move
        for i in range(len(moves)-1,-1,-1): # when removing from a list go backwards through that list
        # generate all opponents move
            self.makeMove(moves[i])
        # for each of your opponents move, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) # if they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: # either chekcmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.stateMate = True
        else:
            self.checkMate = False
            self.stateMate = False

        return moves

    # determine if the current player is in check
    # to check if the game is over
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.whiteKingLocation[1])

        # determine if the enemy can attack
        #decooupling basically ataking it out from get valid moves and making it own function to check
    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove # switch to opponents turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch the move back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False



    """ Get all the pawn moves for the pawn located at row, col and add these moves to the list """
    def getAllPossibleMoves(self):
        moves = [] # empty list of moves
        for r in range(len(self.board)):# number of rows in the board
            for c in range(len(self.board[r])): # number of cols in a given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: # white pawn moves
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] =="--":
                    moves.append(Move((r,c),(r-2,c), self.board))
            if c-1 >= 0: #captures to the left
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == 'b': # enemy pieces to capture
                    moves.append(Move((r,c),(r-1,c+1), self.board))
        else: #blackpawn moves
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] =="--":
                    moves.append(Move((r,c),(r+2,c), self.board))
            if c-1 >= 0: #captures to the left
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r+1][c+1][0] == 'w': # enemy pieces to capture
                    moves.append(Move((r,c),(r+1,c+1), self.board))
        # add pawn promotions later
#Get all the Rooks moves in the chess game and program it
    def getRookMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1)) # up,left,down, right directions where they move
        enemyColor = 'b' if self.whiteToMove else 'w' # sync way of righting two cases
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8 : # position on the board in between
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space is a valid space so we can move it there
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: # if it is a friendly piece
                        break
                else: # as soon as it gets to a off board then break
                    break

    def getKnightMoves(self,r,c,moves):
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r +m[0]
            endCol = c + m[1]
            if 0<= endRow < 8 and 0<= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol), self.board))

# catch the bug in the bishop moves, it is not moving the bishop in any directions

    def getBishopMoves(self,r,c,moves):
        directions = ((-1,1),(-1,1),(1,-1),(1,1)) # travels only diagonal
        enemyColor = 'b' if self.whiteToMove else 'w'  # sync way of righting two cases
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # position on the board in between
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space is a valid space so we can move it there
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # if it is a friendly piece
                        break
                else:  # as soon as it gets to a off board then break
                    break
# get all the possible moves for queen which is similar to bishop and rook moves
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c, moves)
        self.getBishopMoves(r,c, moves)

#
    def getKingMoves(self,r,c,moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0<= endRow < 8 and 0<= endCol <8 :
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol), self.board))

""" Get all the pawn moves for the pawn located at row, col and add these moves to the list """
class Move():
    # maps the keys to values
    #key : value dictionary function
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3,"6": 2, "7": 1, "8": 0}
    rowsToRanks ={ v: k for k,v in ranksToRows.items()}
    filesToCols = {"a": 0,"b": 1,"c": 2,"d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}

    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    """ Over riding the equals method """
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        # you can add to make this like real chess notations
        return self.getRankFiles(self.startRow, self.startCol) + self.getRankFiles(self.endRow, self.endCol)

    def getRankFiles(self, r, c ):
        return self.colsToFiles[c] + self.rowsToRanks[r]