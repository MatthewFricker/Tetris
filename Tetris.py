import pygame
import random
from collections import deque

class Tetris:
    def __init__(self, height=20, width=10):
        pygame.init()
        self.load_images()
        self.game_font = pygame.font.SysFont("Arial", 24)

        self.height = height
        self.width = width
        self.scale = self.images[0].get_width()
        self.window_height = self.scale * self.height
        self.window_width = self.scale * self.width + 600

        self.grid = [[0]*self.width for _ in range(self.height)]
        self.pieces = {"o": [(0,4), (0,5), (1,4), (1,5)], 
                       "z": [(0,4), (0,5), (1,5), (1,6)], 
                       "s": [(0,6), (0,5), (1,4), (1,5)], 
                       "t": [(1,4), (1,5), (1,6), (0,5)], 
                       "i": [(0,3), (0,4), (0,5), (0,6)], 
                       "l": [(0,6), (1,5), (1,4), (1,6)], 
                       "j": [(1,4), (1,5), (1,6), (0,4)]
                       }
        self.line_scores = {1: 40, 2: 100, 3: 300, 4: 1200}
        self.window = pygame.display.set_mode((self.window_width, self.window_height+self.scale))
        self.clock = pygame.time.Clock()

        self.speed = 10
        self.score = 0

        self.game_over = False
        self.main_loop()


    def load_images(self):
        self.images = []
        for name in ["emptysquare", "block", "greyblock"]:
            self.images.append(pygame.image.load(name + ".png"))
        
    
    def main_loop(self):
        self.piece_queue = deque()
        self.piece_name, self.piece = self.get_new_piece()
        i = 0
        pygame.mixer.music.load("Tetris_theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        while not self.game_over:
            self.check_events()
            self.draw_window()
            self.clock.tick(30)
            i += 1

            if i % (30 - self.speed) == 0:
                for y, x in self.piece:
                    if y == 19 or self.grid[y+1][x] == 2:
                        self.freeze_block(self.piece)
                        self.check_rows()
                        self.piece_name, self.piece = self.get_new_piece()
                        break
                self.move_piece(1,0)
                
            
    def check_rows(self):
        lines_cleared = 0
        for i, row in enumerate(self.grid):
            contains_zeroes = False
            for square in row:
                if square == 0 or square == 1:
                    contains_zeroes = True
            if not contains_zeroes:
                lines_cleared += 1
                self.grid.pop(i)
                self.grid.insert(0, [0]*self.width)
        if lines_cleared:
            self.score += self.line_scores[lines_cleared]



    def get_new_piece(self):
        if len(self.piece_queue) <= 1:
            self.piece_queue.extend(deque(self.pieces.keys()))
            random.shuffle(self.piece_queue)
        self.piece_name = self.piece_queue.popleft()
        self.piece = self.pieces[self.piece_name]
        for y,x in self.piece:
            if self.grid[y][x] == 0:
                self.grid[y][x] = 1
            else:
                self.game_over = True
        return self.piece_name, self.piece
    
    def freeze_block(self, piece):
        for y, x in piece:
            self.grid[y][x] = 2
    

    def move_piece(self, y_dir, x_dir):
        new_piece = [(y+y_dir,x+x_dir) for y, x in self.piece]
        if self.speed == 28:
            self.score += 1
        for y, x in new_piece:
            if x >= self.width or x < 0 or y >= self.height or self.grid[y][x] == 2:
                return
        for y, x in self.piece:
            self.grid[y][x] = 0
        for y, x in new_piece:
            self.grid[y][x] = 1
        self.piece = new_piece

    def rotate(self):
        if self.piece_name == "o":
            return
        pivot_y, pivot_x = self.piece[1]
        new_piece = []
        for y, x in self.piece:
            new_piece.append((pivot_x + pivot_y - x, y + pivot_x - pivot_y))
        for y, x in new_piece:
            if y >= self.height or y < 0 or x < 0 or x >= self.width or self.grid[y][x] == 2:
                return
        for y, x in self.piece:
            self.grid[y][x] = 0
        for y, x in new_piece:
            self.grid[y][x] = 1
        self.piece = new_piece
            

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_piece(0,-1)
                if event.key == pygame.K_RIGHT:
                    self.move_piece(0,1)
                if event.key == pygame.K_DOWN:
                    self.speed = 28
                if event.key == pygame.K_UP:
                    self.rotate()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.speed = 10

    def draw_window(self):
        self.window.fill((0, 0, 0))
        for y in range(self.height):
            for x in range(self.width):
                square = self.grid[y][x]
                self.window.blit(self.images[square], (x * self.scale, y * self.scale))
        score_text = self.game_font.render("Score: " + str(self.score), True, (255, 255, 255))
        for y in range(5):
            for x in range(5):
                self.window.blit(self.images[0], (self.width*self.scale + x*self.scale + 300, y*self.scale))
        for y, x in self.pieces[self.piece_queue[0]]:
            self.window.blit(self.images[1], (self.width*self.scale + (x-3)*self.scale + 300, (y+1)*self.scale))
        self.window.blit(score_text, (self.width*self.scale + 100, 20))
        pygame.display.flip()
            
if __name__ == "__main__":
    tetris = Tetris()