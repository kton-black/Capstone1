import pygame
import pathlib
import configparser
import sys
import random

# define colors for the grid and score spaces
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (200, 200, 255)
YELLOW = (255, 255, 0)

class Scrabble_Board(pygame.sprite.Sprite):

    def __init__(self, board_width=600, board_height=600):
        pygame.init()

        #set board and masks
        self.board = []
        self.played_tiles = []
        self.tiles_in_play = []

        #reference for letter, points, multipliers, count, etc.
        self.board_key = {}
        self.tiles_key = {}

        #use if we want to vary board size (not necessary for base game)
        self.width = 0
        self.length = 0

        #determine active player and their scores
        self.turn = 0
        self.p1_score = 0
        self.p2_score = 0
        self.score = 0

        #defines selected tile to set position on board
        self.selected = None

        #define constants for the board size, window size and grid size
        self.BOARD_SIZE = (board_width, board_height)
        self.GRID_SIZE = 15
        self.TILE_SIZE = (self.BOARD_SIZE[0] // self.GRID_SIZE, self.BOARD_SIZE[1] // self.GRID_SIZE)
        self.HAND_SIZE = 7

        #use for drawing and removing tiles from the scene
        self.all_tiles = pygame.sprite.Group()
        self.purse = pygame.sprite.Group()
        self.player1 = pygame.sprite.Group()
        self.player2 = pygame.sprite.Group()
        self.on_board = pygame.sprite.Group()
        self.in_play = pygame.sprite.Group()

        #generate initial data from ini files
        self.load_board()
        self.load_tiles()
        self.load_masks()

        #generate starting hand
        self.update()

    def update(self):
        player = None
        if self.turn == 0:
            player = self.player1
        else:
            player = self.player2

        while len(player) < 7:
            count = len(self.purse.sprites())
            if count > 0:
                i = random.randint(0, count)
                select = self.purse.sprites()[i]
                player.add(select)
                select.remove(self.purse)
        # print(self.player1)
        # print(self.player2)
        # print(self.purse)

    def draw_board(self, screen):
        # create the window and set its title
        # self.window = pygame.display.set_mode(self.WINDOW_SIZE, self.flags)
        pygame.display.set_caption("Scrabble")

        screen.fill((250, 220, 120))

        # draw the grid squares on the window
        square_size = self.BOARD_SIZE[0] // self.GRID_SIZE
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                x = col * square_size
                y = row * square_size
                rect = pygame.Rect(x, y, square_size, square_size)

                color = (0,0,0)

                if self.board_key[self.board[row][col]]['color'] == "WHITE":
                    color = WHITE
                elif self.board_key[self.board[row][col]]['color'] == "LIGHT_BLUE":
                    color = LIGHT_BLUE
                elif self.board_key[self.board[row][col]]['color'] == "LIGHT_RED":
                    color = LIGHT_RED
                elif self.board_key[self.board[row][col]]['color'] == "BLUE":
                    color = BLUE
                elif self.board_key[self.board[row][col]]['color'] == "RED":
                    color = RED
                elif self.board_key[self.board[row][col]]['color'] == "YELLOW":
                    color = YELLOW

                # fill the square with their color
                # print(self.board[row][col])
                pygame.draw.rect(screen, color, rect)

    def draw_grid(self, screen):
        #draws the black lines of the board to make it appear appealing

        square_size = self.BOARD_SIZE[0] // self.GRID_SIZE
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                x = col * square_size
                y = row * square_size
                rect = pygame.Rect(x, y, square_size, square_size)
                pygame.draw.rect(screen, BLACK, rect, width=1)


    def draw_hand(self, screen):
        #draws the current player's tiles in their hand

        sidebar_width = (screen.get_size()[0] - self.BOARD_SIZE[0]) / 2
        # print(sidebar_width)
        hand_width = self.HAND_SIZE * self.TILE_SIZE[0]
        # print(hand_width)
        start_pos = sidebar_width + self.BOARD_SIZE[0] - (hand_width / 2)
        # print(start_pos)
        height = self.BOARD_SIZE[1] - 100
        tiles = None
        if self.turn == 0:
            tiles = self.player1
        else:
            tiles = self.player2

        #Makes tile Tray
        rect = pygame.Rect(start_pos, height , self.TILE_SIZE[0] * self.HAND_SIZE, self.TILE_SIZE[1])
        pygame.draw.rect(screen, (240, 180, 60), rect)

        for i, tile in enumerate(tiles):
            if not tile.in_play:
                tile.update(start_pos + (i * self.TILE_SIZE[0]), height)
        tiles.draw(screen)

    def draw_active_tiles(self, screen):
        #draws all tiles that are actively in play or being played

        self.in_play.draw(screen)
        self.on_board.draw(screen)

    def render(self, screen):
        #calls all functions to redraw scene (used for loop)

        self.draw_board(screen)
        self.draw_active_tiles(screen)
        self.draw_grid(screen)
        self.draw_hand(screen)

        if self.selected:
            # print("Draw Selected", self.selected.rect)
            pygame.draw.rect(screen, (0,255,0), self.selected.rect, width=1)

    def load_board(self):
        #loads board data from 'board.ini' file

        parser = configparser.ConfigParser()
        parser.read(pathlib.Path(__file__).parent.absolute() / 'board.ini')
        # print(parser['board'])
        self.board = parser.get("board","start").split("\n")
        print(self.board)
        # print(parser.sections())
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                # print(desc)
                self.board_key[section] = desc
        self.width = len(self.board[0])
        self.height = len(self.board)
        # print(self.board_key)

    def load_tiles(self):
        #loads all tile data from 'tiles.ini' file

        parser = configparser.ConfigParser()
        parser.read(pathlib.Path(__file__).parent.absolute() / 'tiles.ini')
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                # print(desc)
                self.tiles_key[section] = desc
        # print(self.tiles_key)
        for letter in self.tiles_key:
            # print(letter)
            # print(self.tiles_key[letter]['count'])

            # print(letter['count'])
            for num in range(0,int(self.tiles_key[letter]['count'])):
                # print(num)
                tile = Tile(letter, self.TILE_SIZE[0], self.TILE_SIZE[1])
                self.all_tiles.add(tile)
                self.purse.add(tile)

        # print(self.all_tiles.sprites())
        # print(self.all_tiles.get_sprite(3).letter)
        # print(self.all_tiles)

    def load_masks(self):
        #generates masks to manipulate for word verification

        empty_row = "..............."
        for row in range(15):
            self.played_tiles.append(empty_row)
            self.tiles_in_play.append(empty_row)

    def get_tile(self, x, y):
        #finds the tile that was selected and returns it

        # char = self.board[y][x]
        tiles = None
        if self.turn == 0:
            tiles = self.player1
        else:
            tiles = self.player2

        for tile in tiles:
            if tile.rect.collidepoint((x, y)):
                return tile
        return None

        # test = Tile('A',self.BOARD_SIZE[0]/self.width - 10, self.BOARD_SIZE[1]/self.height - 10)

    def select_tile(self, x, y):
        #generates selection/deselection/movement of a tile

        if self.selected == None:
            self.selected = self.get_tile(x, y)
        else:
            if self.selected.in_play:
                self.tiles_in_play[self.selected.col] = self.tiles_in_play[self.selected.col][:self.selected.row] + '.' + self.tiles_in_play[self.selected.col][self.selected.row + 1:]
                self.selected.remove(self.in_play)
                self.selected.in_play = False
            if 0 <= x <= self.BOARD_SIZE[0] and 0 <= y <= self.BOARD_SIZE[1]:
                col, row = self.selected.get_board_position(x, y)
                if self.tiles_in_play[col][row] == '.' and self.played_tiles[col][row] == '.':
                    self.selected.update(x,y)
                    self.selected.in_play = True
                    self.in_play.add(self.selected)
                    self.tiles_in_play[col] = self.tiles_in_play[col][:row] + self.selected.letter + self.tiles_in_play[col][row + 1:]

            self.selected = None

    def next_turn(self):
        #updates scores and removes tiles from hands of player

        if self.turn == 0:
            self.p1_score += self.score


        else:
            self.p2_score += self.score

        self.score = 0

        for tile in self.in_play:
            tile.add(self.on_board)
            if self.turn == 0:
                tile.remove(self.player1)
            else:
                tile.remove(self.player2)
            tile.remove(self.in_play)
            self.played_tiles[tile.col] = self.played_tiles[tile.col][:tile.row] + tile.letter + self.played_tiles[tile.col][tile.row + 1:]
            self.tiles_in_play[tile.col] = self.tiles_in_play[tile.col][:tile.row] + '.' + self.tiles_in_play[tile.col][tile.row + 1:]

        self.turn ^= 1

        pass

    def reset_active(self):
        for tile in self.in_play:
            self.tiles_in_play[tile.col] = self.tiles_in_play[tile.col][:tile.row] + '.' + self.tiles_in_play[tile.col][tile.row + 1:]
            tile.remove(self.in_play)
            tile.in_play = False

    def get_word_score(self):
        pass

    # def move_tile(self, tile, turn = self.turn):


class Tile(pygame.sprite.Sprite):
    def __init__(self, letter, width, height):
        pygame.sprite.Sprite.__init__(self)

        #holds tile pixel size
        self.width = width
        self.height = height

        #holds character value
        self.letter = letter

        #used to know when and where tiles should be shown
        self.in_play = False
        self.visible = False

        #identify location of tile on board (-1 means its not on the board)
        self.col = -1
        self.row = -1

        #generates tile image to draw
        self.font = pygame.font.SysFont(None, 30)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.text = self.font.render(letter, True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.image.fill((253,253,208))
        self.image.blit(self.text, self.text_rect)

    def update(self, x, y, visible = True):
        #changes tile position and visibility

        col, row = self.get_board_position(x, y)

        if 0 <= col <= 15 and 0 <= row <= 15:
            self.rect.topleft = self.get_slot_position(col, row)
            self.col, self.row = col, row
        else:
            self.col, self.row = -1, -1
            self.rect.topleft = x, y

        self.visible = visible

    def get_board_position(self, x, y):
        #finds the col & row of the board

        col = x // self.width
        row = y // self.height
        return col, row

    def get_slot_position(self, col, row):
        #finds the topleft spot of each tile slot (used for alignment)

        x = self.width * col
        y = self.height * row
        return x, y

# class TileGroup(pygame.sprite.Group):
#     def __init__(self):
#         pygame.sprite.Group.__init__(self)




