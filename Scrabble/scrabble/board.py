import pygame
import pathlib
import configparser
import sys
import random
import time

# define colors for the grid and score spaces
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (200, 200, 255)
YELLOW = (255, 255, 0)

class Scrabble_Board(pygame.sprite.Sprite):

    def __init__(self, board_width=600, board_height=600, vsComputer= False, timer=60):
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
        self.p1_display = None
        self.p2_score = 0
        self.p2_display = None
        self.score = 0

        #defines selected object(s)
        self.selected = None
        self.selection = pygame.sprite.Group()

        #defines button flags
        self.vsComputer = vsComputer
        self.switching = False
        self.redraw = False
        self.blank = None
        self.pause = False
        self.end = False
        self.time = timer

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

        #use for drawing interface
        self.buttons = pygame.sprite.Group()
        self.misc = pygame.sprite.Group()
        self.all_buttons = pygame.sprite.Group()

        #generate initial data from ini files
        self.load_board()
        self.load_tiles()
        self.load_masks()
        self.load_interface()

        #generate starting hand
        self.update()

    def update(self):

        if not self.pause:
            player = None
            if self.turn == 0:
                player = self.player1
            else:
                player = self.player2

            while len(player) < 7:
                count = len(self.purse.sprites())
                if count > 0:
                    i = random.randint(0, count - 1)
                    select = self.purse.sprites()[i]
                    player.add(select)
                    select.remove(self.purse)
            # print(self.player1)
            # print(self.player2)
            # print(self.purse)
        # self.time = self.time - ((time.time() - self.start_time)/1000)
        # self.timer.update_text(str(self.time))

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

        if not (self.vsComputer and self.turn == 1) or self.switching:
            # print("Printing: ", self.turn, self.vsComputer)
            for i, tile in enumerate(tiles):
                if not tile.in_play:
                    tile.update(start_pos + (i * self.TILE_SIZE[0]), height)
            tiles.draw(screen)

    def draw_active_tiles(self, screen):
        #draws all tiles that are actively in play or being played

        self.in_play.draw(screen)
        self.on_board.draw(screen)

    def draw_interface(self, screen):
        #draws all active interface text and buttons


        self.buttons.draw(screen)
        self.misc.draw(screen)

    def render(self, screen):
        #calls all functions to redraw scene (used for loop)

        self.draw_board(screen)
        self.draw_active_tiles(screen)
        self.draw_grid(screen)
        self.draw_hand(screen)
        self.draw_interface(screen)

        if not self.pause:
            if isinstance(self.selected, Tile):
                # print("Draw Selected", self.selected.rect)
                pygame.draw.rect(screen, (0,255,0), self.selected.rect, width=1)

            if len(self.selection.sprites()) > 0:
                # print("Drawing Redraw Selection")
                for tile in self.selection.sprites():
                    pygame.draw.rect(screen, (0,255,0), tile.rect, width=1)

    def load_board(self):
        #loads board data from 'board.ini' file

        parser = configparser.ConfigParser()
        parser.read(pathlib.Path(__file__).parent.absolute() / 'board.ini')
        # print(parser['board'])
        self.board = parser.get("board","start").split("\n")
        # print(self.board)
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
                tile = Tile(letter, self.TILE_SIZE[0], self.TILE_SIZE[1], score = self.tiles_key[letter]['points'])
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

    def load_interface(self):
        #generate buttons

        #player scores
        p1 = Button(100, self.TILE_SIZE[1], self.BOARD_SIZE[0] + 50, self.TILE_SIZE[0] * 1, "P1 Score:", color= (250, 220, 120))
        p2 = Button(100, self.TILE_SIZE[1], self.BOARD_SIZE[0] + 50, self.TILE_SIZE[0] * 3, "P2 Score:", color= (250, 220, 120))
        self.p1_display = Button(200, self.TILE_SIZE[1], self.BOARD_SIZE[0] + 150, self.TILE_SIZE[0] * 1, str(self.p1_score))
        self.p2_display = Button(200, self.TILE_SIZE[1], self.BOARD_SIZE[0] + 150, self.TILE_SIZE[0] * 3, str(self.p2_score))

        #player redraw buttons
        redraw = Button(300, self.TILE_SIZE[1] , self.BOARD_SIZE[0] + 50, self.TILE_SIZE[0] * 11, "Redraw")
        redraw_cancel = Button(self.BOARD_SIZE[0], self.BOARD_SIZE[1], 0, 0, "Click to Cancel Redraw", color=(0, 0, 0), alpha= 200, text_color=(255, 255, 255))

        #board covers
        enter_blank = Button(self.BOARD_SIZE[0], self.BOARD_SIZE[1], 0, 0, "Input Letter for Blank", color=(0, 0, 0),alpha= 200, text_color=(255, 255, 255))
        end_game = Button(self.BOARD_SIZE[0], self.BOARD_SIZE[1], 0, 0, "Game Over!", color=(0, 0, 0),alpha= 200, text_color=(255, 255, 255), font_size= 120)

        timer_text = Button(100, self.TILE_SIZE[1], self.BOARD_SIZE[0] + 50, self.TILE_SIZE[0] * 9, "Timers:", color=(250, 220, 120))
        self.timer = Button(200, self.TILE_SIZE[1], self.BOARD_SIZE[0] + 150, self.TILE_SIZE[0] * 9, str(self.time), color= (250, 220, 120))

        self.buttons.add(redraw)
        self.buttons.add(timer_text)
        self.buttons.add(self.timer)
        self.all_buttons.add(redraw)
        self.all_buttons.add(timer_text)
        self.all_buttons.add(self.timer)
        self.all_buttons.add(redraw_cancel)
        self.all_buttons.add(enter_blank)
        self.all_buttons.add(end_game)
        self.misc.add(p1)
        self.misc.add(p2)
        self.misc.add(self.p1_display)
        self.misc.add(self.p2_display)

    def get_press(self, x, y):
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
        for button in self.buttons:
            if button.rect.collidepoint((x, y)):
                return button

        return None

        # test = Tile('A',self.BOARD_SIZE[0]/self.width - 10, self.BOARD_SIZE[1]/self.height - 10)

    def select_tile(self, x, y):
        #generates selection/deselection/movement of a tile

        if self.selected == None:
            self.selected = self.get_press(x, y)
        elif not self.pause and isinstance(self.selected, Tile):
            if self.selected.in_play:
                self.tiles_in_play[self.selected.row] = self.tiles_in_play[self.selected.row][:self.selected.col] + '.' + self.tiles_in_play[self.selected.row][self.selected.col + 1:]
                self.selected.remove(self.in_play)
                if self.selected.is_blank:
                    self.selected.update_text('_')
                self.selected.in_play = False

            if 0 <= x <= self.BOARD_SIZE[0] and 0 <= y <= self.BOARD_SIZE[1]:
                col, row = self.selected.get_board_position(x, y)
                if self.tiles_in_play[row][col] == '.' and self.played_tiles[row][col] == '.':
                    # print(type(self.selected))
                    # print(self.selected.letter)
                    if self.selected.is_blank:
                        self.buttons.add(self.get_button("Input Letter for Blank"))
                        self.blank = self.selected
                        self.pause = True
                        # self.selected.update_text('A')
                    self.selected.update(x,y)
                    self.selected.in_play = True
                    self.in_play.add(self.selected)
                    self.tiles_in_play[row] = self.tiles_in_play[row][:col] + self.selected.letter + self.tiles_in_play[row][col + 1:]

            self.selected = None

        if self.selected and self.buttons and self.buttons in self.selected.groups():
            if self.selected.statement == "Redraw":
                if not self.redraw:
                    self.redraw = True
                    self.reset_active() #puts all the tile in hand to do redraw
                    self.buttons.add(self.get_button("Click to Cancel Redraw"))
                    color = 203, 203, 158
                    self.selected.update(self.selected.x_coord, self.selected.y_coord, color)
                    self.selected = None
                    return
                else:
                    color = 253, 253, 208
                    self.selected.update(self.selected.x_coord, self.selected.y_coord, color)
                    self.buttons.remove(self.get_button("Click to Cancel Redraw"))
                    self.update()
                    if len(self.selection) > 0:
                        self.next_turn()
                    self.redraw = False
                    self.selected = None
                    return
            elif self.selected.statement == "Click to Cancel Redraw":
                self.selection.empty()
                button = self.get_button("Redraw")
                button.update(button.x_coord, button.y_coord, (253, 253, 208))
                self.redraw = False
                self.selected.remove(self.buttons)
                self.selected = None

        if self.redraw and isinstance(self.selected, Tile):
            if self.selected in self.selection.sprites():
                self.selection.remove(self.selected)
            else:
                self.selection.add(self.selected)
            # print(self.selection)
            self.selected = None

    def get_tile_on_board(self, row, col):
        for tile in self.on_board:
            if tile.row == row and tile.col == col:
                return tile
        for tile in self.in_play:
            if tile.row == row and tile.col == col:
                return tile

    def enter_blank(self, letter):
        self.blank.update_text(letter)
        row = self.blank.row
        col = self.blank.col
        self.tiles_in_play[row] = self.tiles_in_play[row][:col] + self.blank.letter + self.tiles_in_play[row][col + 1:]
        self.blank = None
        self.buttons.remove(self.get_button("Input Letter for Blank"))
        self.pause = False

    def next_turn(self):
        #updates scores and removes tiles from hands of player
        print("Next Turn")

        player = None

        if self.turn == 0:
            self.p1_score = self.p1_score + self.score
            # print("Player 1 Score Updated: ", self.p1_score)
            # print(str(self.p1_score))
            self.p1_display.update_text(str(self.p1_score))
            # print(self.p1_display)
            player = self.player1
        else:
            self.p2_score = self.p2_score + self.score
            self.p2_display.update_text(str(self.p2_score))
            player = self.player2

        # print("Score Reset")
        self.score = 0

        if self.redraw:
            for tile in self.selection:
                tile.add(self.purse)
                tile.remove(player)
                tile.remove(self.selection)
        else:
            for tile in self.in_play:
                # print("Moving tile letter: ", tile.letter)
                tile.add(self.on_board)
                tile.remove(player)
                tile.remove(self.in_play)
                self.played_tiles[tile.row] = self.played_tiles[tile.row][:tile.col] + tile.letter + self.played_tiles[tile.row][tile.col + 1:]
                self.tiles_in_play[tile.row] = self.tiles_in_play[tile.row][:tile.col] + '.' + self.tiles_in_play[tile.row][tile.col + 1:]

        self.turn ^= 1
        self.switching = True

    def reset_active(self):
        # print("Reset Active")

        for tile in self.in_play:
            self.tiles_in_play[tile.row] = self.tiles_in_play[tile.row][:tile.col] + '.' + self.tiles_in_play[tile.row][tile.col + 1:]
            tile.remove(self.in_play)
            tile.in_play = False

    def get_word_score(self, word):
        #word should be a list of the tiles that were used to compose a word
        #this function checks each tiles' value and multiplies them according to the board's multipliers

        multiplier = 1
        effect = ''
        word_score = 0

        for tile in word:
            tile_score = 0
            slot = self.board[tile.row][tile.col]
            # print("Slot: ", slot)
            slot_multiplier = int(self.board_key[slot]['multiplier'])
            effect = self.board_key[slot]['effect_on']
            if not tile.is_blank:
                tile_score = int(self.tiles_key[tile.letter]['points'])
            if effect == 'word':
                multiplier = multiplier * slot_multiplier
            elif effect == 'letter':
                tile_score = tile_score * slot_multiplier
            word_score += tile_score

        word_score = word_score * multiplier

        # print('Word Score:', word_score)

        return word_score

    def get_button(self, statement):
        for button in self.all_buttons.sprites():
            if button.statement == statement:
                return button
        return None

    def end_game(self):
        self.end = True
        self.buttons.add(self.get_button("Game Over!"))


class Tile(pygame.sprite.Sprite):
    def __init__(self, letter, width, height, score = "0"):
        pygame.sprite.Sprite.__init__(self)

        #holds tile pixel size
        self.width = width
        self.height = height

        #holds character value
        self.letter = letter
        self.score = score
        self.is_blank = False
        if score == '0':
            self.is_blank = True

        #used to know when and where tiles should be shown
        self.in_play = False
        self.visible = False

        #identify location of tile on board (-1 means its not on the board)
        self.col = -1
        self.row = -1

        #generates tile image to draw
        self.font = pygame.font.SysFont(None, 30)
        self.score_font = pygame.font.SysFont(None, 15)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.text = self.font.render(letter, True, (0, 0, 0))
        self.score_text = self.score_font.render(score, True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.score_rect = self.score_text.get_rect(center=(self.text_rect.topleft[0] - 5, self.text_rect.topleft[1] - 5))
        self.image.fill((253,253,208))
        self.image.blits([(self.text, self.text_rect),(self.score_text, self.score_rect)])

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

    def update_text(self, letter):
        self.letter = letter
        self.text = self.font.render(letter, True, (0, 0, 0))
        self.image.fill((253, 253, 208))
        self.image.blits([(self.text, self.text_rect),(self.score_text, self.score_rect)])


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

class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, statement, color = (253, 253, 208), text_color = (0, 0, 0), font_size = 30, alpha = 255, pressable = True):
        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height

        # holds display statement value
        self.statement = statement
        self.x_coord = x
        self.y_coord = y
        self.color = color
        self.text_color = text_color
        self.font_size = font_size
        self.pressable = pressable

        # generates tile image to draw
        self.font = pygame.font.SysFont(None, self.font_size)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.text = self.font.render(self.statement, True, self.text_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.image.fill(self.color)
        self.image.set_alpha(alpha)
        self.image.blit(self.text, self.text_rect)

        self.rect.topleft = self.x_coord, self.y_coord

    def update(self, x, y, color):
        self.color = color
        self.x_coord = x
        self.y_coord = y

        self.image.fill(self.color)
        self.image.blit(self.text, self.text_rect)

        self.rect.topleft = self.x_coord, self.y_coord

    def update_text(self, statement):
        # print("Updating Text")
        # print("Old Text: ", self.statement)
        self.statement = statement
        # print("Updated Text: ", self.statement)
        self.text = self.font.render(self.statement, True, self.text_color)
        self.update(self.x_coord, self.y_coord, self.color)

    def pressed(self):
        pass

    def __str__(self):
        return f"Text: {self.statement}"




