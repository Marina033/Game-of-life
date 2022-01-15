from random import randint
from time import sleep
import pygame
import copy

pygame.init()

# Initialise the screen
xmax = 600 # Width of screen in pixels
ymax = 600 # Height of screen in pixels
screen = pygame.display.set_mode((xmax, ymax), 0, 24) # New 24-bit screen

BLACK = (0, 0, 0)

class Cell:
    def __init__(self, grid, item) -> None:
        self.grid = grid
        self.item = item

    def evolve_cell(self, _x, _y) -> bool:
        x, y = _x, _y
        neighbour_cells = [(x - 1, y - 1), (x - 1, y + 0), (x - 1, y + 1),
                           (x + 0, y - 1),                 (x + 0, y + 1),
                           (x + 1, y - 1), (x + 1, y + 0), (x + 1, y + 1)]
        neighbours = 0
        for x, y in neighbour_cells:
            if x >= 0 and y >= 0:
                try:
                    neighbours += self.grid.get_cell(x, y)
                except:
                    pass
        
        return neighbours == 3 or (neighbours == 2 and self.grid.get_cell(_x, _y))

class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = [[randint(0, 1) for _ in range(y)] for _ in range(x)]

    def empty(self):
        self.grid = [[0 for _ in range(self.y)] for _ in range(self.x)]
    
    def set_cell(self, x, y):
        self.grid[x][y] = 1
    
    def get_cell(self, x, y):
        return self.grid[x][y]
    
    def __len__(self):
        return len(self.grid), len(self.grid[0])
        
class Game:
    def __init__(self) -> None:
        h = 0
        cell_number = 0
        alive_color = pygame.Color(0,0,0)
        alive_color.hsva = [h, 100, 100]
        xlen = xmax // 9
        ylen = ymax // 9
        while True:
            self.grid = Grid(xlen, ylen)
            for _ in range(200):
                for x in range(xlen):
                    for y in range(ylen):
                        alive = self.grid.get_cell(x, y)
                        cell_number += 1
                        cell_color = alive_color if alive else BLACK
                        self.draw_block(x, y, cell_color)
                pygame.display.flip()
                h = (h + 2) % 360
                alive_color.hsva = (h, 100, 100)
                self.evolve()
                cell_number = 0
                sleep(0.1)

    def evolve(self):
        x = len(self.grid.grid)
        y = len(self.grid.grid[0])
        oldgrid = copy.deepcopy(self.grid)
        self.grid.empty()
        for r in range(x):
            for c in range(y):
                cell = Cell(oldgrid, oldgrid.get_cell(r, c))
                if cell.evolve_cell(r, c):
                    self.grid.set_cell(r, c)

    def draw_block(self, x, y, alive_color):
        block_size = 9
        x *= block_size
        y *= block_size
        center_point = ((x + (block_size / 2)), (y + (block_size / 2)))
        pygame.draw.circle(screen, alive_color, center_point, block_size / 2,0)

if __name__ == '__main__':
    game = Game()
