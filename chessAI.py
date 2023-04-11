import random
import numpy as np
from timeit import default_timer as timer

centipawnValue = 100
pieceScore = {"K": 0, "Q": centipawnValue * 9.5, "R": centipawnValue * 4.5, "N": centipawnValue * 3, "B": centipawnValue * 3.0, "p": centipawnValue}
CHECKMATE = 100000
STALEMATE = 0
DRAW = 0
DEPTH = 4 # Halfmoves, recommened to be even
ATTACK = "N/A" # Halfmoves, recommened to be Depth + attacks is even, captures or checks
MAX_DEPTH = 8

PawnPhase = 0
KnightPhase = 1
BishopPhase = 1
RookPhase = 2
QueenPhase = 4
TotalPhase = PawnPhase * 16 + KnightPhase * 4 + BishopPhase * 4 + RookPhase * 4 + QueenPhase * 2
phase = TotalPhase
bestLine = [None] * DEPTH
memo = np.zeros((1,2))
hashTable = 0
bishopCombo = [False, False]
bestEval = 0
movesEvaluated = 0

knightScores = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]


egKnightScores = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

kingScores = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]

egKingScores = [
    50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]

rookScores = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

egRookScores = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

pawnScores = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, -5, -60, -65, -5, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]

egPawnScores = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]

bishopScores = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

egBishopScores = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

queenScores = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

egQueenScores = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

piecePositionScores = {"N": knightScores, "K": kingScores, "B": bishopScores, "p": pawnScores, "R": rookScores,
                       "Q": queenScores}
egPiecePositionScores = {"N": egKnightScores, "K": egKingScores, "B": egBishopScores, "p": egPawnScores,
                         "R": egRookScores, "Q": egQueenScores}


def findBestMove(gs, validMoves, turn, returnQueue):
    global nextMove, counter, favLine, capture, bestEval, movesEvaluated
    counter = 0
    nextMove = None
    #sstart = timer()
    #gs.getValidMoves()
    #endd = timer()
    #print(endd-sstart)
    movesEvaluated = 0
    start = timer()
    #bestEval = findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    bestEval = findMoveMinMax(gs, validMoves, 0, gs.whiteToMove, -CHECKMATE, CHECKMATE)
    # findGreedyMove(gs, validMoves, DEPTH, gs.whiteToMove)
    end = timer()
    sec = end - start
    if nextMove == None:
        nextMove = findRandomMove(validMoves)
        print("Gave Up")
    gs.initMove(nextMove, False, True)
    printEval(nextMove, bestEval, turn, sec)
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

def findGreedyMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove, alpha, beta, capture=False):
    global nextMove, counter, movesEvaluated
    # Check if terminal move
    if (depth >= DEPTH and not capture) or (depth >= MAX_DEPTH):
        return scoreBoard(gs)
    if gs.draw:
        return DRAW

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            counter += 1
            if depth == 0:
                movesEvaluated += 1
            gs.initMove(move, True)
            attack = move.isCapture
            nextMoves = gs.getValidCapturesFirst()
            score = findMoveMinMax(gs, nextMoves, depth + 1, False, alpha, beta, attack)
            if score > maxScore:
                maxScore = score
                if depth == 0:
                    nextMove = move
            gs.undoMove()
            alpha = max(alpha, maxScore)
            if depth == 0:
                print(end="\r")
                print("Current Engine move:", nextMove, ", eval:", round(maxScore, 3), ", Moves evaluated:", movesEvaluated, "/", len(validMoves),
                      ", Nodes Traversed:", counter, end="")
            if beta <= alpha:
                break
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            counter += 1
            if depth == 0:
                movesEvaluated += 1
            gs.initMove(move, True)
            attack = move.isCapture
            nextMoves = gs.getValidCapturesFirst()
            score = findMoveMinMax(gs, nextMoves, depth + 1, True, alpha, beta, attack)
            if score < minScore:
                minScore = score
                if depth == 0:
                    nextMove = move
            gs.undoMove()
            beta = min(beta, minScore)
            if depth == 0:
                print(end="\r")
                print("Current Engine move:", nextMove, ", Eval:", round(minScore, 3), ", Moves evaluated:", movesEvaluated, "/", len(validMoves),
                      ", Nodes Traversed:", counter, end="")
            if beta <= alpha:
                break
        return minScore


def findMoveLeastMove(gs, validMoves, depth, whiteToMove, alpha, beta, capture=False):
    global nextMove, counter, movesEvaluated
    # Check if terminal move
    if (depth >= DEPTH):
        return len(validMoves)

    if not whiteToMove:
        maxScore = 0
        for move in validMoves:
            counter += 1
            if depth == 0:
                movesEvaluated += 1
            gs.initMove(move, True)
            attack = move.isCapture
            nextMoves = gs.getValidCapturesFirst()
            score = findMoveMinMax(gs, nextMoves, depth + 1, False, alpha, beta, attack)
            if score > maxScore:
                maxScore = score
                if depth == 0:
                    nextMove = move
            gs.undoMove()
            alpha = max(alpha, maxScore)
            if depth == 0:
                print(end="\r")
                print("Current Engine move:", nextMove, ", eval:", round(maxScore, 3), ", Moves evaluated:", movesEvaluated, "/", len(validMoves),
                      ", Nodes Traversed:", counter, end="")
            if beta <= alpha:
                break
        return maxScore
    else:
        minScore = 1000
        for move in validMoves:
            counter += 1
            if depth == 0:
                movesEvaluated += 1
            gs.initMove(move, True)
            attack = move.isCapture
            nextMoves = gs.getValidCapturesFirst()
            score = findMoveMinMax(gs, nextMoves, depth + 1, True, alpha, beta, attack)
            if score < minScore:
                minScore = score
                if depth == 0:
                    nextMove = move
            gs.undoMove()
            beta = min(beta, minScore)
            if depth == 0:
                print(end="\r")
                print("Current Engine move:", nextMove, ", Eval:", round(minScore, 3), ", Moves evaluated:", movesEvaluated, "/", len(validMoves),
                      ", Nodes Traversed:", counter, end="")
            if beta <= alpha:
                break
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
    global nextMove, counter, favLine, bestEval
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
                bestLine[DEPTH - depth] = move
        gs.undoMove()
        alpha = max(maxScore, alpha)

        if alpha >= beta:
            break
    return maxScore

def findWorstMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier, attack=False): # Generating nonvalid moves
    global nextMove, counter, favLine, bestEval
    # Move Ordering - Implement later
    maxScore = CHECKMATE + 1
    counter += 1

    if (depth <= 0 and not attack) or (depth < -MAX_DEPTH):

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

ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
rowsToRanks = {v: k for k, v in ranksToRows.items()}
filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
colsToFiles = {v: k for k, v in filesToCols.items()}

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
            return -CHECKMATE  # Black Wins
        else:
            return CHECKMATE  # White wins
    elif gs.staleMate:
        return STALEMATE
    elif gs.draw: # ??
        return DRAW

    score = 0
    phase = gamePhase(gs.board)
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":  # Score Positionally
                piecePositionScore = 0
                if square[0] == "w":
                    index = 7 - row
                else:
                    index = row
                pos = col + index * 8
                piecePositionScore = ((piecePositionScores[square[1]][pos] * (256 - phase)) + (egPiecePositionScores[square[1]][pos] * phase)) / 256
            if square[0] == "w":
                score += (pieceScore[square[1]] + piecePositionScore*0.5)
            if square[0] == "b":
                score -= (pieceScore[square[1]] + piecePositionScore*0.5)
    phaseConst = centipawnValue * (256 - phase) / 256
    if gs.castled[0]:
        score += 0.9 * phaseConst
    elif not gs.currentCastlingRights.wqs and not gs.currentCastlingRights.bks:
        score -= 1 * phaseConst
    if gs.castled[1]:
        score -= 0.9 * phaseConst
    elif not gs.currentCastlingRights.bqs and not gs.currentCastlingRights.bks:
        score += 1 * phaseConst


    # Bishop combo 700
    if bishopCombo[0]:
        score += 0.7 * centipawnValue
    if bishopCombo[1]:
        score -= 0.7 * centipawnValue
    return score / centipawnValue

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

def printEval(move, score, turn, sec):
    mult = 1 if turn else -1
    winChance = winningPercentage(mult * score)
    print()
    print("Engine Move:", move, ", Win estimate:", str(round(winChance * 100, 2)), "%, ", "eval:",
          str(round(score, 3)), ", Time:", round(sec, 4), ", nps:", round(counter / sec, 1), "\n")
    #for i in range(0, len(bestLine)):
        #print(str(bestLine[i]), end=" ")
