import pygame

class PuzzleMenu:
    def __init__(self, screen):
        self.screen = screen

        self.font_title = pygame.font.SysFont("Courier New", 48)
        self.font_option = pygame.font.SysFont("Courier New", 32)

        self.title_text = self.font_title.render("PyPuzzle", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 4))

        self.main_options = ["Start", "Settings", "Exit"]
        self.settings_options = ["Maze Size: 64x64", "Move Delay: 5", "Back"]
        self.selected_index = 0
        self.in_settings = False

        self.option_surfaces = []
        self.option_rects = []

        self.maze_sizes = [(16, 16), (32, 32), (64, 64)]
        self.maze_size_index = 2  
        self.maze_size = self.maze_sizes[self.maze_size_index]

        self.move_delay = 5

    def handle_event(self, event):
        options = self.settings_options if self.in_settings else self.main_options

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(options)
            elif event.key == pygame.K_LEFT and self.in_settings:
                if self.selected_index == 0:
                    self.change_maze_size(-1)
                elif self.selected_index == 1:
                    self.change_move_delay(-1)
            elif event.key == pygame.K_RIGHT and self.in_settings:
                if self.selected_index == 0:
                    self.change_maze_size(1)
                elif self.selected_index == 1:
                    self.change_move_delay(1)
            elif event.key == pygame.K_RETURN:
                if self.in_settings:
                    self.in_settings = False
                    self.selected_index = 0
                else:
                    selected = options[self.selected_index]
                    if selected == "Start":
                        return "start"
                    elif selected == "Settings":
                        self.in_settings = True
                        self.selected_index = 0
                    elif selected == "Exit":
                        return "exit"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = i
                    fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                    return self.handle_event(fake_event)

        return None

    def change_maze_size(self, direction):
        self.maze_size_index = (self.maze_size_index + direction) % len(self.maze_sizes)
        self.maze_size = self.maze_sizes[self.maze_size_index]
        self.settings_options[0] = f"Maze Size: {self.maze_size[0]}x{self.maze_size[1]}"

    def change_move_delay(self, direction):
        self.move_delay = max(1, min(10, self.move_delay + direction))
        self.settings_options[1] = f"Move Delay: {self.move_delay}"

    def draw(self):
        self.screen.blit(self.title_text, self.title_rect)

        self.option_surfaces.clear()
        self.option_rects.clear()

        options = self.settings_options if self.in_settings else self.main_options

        for i, option in enumerate(options):
            color = (255, 255, 255) if i == self.selected_index else (180, 180, 180)
            text_surf = self.font_option.render(option, True, color)
            x = self.screen.get_width() // 2
            y = self.screen.get_height() // 2 + i * 50
            text_rect = text_surf.get_rect(center=(x, y))

            self.screen.blit(text_surf, text_rect)

            self.option_surfaces.append(text_surf)
            self.option_rects.append(text_rect)

    def get_settings(self):
        return self.maze_size, self.move_delay
