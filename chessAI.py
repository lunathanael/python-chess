import random
import numpy as np

centipawnValue = 160
pieceScore = {"K": 20000, "Q": 1160, "R": 670, "N": 450, "B": 480, "p": centipawnValue}
CHECKMATE = 100000
STALEMATE = 0
DRAW = 0
DEPTH = 2 # Halfmoves, recommened to be even
ATTACK = 7 # Halfmoves, recommened to be Depth + attacks is even, captures or checks
MAX_DEPTH = DEPTH + ATTACK

PawnPhase = 0
KnightPhase = 1
BishopPhase = 1
RookPhase = 2
QueenPhase = 4
TotalPhase = PawnPhase * 16 + KnightPhase * 4 + BishopPhase * 4 + RookPhase * 4 + QueenPhase * 2
phase = TotalPhase
bestLine = [None] * DEPTH
capture = False
memo = np.zeros((1,2))
hashTable = 0
bishopCombo = [False, False]
bestEval = 0
lineLog = 0


knightScores = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-50, -50, -30, -30, -30, -30, -50, -50]]

egKnightScores = [
    [-58, -38, -13, -28, -31, -27, -63, -99],
    [-25, -8, -25, -2, -9, -25, -24, -52],
    [-24, -20, 10, 9, -1, -9, -19, -41],
    [-17, 3, 22, 22, 22, 11, 8, -18],
    [-18, -6, 16, 25, 16, 17, 4, -18],
    [-23, -3, -1, 15, 10, -3, -20, -22],
    [-42, -20, -10, -5, -2, -20, -23, -44],
    [-29, -51, -23, -15, -22, -18, -50, -64]
]

kingScores = [
    [-30, -40, -40, -50, -50, -40, -40, -30, ],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]]

egKingScores = [
    [-74, -35, -18, -18, -11, 15, 4, -17],
    [-12, 17, 14, 17, 17, 38, 23, 11],
    [10, 17, 23, 15, 20, 45, 44, 13],
    [-8, 22, 24, 27, 26, 33, 26, 3],
    [-18, -4, 21, 24, 27, 23, 9, -11],
    [-19, -3, 11, 21, 23, 16, 7, -9],
    [-27, -11, 4, 13, 14, 4, -5, -17],
    [-53, -34, -21, -11, -28, -14, -24, -43]]

rookScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 2, 6, 6, 6, 6, 2, -5],
    [1, 0, 5, 5, 5, 5, 0, 1]]

egRookScores = [
    [13, 10, 18, 15, 12, 12, 8, 5],
    [11, 13, 13, 11, -3, 3, 8, 3],
    [7, 7, 7, 5, 4, -3, -5, -3],
    [4, 3, 13, 1, 2, 1, -1, 2],
    [3, 5, 8, 4, -5, -6, -8, -11],
    [-4, 0, -5, -1, -7, -12, -8, -16],
    [-6, -6, 0, 2, -9, -9, -11, -3],
    [-9, 2, 3, -1, -5, -13, 4, -20]
]

pawnScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 12, 25, 25, 12, 5, 5],
    [0, 4, 32, 34, 35, 32, 4, 0],
    [5, 17, 20, 20, 20, 20, 17, 5],
    [-5, -6, 0, -40, -40, 0, -6, -5],
    [0, 0, 0, 0, 0, 0, 0, 0]]

egPawnScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [178, 173, 158, 134, 147, 132, 165, 187],
    [94, 100, 85, 67, 56, 53, 82, 84],
    [32, 24, 13, 5, -2, 4, 17, 17],
    [13, 9, -3, -7, -7, -8, 3, -1],
    [4, 7, -6, 1, 0, -5, -1, -8],
    [13, 8, 8, 10, 13, 0, 2, -7],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

bishopScores = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 11, 0, 0, 0, 0, 11, -10],
    [-10, -10, -20, -10, -10, -20, -10, -10]]

egBishopScores = [
    [-14, -21, -11, -8, -7, -9, -17, -24],
    [-8, -4, 7, -12, -3, -13, -4, -14],
    [2, -8, 0, -1, -2, 6, 0, 4],
    [-3, 9, 12, 9, 14, 10, 3, 2],
    [-6, 3, 13, 19, 7, 10, -3, -9],
    [-12, -3, 8, 10, 13, 3, -7, -15],
    [-14, -18, -7, -1, 4, -9, -15, -27],
    [-23, -9, -23, -5, -9, -16, -5, -17]
]

queenScores = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -5, -5, -5, -10, -10, -20]]

egQueenScores = [
    [-9, 22, 22, 27, 27, 19, 10, 20],
    [-17, 20, 32, 41, 58, 25, 30, 0],
    [-20, 6, 9, 49, 47, 35, 19, 9],
    [3, 22, 24, 45, 57, 40, 57, 36],
    [-18, 28, 19, 47, 31, 34, 39, 23],
    [-16, -27, 15, 6, 9, 17, 10, 5],
    [-22, -23, -30, -16, -16, -23, -36, -32],
    [-33, -28, -22, -43, -5, -32, -20, -41]
]

piecePositionScores = {"N": knightScores, "K": kingScores, "B": bishopScores, "p": pawnScores, "R": rookScores,
                       "Q": queenScores}
egPiecePositionScores = {"N": egKnightScores, "K": egKingScores, "B": egBishopScores, "p": egPawnScores,
                         "R": egRookScores, "Q": egQueenScores}


def findBestMove(gs, validMoves, turn, returnQueue):
    global nextMove, counter, favLine, capture, bestEval
    counter = 0
    nextMove = None
    random.shuffle(validMoves)
    bestEval = findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    #bestEval = minimax(gs, validMoves, 0, -CHECKMATE, CHECKMATE, gs.whiteToMove, attack=False)
    # findGreedyMove(gs, validMoves, DEPTH, gs.whiteToMove)
    gs.initMove(nextMove, False, True)
    printEval(nextMove, bestEval, turn)
    returnQueue.put(nextMove)

def findWorstMove(gs, validMoves, turn, returnQueue):
    global nextMove, counter, favLine, capture, bestEval
    counter = 0
    nextMove = None
    random.shuffle(validMoves)
    bestEval = findWorstMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    # findGreedyMove(gs, validMoves, DEPTH, gs.whiteToMove)
    gs.initMove(nextMove, False, True)
    printEval(nextMove, bestEval, turn)
    returnQueue.put(nextMove)


def findRandomMove(validMoves):  # Find Random Move
    if len(validMoves) != 0:
        return validMoves[random.randint(0, len(validMoves) - 1)]
    else:
        return None


# Greedy score based 2 depth
def findGreedyMove(gs, validMoves):  # Find best move based off material
    turnMultiplier = 1 if gs.whiteToMove else -1

    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None

    random.shuffle(validMoves)  # Variation
    for playerMove in validMoves:
        gs.initMove(playerMove, True)
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        if gs.draw:
            opponentMaxScore = DRAW
        if gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.initMove(opponentsMove, True)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                elif gs.draw:
                    score = DRAW
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)

                opponentMaxScore = max(opponentMaxScore, score)

                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()

    return bestPlayerMove


# Helper method to first recursive call.
def findGreedyMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    # Check if terminal move
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.initMove(move, True)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.initMove(move, True)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove

    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.initMove(move, True)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier, attack=False): # Generating nonvalid moves
    global nextMove, counter, favLine, bestEval, lineLog
    # Move Ordering - Implement later
    maxScore = -CHECKMATE - 1
    counter += 1

    if (depth <= 0 and not attack) or (depth < -ATTACK):

        """        hashOf = hash(getFen(gs.board, gs.enpassantPossible, gs.whiteToMove, gs.currentCastlingRights))
        indexx = ind(memo, hashOf)
         # Hashing does not change speed :(
        if indexx == None:
            returnScore = turnMultiplier * scoreBoard(gs)
            memo = np.vstack((memo, [hashOf, returnScore]))
            return returnScore
        else:
            returnScore = memo[list(indexx)[0], 1]
            hashTable += 1
            return returnScore"""
        return turnMultiplier * scoreBoard(gs)
    else:
        attack = False

    for move in validMoves:
        gs.initMove(move, True)
        nextMoves = gs.getValidMoves()
        attack = (move.isCapture or gs.check)
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier, attack)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
            if depth > 0:
                if depth == 1:
                    lineLog += 1
                bestLine[DEPTH - depth] = move
        gs.undoMove()
        alpha = max(maxScore, alpha)

        if alpha >= beta:
            break
    return maxScore


def minimax(gs, validMoves, depth, alpha, beta, whiteToMove, attack=False):

    if (depth >= DEPTH and not attack) or (depth >= MAX_DEPTH):
        return scoreBoard(gs)

    if whiteToMove:
        bestVal = -CHECKMATE - 1
        for move in validMoves:
            gs.initMove(move, True)
            nextMoves = gs.getValidMoves()
            attack = (move.isCapture or gs.check)
            value = minimax(gs, validMoves, depth + 1, alpha, beta, False, attack)
            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal

    else:
        bestVal = +CHECKMATE + 1
        for move in validMoves:
            gs.initMove(move, True)
            nextMoves = gs.getValidMoves()
            attack = (move.isCapture or gs.check)
            value = minimax(gs, validMoves, depth + 1, alpha, beta, True, attack)
            bestVal = min(bestVal, value)
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return bestVal




def findWorstMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier, attack=False): # Generating nonvalid moves
    global nextMove, counter, favLine, bestEval
    # Move Ordering - Implement later
    maxScore = CHECKMATE + 1
    counter += 1

    if (depth <= 0 and not attack) or (depth < -ATTACK):

        """        hashOf = hash(getFen(gs.board, gs.enpassantPossible, gs.whiteToMove, gs.currentCastlingRights))
        indexx = ind(memo, hashOf)
         # Hashing does not change speed :(
        if indexx == None:
            returnScore = turnMultiplier * scoreBoard(gs)
            memo = np.vstack((memo, [hashOf, returnScore]))
            return returnScore
        else:
            returnScore = memo[list(indexx)[0], 1]
            hashTable += 1
            return returnScore"""
        return turnMultiplier * scoreBoard(gs)
    else:
        attack = False

    for move in validMoves:
        gs.initMove(move, True)
        nextMoves = gs.getValidMoves()
        attack = (move.isCapture or gs.check)
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier, attack)
        if score < maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
            if depth > 0:
                bestLine[DEPTH - depth] = move
        gs.undoMove()
        alpha = min(maxScore, alpha)

        if alpha <= beta:
            break
    return maxScore


def getFen(board, enp, turn, castle):
    spaces = 0
    FEN = ""
    for row in range(len(board)):
        for col in range(len(board[row])):
            square = board[row][col]
            if square == "--":
                spaces += 1
                continue
            else:
                if spaces != 0:
                    FEN += str(spaces)
                    spaces = 0
                piece = square[1]
                if square == "wp":
                    piece = piece.capitalize()
                if square[0] == "b":
                    piece = piece.lower()
                FEN += piece
        if spaces != 0:
            FEN += str(spaces)
            spaces = 0
        if row != 7:
            FEN += "/"
    if turn:
        FEN += " w "
    else: FEN += " b "

    if castle.wks:
        FEN += "K"
    if castle.wqs:
        FEN += "Q"
    if castle.bks:
        FEN += "k"
    if castle.bqs:
        FEN += "q"

    if enp != ():
        FEN += " " + getRankFile(list(enp)[0], list(enp)[1])
    return FEN

ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
rowsToRanks = {v: k for k, v in ranksToRows.items()}
filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
colsToFiles = {v: k for k, v in filesToCols.items()}


def getRankFile(r, c):
    return colsToFiles[c] + rowsToRanks[r]


def ind(array, item):
    for idx, val in np.ndenumerate(array):
        if val == item:
            return idx

def gamePhase(board):
    # find all pieces, remove later
    pieceCounts = [0] * 12
    pieceIndex = {"wp": 0, "wN": 1, "wB": 2, "wR": 3, "wQ": 4, "bp": 5, "bN": 6, "bB": 7, "bR": 8, "bQ": 9, "wK": 10,
                  "bK": 11}
    for row in range(len(board)):
        for col in range(len(board[row])):
            square = board[row][col]
            if square == "--":
                continue
            else:
                pieceCounts[pieceIndex[square]] += 1

    phase = TotalPhase

    phase -= pieceCounts[0] * PawnPhase
    phase -= pieceCounts[1] * KnightPhase
    phase -= pieceCounts[2] * BishopPhase
    if pieceCounts[2] == 2:
        bishopCombo[0] = True
    phase -= pieceCounts[3] * RookPhase
    phase -= pieceCounts[4] * QueenPhase
    phase -= pieceCounts[5] * PawnPhase
    phase -= pieceCounts[6] * KnightPhase
    phase -= pieceCounts[7] * BishopPhase
    if pieceCounts[7] == 2:
        bishopCombo[1] = True
    phase -= pieceCounts[8] * RookPhase
    phase -= pieceCounts[9] * QueenPhase

    phase = (phase * 256 + (TotalPhase / 2)) / TotalPhase

    return phase


# Positive score is good for white
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return CHECKMATE  # Black Wins
        else:
            return -CHECKMATE  # White wins
    elif gs.staleMate:
        return STALEMATE
    elif gs.draw:
        return DRAW

    score = 0
    phase = gamePhase(gs.board)
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":  # Score Positionally
                piecePositionScore = 0
                if square[0] == "w":
                    index = row
                else:
                    index = 7 - row
                piecePositionScore = ((piecePositionScores[square[1]][index][col] * (256 - phase)) + (egPiecePositionScores[square[1]][index][col] * phase)) / 256
            if square[0] == "w":
                score += (pieceScore[square[1]] + piecePositionScore * 0.05)
            if square[0] == "b":
                score -= (pieceScore[square[1]] + piecePositionScore * 0.05)
    if gs.castled[0]:
        score += 0.9 * centipawnValue
    elif not gs.currentCastlingRights.wqs and not gs.currentCastlingRights.bks:
        score -= 1 * centipawnValue
    if gs.castled[1]:
        score -= 0.9 * centipawnValue
    elif not gs.currentCastlingRights.bqs and not gs.currentCastlingRights.bks:
        score += 1.2 * centipawnValue


    # Bishop combo 700
    if bishopCombo[0]:
        score += 0.7 * centipawnValue
    if bishopCombo[1]:
        score -= 0.7 * centipawnValue
    return score

def winningPercentage(pawnAdvantage):
    return 1 / (1 + 10 ** (-pawnAdvantage / 4))


def scoreMaterial(board):  # Calculate material
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            if square[0] == "b":
                score -= pieceScore[square[1]]

    return score


def printEval(move, score, turn):
    mult = 1 if turn else -1
    winChance = winningPercentage(score / centipawnValue)
    print("Engine Move:", move, ", Win estimate:", str(round(winChance * 100, 2)), "%, ", "Evaluation:",
          str(round(mult * score / 100, 2)), end=" , Line: ")
    for i in range(0, len(bestLine)):
        print(str(bestLine[i]), end=" ")
    print("Nodes: ", counter)
    #print(hashTable)
