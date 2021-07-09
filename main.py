import pygame
from typing import List, Optional


class Playground:
    def __init__(self) -> None:
        self.board: Optional[List[List[int]]] = [[None for _ in range(9)] for _ in range(9)]

    def checkRowCol(self, row: int, col: int, num: int) -> bool:
        for i in range(9):
            if self.board[i][col] == num or self.board[row][i] == num:
                return False
        return True

    def checkBox(self, row: int, col: int, num: int) -> bool:
        for i in range(3):
            for j in range(3):
                if self.board[row - row % 3 + i][col - col % 3 + j] == num:
                    return False
        return True

    def isEnd(self) -> bool:
        for row in range(9):
            for col in range(9):
                if self.board[row][col] is None:
                    return False
        return True

    def insert(self, row: int, col: int, num: int) -> bool:
        if self.checkRowCol(row, col, num) and self.checkBox(row, col, num):
            self.board[row][col] = num
            return True
        return True


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (30,144,255)
GREY = (169,169,169)


MARGIN = 10
WIDTH = 50
HEIGHT = 50


class Options:
    def __init__(self) -> None:
        self.pos = None
        self.done = False
        self.screen = None
        self.clock = None
        self.reset = False
        self.home_screen = True
        self.game_screen = False
        self.end_screen = False
        self.mouse_pos = (0, 0)
        self.screen_size = [450, 550]
        self.margin = 10
        self.width = 40
        self.height = 40
        self.avaibles = [-1 for _ in range(9)]


def init_pygame(options: Options) -> None:
    pygame.init()
    options.screen = pygame.display.set_mode(options.screen_size)
    pygame.display.set_caption("Sudoku")
    options.clock = pygame.time.Clock()
    return None


def draw_empty(column, row, options, color):
    pygame.draw.rect(options.screen, color, [WIDTH * column, HEIGHT * row, WIDTH, HEIGHT])
    return None


def drawNumber(column, row, options, number):
    font = pygame.font.SysFont('arial', 40)
    text = font.render(str(number), True, BLACK)
    options.screen.blit(text, (WIDTH * column + WIDTH // 2 - 8, HEIGHT * row + 3))


def draw_playground(playground: Playground, options: Options):
    for row in range(11):
        for column in range(9):
            
            if row < 9:
                draw_empty(column, row, options, WHITE)
                if playground.board[row][column] != None:
                    drawNumber(column, row, options, playground.board[row][column])
            if row == 9:
                if options.pos is not None and options.avaibles[column] == 0:
                    draw_empty(column, row, options, RED)
                else:
                    draw_empty(column, row, options, GREY)
                drawNumber(column, row, options, column + 1)
    
    color = WHITE
    if options.mouse_pos == 10:
        color = RED
    
    pygame.draw.rect(options.screen, color, [0, HEIGHT * 10, 450, HEIGHT])
    font = pygame.font.SysFont('arial', 40)
    text = font.render("SOLVE", True, BLACK)
    options.screen.blit(text, (WIDTH * 3 + WIDTH // 2, HEIGHT * 10 + 3))
    
    for i in range(10):
        w = 8 if i % 3 == 0 else 3
        pygame.draw.line(options.screen, BLACK, (0, 50 * i), (450, 50 * i), width = w)
        pygame.draw.line(options.screen, BLACK, (50 * i, 0), (50 * i, 450), width = w)
        pygame.draw.line(options.screen, BLACK, (50 * i, 450), (50 * i, 500), width=6)


    pygame.draw.line(options.screen, BLACK, (0, 500), (450, 500), width=8)

    return None


def end(plg: Playground):
    for i in range(9):
        for j in range(9):
            if plg.board[i][j] is None:
                return (i, j)
    return None            


def back_solve(plg: Playground):
    ok = True
    for i in range(9):
        for j in range(9):
            if plg.board[i][j] is None:
                ok = False
                break
    if ok:
        return True
    pos = end(plg)

    if pos is not None:
        for x in range(1, 10):
            if plg.checkBox(pos[0], pos[1], x) and plg.checkRowCol(pos[0], pos[1], x):
                
                plg.board[pos[0]][pos[1]] = x

                if back_solve(plg):
                    return True
                plg.board[pos[0]][pos[1]] = None
    return False
    

def avaibles(plg: Playground, row: int, col: int) -> List[int]:
    result = [0 for _ in range(9)]

    for i in range(9):
        if plg.board[i][col] != None:
            result[plg.board[i][col] - 1] = -1
        if plg.board[row][i] != None:
            result[plg.board[row][i] - 1] = -1
    for i in range(3):
        for j in range(3):
            if plg.board[row - row % 3 + i][col - col % 3 + j] != None:
                result[plg.board[row - row % 3 + i][col - col % 3 + j] - 1] = -1
    return result


def mainLoop():
    options = Options()
    init_pygame(options)
    plg = Playground()

    solve_button = False
    while True:
        for event in pygame.event.get(): 
            mas = pygame.mouse.get_pos()
            options.mouse_pos = mas[1] // WIDTH
            if event.type == pygame.QUIT:  
                pygame.quit
                return None  
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                row = pos[1] // HEIGHT
                col = pos[0] // WIDTH
                if row < 9 and col < 9 and not solve_button:
                    if plg.board[row][col] != None:
                        plg.board[row][col] = None
                    else:
                        options.avaibles = avaibles(plg, row, col)
                        print(options.avaibles)
                        options.pos = (row, col)
                        
                elif row == 9 and not solve_button:
                    if options.pos is not None:
                
                        print(col + 1)
                        print(plg.insert(options.pos[0], options.pos[1], col + 1))
                        options.pos = None
                elif row == 10:
                    solve_button = not solve_button

        if solve_button:
            back_solve(plg)
            solve_button = not solve_button
        draw_playground(plg, options)
        options.clock.tick(60)
        pygame.display.flip()
    
    pygame.quit()
    return None

if __name__ == "__main__":
    mainLoop()
    