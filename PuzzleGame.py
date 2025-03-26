import pygame

class PuzzleGame:
    def __init__(self, screen):
        self.screen = screen
        self.rows = 10
        self.cols = 15
        self.grid = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        
        self.player_symbol = '@'
        self.player_pos = [1, 1]

        self.font = pygame.font.SysFont("Courier New", 24)
        self.cell_width = screen.get_width() // self.cols
        self.cell_height = screen.get_height() // self.rows

        self.place_player()

    def place_player(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == self.player_symbol:
                    self.grid[row][col] = ' '

        r, c = self.player_pos
        self.grid[r][c] = self.player_symbol

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            r, c = self.player_pos
            if event.key == pygame.K_UP and r > 0:
                self.player_pos[0] -= 1
            elif event.key == pygame.K_DOWN and r < self.rows - 1:
                self.player_pos[0] += 1
            elif event.key == pygame.K_LEFT and c > 0:
                self.player_pos[1] -= 1
            elif event.key == pygame.K_RIGHT and c < self.cols - 1:
                self.player_pos[1] += 1
            self.place_player()

    def update(self):
        pass  
    
    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                char = self.grid[row][col]
                text = self.font.render(char, True, (255, 255, 255))
                x = col * self.cell_width + 8
                y = row * self.cell_height + 4
                self.screen.blit(text, (x, y))