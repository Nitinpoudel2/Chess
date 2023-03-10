"""
This is our main driver which will be responsible for
handling user input and displaying the current gamestate object
"""

import pygame as p
from Chess import ChessEngine
from Chess.ChessEngine import GameState




WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}
""" Initialize a global dictionary of images. This will be called exactly once in the middle
"""


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE, SQ_SIZE))



def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made
    loadImages()  # only do it once before the while loop is executed
    running = True
    sqSelected = ()# not selected, keep the track of the last click of the user (tuple:(row.col))
    playerClicks = []# keeping the track of player clicks two tuples: [(6,4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # x,y location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col):
                    sqSelected = () # deselect the value and return the value
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) # append both  1st and 2nd clicks
                if len(playerClicks) == 2: # after the second click in the game
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected =  ()
                    playerClicks = []
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True #

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
"""
Reponsible for all the graphics within a current game state
"""
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)
"""Draws the squares on the board"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
def drawBoard(screen):
    """Draws the pieces on the board using the current gamestate.board"""
    colors = [p.Color("white"), p.Color(" gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
if __name__ == "__main__":

    main()
