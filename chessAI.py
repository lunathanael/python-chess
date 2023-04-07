import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "N": 3, "B": 3, "p": 1}
CHECKMATE = 10000
STALEMATE = 0
DEPTH = 3


knightScores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]]

kingScores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [2, 1, 1, 1, 1, 1, 1, 2],
    [2, 3, 4, 1, 1, 1, 4, 3]]

rookScores = [
    [3, 2, 2, 4, 4, 2, 2, 3],
    [2, 4, 4, 4, 4, 4, 4, 2],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 4, 4, 4, 4, 4, 4, 2],
    [3, 2, 2, 4, 4, 2, 2, 3]]

whitePawnScores = [
    [9, 9, 9, 9, 9, 9, 9, 9],
    [6, 6, 5, 4, 4, 5, 6, 6],
    [5, 4, 4, 4, 4, 4, 4, 5],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [2, 2, 2, 3, 4, 2, 2, 2],
    [2, 2, 1, 2, 2, 1, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 3, 2, 2, 2, 1, 3, 2],
    [2, 2, 4, 3, 3, 2, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [5, 4, 4, 4, 4, 4, 4, 5],
    [6, 6, 5, 4, 4, 5, 6, 6],
    [9, 9, 9, 9, 9, 9, 9, 9]]

bishopScores = [
    [2, 2, 0, 0, 0, 0, 2, 2],
    [2, 4, 3, 1, 1, 3, 4, 2],
    [1, 3, 3, 3, 3, 3, 3, 1],
    [1, 1, 3, 3, 3, 3, 1, 1],
    [1, 1, 3, 3, 3, 3, 1, 1],
    [1, 3, 3, 3, 3, 3, 3, 0],
    [2, 4, 3, 1, 1, 3, 4, 2],
    [2, 2, 0, 0, 0, 0, 2, 2]]

queenScores = [
    [0, 0, 0, 3, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 3, 1, 1],
    [0, 2, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 2, 0, 0],
    [1, 1, 1, 1, 1, 3, 1, 1],
    [0, 0, 0, 3, 0, 0, 0, 0]]


piecePositionScores = {"N": knightScores, "K": kingScores, "B": bishopScores, "wp": whitePawnScores, "R": rookScores, "bp": blackPawnScores, "Q": queenScores}


def findBestMove(gs, validMoves, returnQueue):
    global nextMove, counter
    counter = 0
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    #findGreedyMove(gs, validMoves, DEPTH, gs.whiteToMove)
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
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # Move Ordering - Implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.initMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

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
                if square[1] == "p":
                    piecePositionScore = piecePositionScores[square][row][col]
                else:
                    piecePositionScore = piecePositionScores[square[1]][row][col]
            if square[0] == "w":
                score += pieceScore[square[1]] + piecePositionScore * 0.15
            if square[0] == "b":
                score -= pieceScore[square[1]] + piecePositionScore * 0.15
    return score

def scoreMaterial(board): # Calculate material
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            if square[0] == "b":
                score -= pieceScore[square[1]]
    return score
