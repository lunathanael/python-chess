"""
This is our main driver file, responsible for handling user input and displaying current GameState object.
"""
import pygame as pg
import chessEngine
import chessAI as ai

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 9999
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
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # Flag variable for when a move is made, to regenerate valid moves.
    animate = False # Flag variable for when we should animate a move

    loadImages()
    running = True
    gameOver = False
    sqSelected = ()
    playerClicks = []

    playerOne = False # If player 1 is human, this will be True
    playerTwo = False # If player 2 is human, this will be True

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            # Mouse handler
            elif e.type == pg.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = pg.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = chessEngine.makeMove(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.initMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            # Key Handler
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == pg.K_r:
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    gameOver = False
                    animate, moveMade = False, False

        # AI move finder Logic
        if not gameOver and not humanTurn:
            AImove = ai.findRandomMove(validMoves)
            gs.initMove(AImove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                # Animate Move
                animateMove(gs.moveLog[-1], screen, gs.board, clock)

            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        # for move in gs.moveLog:
        # print(move.getChessNotation(), end=", ")

        drawGameState(screen, gs, playerClicks, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by Checkmate!")
            else:
                drawText(screen, "White wins by Checkmate!")
        elif gs.staleMate:
            drawText(screen, "StaleMate!")

        clock.tick(MAX_FPS)
        pg.display.flip()


"""
Responsible for all the graphics within the current game state.
"""
def drawGameState(screen, gs, squaresHighlighted, validMoves, sqSelected):
    drawBoardSquares(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


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
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # Draw moving piece
        screen.blit(IMAGES[move.pieceMoved], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.display.flip()
        clock.tick(144) # Framerate for animation

def drawText(screen, text):
    font = pg.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, pg.Color("Gray"))
    textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pg.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == '__main__':
    main()
