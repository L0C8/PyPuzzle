import pygame
import random

class PuzzleGame:
    def __init__(self, screen):
        self.screen = screen
        self.rows = 10
        self.cols = 15
        self.grid = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

        # Game state
        self.paused = False

        # Player
        self.player_symbol = '@'
        self.player_pos = [1, 1]

        # Block
        self.block_symbol = '#'
        self.place_random_block()

        # Fonts
        self.font = pygame.font.SysFont("Courier New", 24)
        self.cell_width = screen.get_width() // self.cols
        self.cell_height = screen.get_height() // self.rows

        # Pause UI
        self.pause_box = pygame.Rect(90, 60, 300, 200)
        self.resume_rect = None
        self.exit_rect = None

        self.place_player()

        # Menu communication
        self.request_exit_to_menu = False

    def place_random_block(self):
        while True:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if [r, c] != self.player_pos:
                self.grid[r][c] = self.block_symbol
                break

    def place_player(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == self.player_symbol:
                    self.grid[row][col] = ' '

        r, c = self.player_pos
        self.grid[r][c] = self.player_symbol

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused = not self.paused
            return

        if self.paused:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.resume_rect and self.resume_rect.collidepoint(event.pos):
                    self.paused = False
                elif self.exit_rect and self.exit_rect.collidepoint(event.pos):
                    self.request_exit_to_menu = True
            return

        # Normal movement (not paused)
        if event.type == pygame.KEYDOWN:
            r, c = self.player_pos
            new_r, new_c = r, c

            if event.key == pygame.K_UP and r > 0:
                new_r -= 1
            elif event.key == pygame.K_DOWN and r < self.rows - 1:
                new_r += 1
            elif event.key == pygame.K_LEFT and c > 0:
                new_c -= 1
            elif event.key == pygame.K_RIGHT and c < self.cols - 1:
                new_c += 1

            if self.grid[new_r][new_c] != self.block_symbol:
                self.player_pos = [new_r, new_c]
                self.place_player()

    def update(self):
        pass  # For future logic

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                char = self.grid[row][col]
                text = self.font.render(char, True, (255, 255, 255))
                x = col * self.cell_width + 8
                y = row * self.cell_height + 4
                self.screen.blit(text, (x, y))

        if self.paused:
            self.draw_pause_menu()

    def draw_pause_menu(self):

        # Background panel for pause menu
        bg_box = self.pause_box.inflate(20, 20)
        pygame.draw.rect(self.screen, (30, 30, 30), bg_box)

        # Outer and inner box 
        pygame.draw.rect(self.screen, (255, 255, 255), self.pause_box, 4)
        inner_box = self.pause_box.inflate(-12, -12)
        pygame.draw.rect(self.screen, (255, 255, 255), inner_box, 2)

        # Paused title
        pause_text = self.font.render("Paused", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.pause_box.centerx, self.pause_box.top + 30))
        self.screen.blit(pause_text, pause_rect)

        # Resume button
        resume_text = self.font.render("Resume", True, (255, 255, 255))
        self.resume_rect = resume_text.get_rect(center=(self.pause_box.centerx, self.pause_box.centery))
        self.screen.blit(resume_text, self.resume_rect)

        # Exit button
        exit_text = self.font.render("Exit", True, (255, 255, 255))
        self.exit_rect = exit_text.get_rect(center=(self.pause_box.centerx, self.pause_box.centery + 40))
        self.screen.blit(exit_text, self.exit_rect)