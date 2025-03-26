import pygame
import random

class PuzzleMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 64)
        self.font_option = pygame.font.SysFont(None, 40)

        self.title_color = self.random_color()
        self.option_color = (255, 255, 255)

        self.title_text = self.font_title.render("PyPuzzle", True, self.title_color)
        self.start_text = self.font_option.render("Start", True, self.option_color)
        self.exit_text = self.font_option.render("Exit", True, self.option_color)

        width, height = screen.get_size()
        self.title_rect = self.title_text.get_rect(center=(width // 2, height // 3))
        self.start_rect = self.start_text.get_rect(center=(width // 2, height // 2))
        self.exit_rect = self.exit_text.get_rect(center=(width // 2, height // 2 + 50))

    def random_color(self):
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_rect.collidepoint(event.pos):
                return "start"
            elif self.exit_rect.collidepoint(event.pos):
                return "exit"
        return None

    def draw(self):
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.start_text, self.start_rect)
        self.screen.blit(self.exit_text, self.exit_rect)