import pygame, sys  # 声明 导入需要的模块
from pygame.locals import *
from math import pi
import copy


class visualization:
    """
    class visualization, implement a visualizer for TicTacToe game via pygame
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 700))
        pygame.display.set_caption('TicTacToe')

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.box1 = [50, 50, 195, 195]
        self.box2 = [50, 250, 195, 195]
        self.box3 = [50, 450, 195, 195]
        self.box4 = [250, 50, 195, 195]
        self.box5 = [250, 250, 195, 195]
        self.box6 = [250, 450, 195, 195]
        self.box7 = [450, 50, 195, 195]
        self.box8 = [450, 250, 195, 195]
        self.box9 = [450, 450, 195, 195]

        self.boxes = [self.box1, self.box2, self.box3, self.box4, self.box5, self.box6, self.box7, self.box8, self.box9]

        self.screen.fill(self.BLACK)
        for i in range(0, 9):
            pygame.draw.rect(self.screen, self.WHITE, self.boxes[i], 3)
        self.status = 1
        self.number = 0
        self.nine = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def isWin(self, q):
        if self.nine[0][0] == q and self.nine[0][1] == q and self.nine[0][2] == q:
            self.drawWin(q)
        elif self.nine[1][0] == q and self.nine[1][1] == q and self.nine[1][2] == q:
            self.drawWin(q)
        elif self.nine[2][0] == q and self.nine[2][1] == q and self.nine[2][2] == q:
            self.drawWin(q)
        elif self.nine[0][0] == q and self.nine[1][0] == q and self.nine[2][0] == q:
            self.drawWin(q)
        elif self.nine[0][1] == q and self.nine[1][1] == q and self.nine[2][1] == q:
            self.drawWin(q)
        elif self.nine[0][2] == q and self.nine[1][2] == q and self.nine[2][2] == q:
            self.drawWin(q)
        elif self.nine[0][0] == q and self.nine[1][1] == q and self.nine[2][2] == q:
            self.drawWin(q)
        elif self.nine[2][0] == q and self.nine[1][1] == q and self.nine[0][2] == q:
            self.drawWin(q)
        elif self.number == 9:
            self.drawDraw()
        else:
            return False

    def drawWin(self, q):
        if q == 1:
            font = pygame.font.Font('Bank-Gothic-Medium-BT.ttf', 45)
            text = font.render('Circle WIN!!!', True, self.RED)
            self.screen.blit(text, (210, 300))
        elif q == 2:
            font = pygame.font.Font('Bank-Gothic-Medium-BT.ttf', 45)
            text = font.render('X WIN!!!', True, self.RED)
            self.screen.blit(text, (260, 300))

    def drawDraw(self):
        font = pygame.font.Font('Bank-Gothic-Medium-BT.ttf', 40)
        text = font.render('THE GAME HAS DRAWN!', True, self.RED)
        self.screen.blit(text, (85, 300))

    def drawGame(self, grid):
        self.nine = copy.deepcopy(grid)
        for i in range(3):
            for j in range(3):
                if self.nine[i][j] == 1:
                    pygame.draw.arc(self.screen, self.GREEN, [i * 200 + 75, j * 200 + 75, 150, 150], 0, 2 * pi, 5)
                    self.number += 1
                elif self.nine[i][j] == -1:
                    pygame.draw.line(self.screen, self.BLUE, [i * 200 + 75, j * 200 + 75],
                                     [i * 200 + 225, j * 200 + 225], 6)
                    pygame.draw.line(self.screen, self.BLUE, [i * 200 + 225, j * 200 + 75],
                                     [i * 200 + 75, j * 200 + 225], 6)
                    self.number += 1
        if not self.isWin(1):
            self.isWin(2)
        pygame.display.update()

    def waitForClose(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
