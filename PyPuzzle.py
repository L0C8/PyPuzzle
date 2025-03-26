import pygame
import sys
from PuzzleMenu import PuzzleMenu
from PuzzleGame import PuzzleGame

pygame.init()

# ----- Screen settings -----
WIDTH, HEIGHT = 480, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPuzzle")

# ----- Game states -----
MENU = "menu"
GAME = "game"
state = MENU

# ----- Initialize components -----
clock = pygame.time.Clock()
menu = PuzzleMenu(screen)
game = PuzzleGame(screen)

# ----- Main loop -----
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == MENU:
            result = menu.handle_event(event)
            if result == "start":
                state = GAME
            elif result == "exit":
                running = False
        elif state == GAME:
            game.handle_event(event)

    screen.fill((30, 30, 30))
    if state == MENU:
        menu.draw()
    elif state == GAME:
        game.update()
        game.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()