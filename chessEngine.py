"""
This class is responsible for storing all the information about the current state of a chess. It will also be
responsible for determining the valid moves at the current state and keep a move log.
"""
import numpy as np


class GameState:
    def __init__(self):
        self.board = np.array([["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                              ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                              ["--", "--", "--", "--", "--", "--", "--", "--"],
                              ["--", "--", "--", "--", "--", "--", "--", "--"],
                              ["--", "--", "--", "--", "--", "--", "--", "--"],
                              ["--", "--", "--", "--", "--", "--", "--", "--"],
                              ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                              ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]])

        self.moveFunctions = {"p": self.getPawnMoves, "B": self.getBishopMoves, "N": self.getKnightMoves,
                              "R": self.getRookMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)


    def initMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        # Refresh king location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            # Refresh king location
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            self.whiteToMove = not self.whiteToMove


    # Checks are considered
    def getValidMoves(self):
        return self.getAllPossibleMoves()


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # Call the appropriate move function based off of piece type
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(makeMove((r, c), (r-1, c), self.board))
            if r == 6 and self.board[r - 2][c] == "--":
                moves.append(makeMove((r, c), (r - 2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(makeMove((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(makeMove((r, c), (r-1, c+1), self.board))

        else:
            if self.board[r+1][c] == "--":
                moves.append(makeMove((r, c), (r+1, c), self.board))
            if r == 1 and self.board[r + 2][c] == "--":
                moves.append(makeMove((r, c), (r + 2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(makeMove((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(makeMove((r, c), (r+1, c+1), self.board))
        # Add pawn promotions later

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (1, 1), (1, -1), (-1, 1)) # 4 Directions
        targetTurn = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): # Maximum of 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Valid empty space
                        moves.append(makeMove((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == targetTurn:  # Valid target
                        moves.append(makeMove((r, c), (endRow, endCol), self.board))
                        break
                    else:  # Same turn target
                        break
                else:  # Move is off board
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1))  # 4 Directions
        allyTurn = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyTurn:  # Valid target
                        moves.append(makeMove((r, c), (endRow, endCol), self.board))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1)) # 4 Directions
        targetTurn = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): # Maximum of 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # Valid empty space
                        moves.append(makeMove((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == targetTurn: # Valid target
                        moves.append(makeMove((r, c), (endRow, endCol), self.board))
                        break
                    else: # Same turn target
                        break
                else: # Move is off board
                    break
    def getQueenMoves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1))  # 8 Directions
        targetTurn = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # Maximum of 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # Valid empty space
                        moves.append(makeMove((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == targetTurn:  # Valid target
                        moves.append(makeMove((r, c), (endRow, endCol), self.board))
                        break
                    else:  # Same turn target
                        break
                else:  # Move is off board
                    break
    def getKingMoves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1))  # 8 Directions
        allyTurn = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyTurn:  # Valid target
                    moves.append(makeMove((r, c), (endRow, endCol), self.board))


class makeMove:

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # Assigning a identity for each move
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    """
    Override The equals method
    """
    def __eq__(self, other):
        if isinstance(other, makeMove):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        # Can add to make real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



