import pygame
import random
import time

class PuzzleGame:
    def __init__(self, screen, maze_size, move_delay):
        self.screen = screen
        self.visible_rows = 10
        self.visible_cols = 15
        self.total_rows, self.total_cols = maze_size
        self.move_delay = move_delay / 25.0 # revised so it's faster
        self.grid = [['#' for _ in range(self.total_cols)] for _ in range(self.total_rows)]

        self.paused = False
        self.won = False
        self.player_symbol = '@'
        self.finish_symbol = 'O'
        self.move_direction = None
        self.last_move_time = time.time()

        self.font = pygame.font.SysFont("Courier New", 24)
        self.cell_width = screen.get_width() // self.visible_cols
        self.cell_height = screen.get_height() // self.visible_rows

        self.pause_box = pygame.Rect(90, 60, 300, 200)
        self.resume_rect = None
        self.exit_rect = None
        self.pause_options = ["Resume", "Exit"]
        self.pause_selected_index = 0
        self.pause_option_rects = []

        self.generate_maze()

        self.request_exit_to_menu = False

    def generate_maze(self):
        def neighbors(r, c):
            dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            result = []
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 < nr < self.total_rows and 0 < nc < self.total_cols:
                    result.append((nr, nc))
            random.shuffle(result)
            return result

        start_r = random.randrange(1, self.total_rows, 2)
        start_c = random.randrange(1, self.total_cols, 2)
        self.grid[start_r][start_c] = ' '
        stack = [(start_r, start_c)]

        while stack:
            r, c = stack[-1]
            for nr, nc in neighbors(r, c):
                if self.grid[nr][nc] == '#':
                    wall_r, wall_c = (r + nr) // 2, (c + nc) // 2
                    self.grid[wall_r][wall_c] = ' '
                    self.grid[nr][nc] = ' '
                    stack.append((nr, nc))
                    break
            else:
                stack.pop()

        empty_cells = [(r, c) for r in range(self.total_rows) for c in range(self.total_cols) if self.grid[r][c] == ' ']
        self.player_pos = random.choice(empty_cells)
        self.grid[self.player_pos[0]][self.player_pos[1]] = self.player_symbol
        empty_cells.remove(self.player_pos)
        self.finish_pos = random.choice(empty_cells)
        self.grid[self.finish_pos[0]][self.finish_pos[1]] = self.finish_symbol

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused = not self.paused
            return

        if self.paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pause_selected_index = (self.pause_selected_index - 1) % len(self.pause_options)
                elif event.key == pygame.K_DOWN:
                    self.pause_selected_index = (self.pause_selected_index + 1) % len(self.pause_options)
                elif event.key == pygame.K_RETURN:
                    selected = self.pause_options[self.pause_selected_index]
                    if selected == "Resume":
                        self.paused = False
                    elif selected == "Exit":
                        self.request_exit_to_menu = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.pause_option_rects):
                    if rect.collidepoint(event.pos):
                        if self.pause_options[i] == "Resume":
                            self.paused = False
                        elif self.pause_options[i] == "Exit":
                            self.request_exit_to_menu = True
            return

        if self.won:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.request_exit_to_menu = True
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.move_direction = event.key

        if event.type == pygame.KEYUP:
            if event.key == self.move_direction:
                self.move_direction = None

    def update(self):
        if self.paused or self.won:
            return

        current_time = time.time()
        if self.move_direction and (current_time - self.last_move_time) >= self.move_delay:
            self.last_move_time = current_time
            r, c = self.player_pos
            new_r, new_c = r, c

            if self.move_direction == pygame.K_UP and r > 0:
                new_r -= 1
            elif self.move_direction == pygame.K_DOWN and r < self.total_rows - 1:
                new_r += 1
            elif self.move_direction == pygame.K_LEFT and c > 0:
                new_c -= 1
            elif self.move_direction == pygame.K_RIGHT and c < self.total_cols - 1:
                new_c += 1

            if self.grid[new_r][new_c] != '#':
                if self.grid[new_r][new_c] == self.finish_symbol:
                    self.won = True
                self.grid[r][c] = ' '
                self.player_pos = [new_r, new_c]
                self.grid[new_r][new_c] = self.player_symbol

    def draw(self):
        if self.won:
            self.draw_win_screen()
            return

        r, c = self.player_pos
        row_start = max(0, min(self.total_rows - self.visible_rows, r - 4))
        col_start = max(0, min(self.total_cols - self.visible_cols, c - 7))

        for i in range(self.visible_rows):
            for j in range(self.visible_cols):
                grid_r = row_start + i
                grid_c = col_start + j
                char = self.grid[grid_r][grid_c]
                if char == '#':
                    color = (120, 120, 120)
                elif char == 'O':
                    color = (255, 255, 0)
                else:
                    color = (255, 255, 255)
                text = self.font.render(char, True, color)
                x = j * self.cell_width + 8
                y = i * self.cell_height + 4
                self.screen.blit(text, (x, y))

        if self.paused:
            self.draw_pause_menu()

    def draw_pause_menu(self):
        self.pause_option_rects = []
        bg_box = self.pause_box.inflate(20, 20)
        pygame.draw.rect(self.screen, (30, 30, 30), bg_box)
        pygame.draw.rect(self.screen, (255, 255, 255), self.pause_box, 4)
        inner_box = self.pause_box.inflate(-12, -12)
        pygame.draw.rect(self.screen, (255, 255, 255), inner_box, 2)

        pause_text = self.font.render("Paused", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.pause_box.centerx, self.pause_box.top + 30))
        self.screen.blit(pause_text, pause_rect)

        for i, option in enumerate(self.pause_options):
            color = (255, 255, 255) if i == self.pause_selected_index else (180, 180, 180)
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.pause_box.centerx, self.pause_box.centery + i * 40))
            self.screen.blit(option_text, option_rect)
            self.pause_option_rects.append(option_rect)

        self.resume_rect = self.pause_option_rects[0]
        self.exit_rect = self.pause_option_rects[1]

    def draw_win_screen(self):
        msg = "Level Complete! Press Enter"
        text = self.font.render(msg, True, (255, 255, 0))
        rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, rect)