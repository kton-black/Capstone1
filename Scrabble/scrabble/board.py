import pygame
import pathlib
import configparser
import sys

class Scrabble_Board(object):

    def __init__(self, window, board_width=600, board_height=600, window_width=1000, window_height=600):
        pygame.init()
        self.board = []
        self.key = {}
        self.width = 0
        self.length = 0

        self.window = window

        self.load_file()

        # define constants for the board size, window size and grid size
        self.BOARD_SIZE = (board_width, board_height)
        self.WINDOW_SIZE = (window_width, window_height)
        self.GRID_SIZE = 15

        self.flags = pygame.SCALED | pygame.RESIZABLE


    def create_board(self):
        # define colors for the grid and score spaces
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        LIGHT_RED = (255, 200, 200)
        BLUE = (0, 0, 255)
        LIGHT_BLUE = (200, 200, 255)
        YELLOW = (255, 255, 0)

        # create the window and set its title
        # self.window = pygame.display.set_mode(self.WINDOW_SIZE, self.flags)
        pygame.display.set_caption("Scrabble Board")

        self.window.fill((250, 220, 120))

        # draw the grid squares on the window
        square_size = self.BOARD_SIZE[0] // self.GRID_SIZE
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                x = col * square_size
                y = row * square_size
                rect = pygame.Rect(x, y, square_size, square_size)

                # fill the square with white
                pygame.draw.rect(self.window, WHITE, rect)

                # draw light blue squares on double-letter
                if self.board[row][col] == '@':
                    pygame.draw.rect(self.window, LIGHT_BLUE, rect)

                # draw light red squares on double-word
                elif self.board[row][col] == '!':
                    pygame.draw.rect(self.window, LIGHT_RED, rect)

                # draw blue squares on triple-letter
                elif self.board[row][col] == '^':
                    pygame.draw.rect(self.window, BLUE, rect)

                # draw red squares on triple-word
                elif self.board[row][col] == '$':
                    pygame.draw.rect(self.window, RED, rect)

                elif self.board[row][col] == '*':
                    pygame.draw.rect(self.window, YELLOW, rect)

                pygame.draw.rect(self.window, BLACK, rect, width=1)

    def display(self, main_window):
        main_window.blit(pygame.transform.scale(self.window, main_window.get_size()), (0,0))


    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def load_file(self, file= pathlib.Path(__file__).parent.absolute() / 'board.ini'):
        parser = configparser.ConfigParser()
        parser.read(file)
        #self.tileset = parser.get("board","image")
        print(parser['board'])
        self.board = parser.get("board","start").split("\n")
        # print(parser.sections())
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                # print(desc)
                self.key[section] = desc
        self.width = len(self.board[0])
        self.height = len(self.board)
        # print(self.key)
        # print(self.width)
        # print(self.height)

    def get_tile(self, x, y):
        try:
            char = self.board[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

class Tile(object):
    def __init__(self):
        pass
