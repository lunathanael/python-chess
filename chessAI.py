import random

pieceScore = {"K": 20000, "Q": 900, "R": 500, "N": 320, "B": 330, "p": 100}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 2
CAPTURES = 3
MAX_DEPTH = DEPTH + CAPTURES

PawnPhase = 0
KnightPhase = 1
BishopPhase = 1
RookPhase = 2
QueenPhase = 4
TotalPhase = PawnPhase*16 + KnightPhase*4 + BishopPhase*4 + RookPhase*4 + QueenPhase*2
phase = TotalPhase
bestLine = [None] * DEPTH
bestEval = 0
capture = False



knightScores = [
    [-50,-40,-30,-30,-30,-30,-40, -50],
    [-40,-20,  0,  0,  0,  0,-20, -40],
    [-30,  0, 10, 15, 15, 10,  0, -30],
    [-30,  5, 15, 20, 20, 15,  5, -30],
    [-30,  5, 15, 20, 20, 15,  5, -30],
    [-30,  0, 10, 15, 15, 10,  0, -30],
    [-40,-20,  0,  0,  0,  0,-20, -40],
    [-50,-40,-30,-30,-30,-30,-40, -50]]

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
    [-30,-40,-40,-50,-50,-40,-40,-30,],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]]

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
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  5,  5,  5,  5,  0,  0]]

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
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]]

egPawnScores = [
    [0,   0,   0,   0,   0,   0,   0,   0],
    [178, 173, 158, 134, 147, 132, 165, 187],
     [94, 100,  85,  67,  56,  53,  82,  84],
     [32,  24,  13,   5,  -2,   4,  17,  17],
     [13,   9,  -3,  -7,  -7,  -8,   3,  -1],
     [4,   7,  -6,   1,   0,  -5,  -1,  -8],
     [13,   8,   8,  10,  13,   0,   2,  -7],
      [0,   0,   0,   0,   0,   0,   0,   0]
]

bishopScores = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]]

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
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]]

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


piecePositionScores = {"N": knightScores, "K": kingScores, "B": bishopScores, "p": pawnScores, "R": rookScores, "Q": queenScores}
egPiecePositionScores = {"N": egKnightScores, "K": egKingScores, "B": egBishopScores, "p": egPawnScores, "R": egRookScores, "Q": egQueenScores}


def findBestMove(gs, validMoves, turn, returnQueue):
    global nextMove, counter
    counter = 0
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    #findGreedyMove(gs, validMoves, DEPTH, gs.whiteToMove)
    printEval(nextMove, bestEval, turn)
    returnQueue.put(nextMove)

def findRandomMove(validMoves): # Find Random Move
    if len(validMoves) != 0:
        return validMoves[random.randint(0, len(validMoves) - 1)]
    else:
        return None

# Greedy score based 2 depth
def findGreedyMove(gs, validMoves): # Find best move based off material
    turnMultiplier = 1 if gs.whiteToMove else -1

    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None

    random.shuffle(validMoves) # Variation
    for playerMove in validMoves:
        gs.initMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        if gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.initMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
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
            gs.initMove(move)
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
            gs.initMove(move)
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
        gs.initMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter, favLine,  bestEval, capture
    # Move Ordering - Implement later
    maxScore = -CHECKMATE - 1

    if (depth <= 0 and not capture) or (depth < -CAPTURES):
        return turnMultiplier * scoreBoard(gs)

    for move in validMoves:
        gs.initMove(move)
        capture = move.isCapture
        phase = gamePhase(gs.board)
        counter += 1
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                bestEval = score
            if depth > 0:
                bestLine[DEPTH - depth] = move

        gs.undoMove()
        alpha = max(maxScore, alpha)

        if alpha >= beta:
            break
    return maxScore


def gamePhase(board):
    # find all pieces, remove later
    pieceCounts = [0] * 12
    pieceIndex = {"wp":0 , "wN": 1, "wB": 2, "wR": 3, "wQ": 4, "bp": 5, "bN": 6, "bB": 7, "bR": 8, "bQ": 9, "wK": 10, "bK": 11}
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
    phase -= pieceCounts[3] * RookPhase
    phase -= pieceCounts[4] * QueenPhase
    phase -= pieceCounts[5] * PawnPhase
    phase -= pieceCounts[6] * KnightPhase
    phase -= pieceCounts[7] * BishopPhase
    phase -= pieceCounts[8] * RookPhase
    phase -= pieceCounts[9] * QueenPhase

    phase = (phase * 256 + (TotalPhase / 2)) / TotalPhase

    return phase


# Positive score is good for white
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE # Black Wins
        else:
            return CHECKMATE # White wins
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--": # Score Positionally
                piecePositionScore = 0
                if square[0] == "w":
                    index = row
                else:
                    index = 7 - row
                    piecePositionScore = ((piecePositionScores[square[1]][index][col] * (256 - phase))
                                          + (egPiecePositionScores[square[1]][index][col] * phase)) / 256
            if square[0] == "w":
                score += pieceScore[square[1]] + piecePositionScore * 0.2
            if square[0] == "b":
                score -= pieceScore[square[1]] + piecePositionScore * 0.2
    return score


def winningPercentage(pawnAdvantage):
    return 1 / (1 + 10**(-pawnAdvantage / 4))


def scoreMaterial(board): # Calculate material
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
    winChance = winningPercentage(mult * score / 100)
    print("Engine Move:", move, ", Win estimate:", str(round(winChance * 100, 2)), "%, ", "Evaluation:",
          str(round(score / 100, 2)), end=" , Line: ")
    for i in range(0, len(bestLine)):
        print(str(bestLine[i]), end=" ")
    print("Nodes: ", counter)
