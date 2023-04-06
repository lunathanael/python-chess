"""
This is our main driver file, responsible for handling user input and displaying current GameState object.
"""
import pygame as pg
import chessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
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

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
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
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, playerClicks)
        clock.tick(MAX_FPS)
        pg.display.flip()


"""
Responsible for all the graphics within the current game state.
"""
def drawGameState(screen, gs, squaresHighlighted):
    drawBoardSquares(screen)
    # Add in piece highlighting
    drawSquareHighlights(screen, squaresHighlighted, gs.moveLog)
    drawPieces(screen, gs.board)


def drawBoardSquares(screen):
    colors = [pg.Color("white"), pg.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            pg.draw.rect(screen, color, pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawSquareHighlights(screen, squaresHighlighted, moveLog):
    for sq in squaresHighlighted:
        pg.draw.rect(screen, pg.Color("cyan3"), pg.Rect(sq[1] * SQ_SIZE, sq[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if len(moveLog) != 0:
        move = moveLog[-1]
        pg.draw.rect(screen, pg.Color("lightgreen"), pg.Rect(move.startCol * SQ_SIZE, move.startRow * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.draw.rect(screen, pg.Color("lightgreen"), pg.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
