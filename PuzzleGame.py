import pygame

class PuzzleGame:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.text = self.font.render("testing!", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    def handle_event(self, event):
        pass  

    def update(self):
        pass  
    def draw(self):
        self.screen.blit(self.text, self.text_rect)