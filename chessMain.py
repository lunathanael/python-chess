"""
This is our main driver file, responsible for handling user input and displaying current GameState object.
"""
import pygame as pg
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import chessEngine
import chessAI as ai
from multiprocessing import Process, Queue


BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 99999
IMAGES = {}


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = pg.image.load("images/" + piece + ".png")

"""
The main drive for our code. This will handle user input and updating the graphics.
"""



def main():
    pg.init()
    screen = pg.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidCapturesFirst()
    moveMade = False # Flag variable for when a move is made, to regenerate valid moves.
    animate = False # Flag variable for when we should animate a move
    moveLogFont = pg.font.SysFont("Arial", 16, False, False)

    loadImages()
    running = True
    gameOver = False
    sqSelected = ()
    playerClicks = []

    AIThinking = False
    moveFinderProcess = False
    moveUndone = False






    playerOne = False # If player 1 is human, this will be True
    playerTwo = False # If player 2 is human, this will be True







    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            # Mouse handler
            elif e.type == pg.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = pg.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8:
                        sqSelected = () # Deselect
                        playerClicks = [] # Clear player Clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2 and humanTurn:
                        move = chessEngine.makeMove(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.initMove(validMoves[i], AIThinking)
                                print(round(ai.scoreBoard(gs), 3))
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                                moveUndone = False
                        if not moveMade:
                            playerClicks = [sqSelected]

            # Key Handler
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_l:
                    printMoveLog(screen, gs)

                if e.key == pg.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = not moveUndone
                    aiGaveup = False

                if e.key == pg.K_r:
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    gameOver = False
                    animate, moveMade = False, False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = not moveUndone

                if e.key == pg.K_p:
                    if not AIThinking and not moveUndone:
                        AIThinking = True
                        print("White", end=" ") if gs.whiteToMove else print("Black", end=" ")
                        print("Thinking:")
                        returnQueue = Queue()
                        if gs.whiteToMove:
                            moveFinderProcess = Process(target=ai.iterativeDeepeningSearch, args=(gs, validMoves, 3, 2, 4, returnQueue))
                        else:
                            moveFinderProcess = Process(target=ai.findBestMove,
                                                        args=(gs, validMoves, gs.whiteToMove, returnQueue))
                        moveFinderProcess.start()

                    if not moveFinderProcess.is_alive():
                        AIMove = returnQueue.get()
                        AIThinking = False
                        gs.initMove(AIMove, AIThinking, True)
                        moveMade = True
                        animate = True

        # AI move finder Logic
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                print("White", end=" ") if gs.whiteToMove else print("Black", end=" ")
                print("Thinking")
                returnQueue = Queue()
                if gs.whiteToMove:
                    moveFinderProcess = Process(target=ai.twoStepSearch, args=(gs, validMoves, 3, 2, 4, returnQueue))
                else:
                    moveFinderProcess = Process(target=ai.findBestMove,
                                                        args=(gs, validMoves, gs.whiteToMove, returnQueue))
                moveFinderProcess.start()

            if not moveFinderProcess.is_alive():
                AIMove = returnQueue.get()
                AIThinking = False
                gs.initMove(AIMove, AIThinking, True)
                moveMade = True
                animate = True

        if moveMade:
            if animate:
                # Animate Move
                animateMove(gs.moveLog[-1], screen, gs.board, clock)

            validMoves = gs.getValidCapturesFirst()
            moveMade = False
            animate = False

        # for move in gs.moveLog:
        # print(move.getChessNotation(), end=", ")

        drawGameState(screen, gs, playerClicks, validMoves, sqSelected, moveLogFont, moveMade)

        if gs.checkMate or gs.staleMate or gs.draw:
            gameOver = True
            if gs.draw:
                drawEndgameText(screen, "Draw!")
            else:
                drawEndgameText(screen, "StaleMate!" if gs.staleMate else "Black wins by Checkmate!" if gs.whiteToMove else "White wins by Checkmate!")
        clock.tick(MAX_FPS)
        pg.display.flip()


"""
Responsible for all the graphics within the current game state.
"""
def drawGameState(screen, gs, squaresHighlighted, validMoves, sqSelected, moveLogFont, moveMade):
    drawBoardSquares(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont, moveMade)


def drawBoardSquares(screen):
    global colors
    colors = [pg.Color("white"), pg.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            pg.draw.rect(screen, color, pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightSquares(screen, gs, validMoves, sqSelected):
    if len(gs.moveLog) != 0:
        move = gs.moveLog[-1]
        pg.draw.rect(screen, pg.Color("darksalmon"), pg.Rect(move.startCol * SQ_SIZE, move.startRow * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.draw.rect(screen, pg.Color("darksalmon"), pg.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if sqSelected != ():
        r, c = sqSelected
        # if gs.board[r][c] == ("w" if gs.whiteToMove else "b"):
        s = pg.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100) # Transparency value: 0 transparent, 255 opaque
        s.fill(pg.Color("yellow2"))
        screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
        # Highlight moves from that square
        s.fill(pg.Color("darkorchid4"))
        for move in validMoves:
            if move.startRow == r and move.startCol == c:
                screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draws the Move Log
def drawMoveLog(screen, gs, font, moveMade):
    moveLogRect = pg.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    pg.draw.rect(screen, pg.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1]) + " "
        moveTexts.append(moveString)
    padding = 5
    movesPerRow = 3
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, pg.Color("white"))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing
    if moveMade:
        print(moveTexts)



def printMoveLog(screen, gs):
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1]) + " "
        moveTexts.append(moveString)

    movesPerRow = 3
    text = ""
    print()
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        print(text)

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol

    framesPerSquare = 5 # Frames per one square move

    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount), (move.startCol + dC * frame / frameCount)
        drawBoardSquares(screen)
        drawPieces(screen, board)
        # Erase piece from ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pg.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pg.draw.rect(screen, color, endSquare)
        # Draw captured piece into rectangle
        if move.pieceCaptured != "--":
            if move.isEnpassantMove:
                enpassantRow = move.endRow + 1 if move.pieceCaptured[0] == "b" else move.endRow - 1
                endSquare = pg.Rect(move.endCol*SQ_SIZE, enpassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # Draw moving piece
        screen.blit(IMAGES[move.pieceMoved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.display.flip()
        clock.tick(144) # Framerate for animation

def drawEndgameText(screen, text):
    font = pg.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, pg.Color("Gray"))
    textLocation = pg.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2, BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pg.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == '__main__':
    main()
