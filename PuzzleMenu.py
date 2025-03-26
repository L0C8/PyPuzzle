import pygame

class PuzzleMenu:
    def __init__(self, screen):
        self.screen = screen

        self.font_title = pygame.font.SysFont("Courier New", 48)
        self.font_option = pygame.font.SysFont("Courier New", 32)

        self.title_text = self.font_title.render("PyPuzzle", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))

        self.options = ["Start", "Exit"]
        self.selected_index = 0

        self.option_surfaces = []
        self.option_rects = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_index].lower()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    return self.options[i].lower()

        return None

    def draw(self):
        self.screen.blit(self.title_text, self.title_rect)

        self.option_surfaces.clear()
        self.option_rects.clear()

        for i, option in enumerate(self.options):
            if i == self.selected_index:
                color = (255, 255, 255)  # Selected 
            else:
                color = (180, 180, 180)  # Unselected 

            text_surf = self.font_option.render(option, True, color)
            x = self.screen.get_width() // 2
            y = self.screen.get_height() // 2 + i * 50
            text_rect = text_surf.get_rect(center=(x, y))

            self.screen.blit(text_surf, text_rect)

            self.option_surfaces.append(text_surf)
            self.option_rects.append(text_rect)