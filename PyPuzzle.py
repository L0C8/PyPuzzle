import pygame
import sys
import random

# ----- Screen Size ----- 
WIDTH, HEIGHT = 480, 320

# ----- Initialize PyGame ----- 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPuzzle")

# ----- Assets setup ----- 
# we'll add stuff later

# ----- Font setup ----- 
font_title = pygame.font.SysFont(None, 64)
font_option = pygame.font.SysFont(None, 40)

# ----- Text setup -----
def random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

title_color = random_color()
option_color = (255, 255, 255)

title_text = font_title.render("PyPuzzle", True, title_color)
start_text = font_option.render("Start", True, option_color)
exit_text = font_option.render("Exit", True, option_color)

title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# -- Clock
clock = pygame.time.Clock()

# ---------- Main loop ----------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                print("Start game!")
            elif exit_rect.collidepoint(event.pos):
                running = False

    screen.fill((30, 30, 30))
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(exit_text, exit_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()