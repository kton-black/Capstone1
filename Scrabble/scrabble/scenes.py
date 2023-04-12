import pygame
import itertools
import random

from scrabble.board import Scrabble_Board
from scrabble.board import Button

# https://nerdparadise.com/programming/pygame/part7

class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

class StartScreen(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

        self.buttons = pygame.sprite.Group()
        self.load_buttons()

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            # if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                # self.SwitchToScene(BoardScreen())
                # pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed = None
                for button in self.buttons:
                    if button.rect.collidepoint((event.pos[0], event.pos[1])):
                        pressed = button
                        break
                if pressed:
                    if pressed.statement == "Player VS Computer":
                        self.SwitchToScene(BoardScreen(vsComputer = True))
                    elif pressed.statement == "Player VS Player":
                        self.SwitchToScene(BoardScreen())
                    elif pressed.statement == "Exit Game":
                        self.SwitchToScene(None)

    def Update(self):

        pass

    def Render(self, screen):
        # print("Start")
        screen.fill((255,0,0))
        self.buttons.draw(screen)

    def load_buttons(self):

        # width, height, x, y, statement, color = (253, 253, 208), text_color = (0, 0, 0), alpha = 255, pressable = True
        playerVcomputer = Button(500, 75, 250, 300, "Player VS Computer", font_size= 60)
        playerVplayer = Button(500, 75, 250, 400, "Player VS Player", font_size= 60)
        exit = Button(500, 75, 250, 500, "Exit Game", font_size= 60)
        pygame.display.flip()

        self.buttons.add(playerVcomputer)
        self.buttons.add(playerVplayer)
        self.buttons.add(exit)

class BoardScreen(SceneBase):
    def __init__(self, vsComputer = False):
        SceneBase.__init__(self)
        self.selecting = False
        self.board = Scrabble_Board(vsComputer= vsComputer)
        self.check = False
        self.vsComputer = vsComputer
        self.clock = pygame.time.Clock()
        self.timer = pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.redraw = False

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if self.vsComputer and self.board.turn == 1:
                print('Computer turn')
                tiles = []
                blanks = []
                self.redraw = True

                for tile in self.board.player2.sprites():
                    tiles.append(tile.letter)
                possible_words = self.computer_player(self.board.played_tiles, tiles)
                if possible_words:
                    for index in range(len(possible_words)):
                        moves = possible_words[index]
                        print(moves)
                        if moves:
                            while "_" in tiles:
                                for play in moves:
                                    if play[0] in tiles:
                                        tiles.remove(play[0])
                                    else:
                                        blanks.append(play[0])
                            for move in moves:
                                for tile in self.board.player2.sprites():
                                    if move[0] == tile.letter:
                                        x, y = tile.rect.center
                                        self.board.select_tile(x, y)
                                        x = self.board.TILE_SIZE[0] * move[1]
                                        y = self.board.TILE_SIZE[1] * move[2]
                                        self.board.select_tile(x, y)
                                    elif tile.letter == "_" and move[0] in blanks:
                                        x, y = tile.rect.center
                                        self.board.select_tile(x, y)
                                        x = self.board.TILE_SIZE[0] * move[1]
                                        y = self.board.TILE_SIZE[1] * move[2]
                                        self.board.select_tile(x, y)
                                        self.board.enter_blank(chr(move[0]))
                            self.check = True
                            self.Update()
                            if not self.redraw:
                                break
                if self.redraw:
                    redraw_button = self.board.get_button("Redraw")
                    x, y = redraw_button.rect.center
                    self.board.select_tile(x, y)
                    for tile in self.board.player2.sprites():
                        x, y = tile.rect.center
                        self.board.select_tile(x, y)
                    x, y = redraw_button.rect.center
                    self.board.select_tile(x, y)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # select/deselect objects
                self.board.select_tile(event.pos[0], event.pos[1])
                self.selecting = not self.selecting

            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                # end turn
                if not self.board.pause:
                    self.check = True

            elif self.board.blank and event.type == pygame.KEYDOWN and (64 < event.key < 91 or 96 < event.key < 123):
                if event.key > 96:
                    event.key = event.key - 32
                # print("Blank Letter Input: ", chr(event.key))
                self.board.enter_blank(chr(event.key))

            elif event.type == pygame.USEREVENT:
                self.board.time = self.board.time - 1
                self.board.timer.update_text(str(self.board.time)) if self.board.time > 0 else self.board.end_game()


    def Update(self):
        # call functions to verify plays
        # print("Updating Scene")

        if self.check:
            if self.Verify_Turn():
                # self.board.get_score()
                self.board.next_turn()
                if self.vsComputer:
                    self.redraw = False
            else:
                self.board.reset_active()

        self.board.update()
        self.check = False

    def Render(self, screen):
        # print("Game")
        screen.fill((250, 220, 120))
        self.board.render(screen)

    def Verify_Turn(self):
        #verifies if the turn was valid
        # print("Verifying Turn")

        rows, cols = [], []
        horizontal = False
        vertical = False
        on_played = False
        merged, start = self.Merge_Masks()
        # print(merged)

        #gets the rows and columns of the tiles in play
        if not self.board.in_play:
            return False
        for tile in self.board.in_play:
            rows.append(tile.row)
            cols.append(tile.col)

        # print("Max Rows: ", max(rows))
        # print("Min Rows: ", min(rows))

        # print("Max Cols: ", max(cols))
        # print("Min Cols: ", min(cols))

        horizontal = all(row == rows[0] for row in rows)
        vertical = all(col == cols[0] for col in cols)

        if horizontal or vertical:
            #verifies if played letters are adjacently in the same row or in the same column

            num_tiles = len(self.board.in_play.sprites())
            # print("# of Tiles: ", num_tiles)

            if num_tiles == 1:
                if not on_played:
                    if min(cols) - 1 > -1 and not self.board.played_tiles[rows[0]][min(cols)-1] == '.' or\
                       max(cols) + 1 < len(merged) and not self.board.played_tiles[rows[0]][max(cols)+1] == '.' or \
                       min(rows) - 1 > -1 and not self.board.played_tiles[min(rows) - 1][cols[0]] == '.' or\
                       max(rows) + 1 < len(merged) and not self.board.played_tiles[max(rows)+1][cols[0]] == '.':
                        on_played = True

            elif horizontal:
                for col in range(min(cols), max(cols)+1):
                    print("Horizontal")
                    print("Row: ", rows[0])
                    print("Col: ", col)

                    #checks for blank in between characters
                    if merged[rows[0]][col] == '.':
                        return False
                    #checks if expanding off of played tiles in between letters (requirement to play word)
                    elif not self.board.played_tiles[rows[0]][col] == '.':
                        on_played = True
                # checks if starting word is on starting square
                if start and 7 in rows and 7 in cols:
                    on_played = True
                # checks if expanding off of played tiles on edges horizontally
                elif not on_played:
                    if min(cols) - 1 > -1 and not self.board.played_tiles[rows[0]][min(cols)-1] == '.' or\
                       max(cols) + 1 < len(merged) and not self.board.played_tiles[rows[0]][max(cols)+1] == '.':
                        on_played = True

            elif vertical:
                for row in range(min(rows), max(rows)+1):
                    print("Vertical")
                    print("Row: ", row)
                    print("Col: ", cols[0])
                    if merged[row][cols[0]] == '.':
                        return False
                    # checks if expanding off of played tiles in between letters
                    elif not self.board.played_tiles[row][cols[0]] == '.':
                        on_played = True
                # checks if starting word is on starting square
                if start and 7 in rows and 7 in cols:
                    on_played = True
                # checks if expanding off of played tiles on edges vertically
                elif not on_played:
                    if min(rows) - 1 > -1 and not self.board.played_tiles[min(rows)-1][cols[0]] == '.' or\
                       max(rows) + 1 < len(merged) and not self.board.played_tiles[max(rows)+1][cols[0]] == '.':
                        on_played = True

            print("On Played: ", on_played)
            if on_played:

                score = self.Check_Words(merged) - self.Check_Words(self.board.played_tiles)
                # print("On Played Score: ", score)
                if score > 0:
                    self.board.score = score
                    return True
        return False

    def Merge_Masks(self):
        # combines board masks

        start = True
        tiles = []
        for playing_row, played_row in zip(self.board.tiles_in_play, self.board.played_tiles):
            tiles.append([])
            for playing, played in zip(playing_row, played_row):
                if not playing == '.':
                    tiles[-1].append(playing)
                elif not played == '.':
                    tiles[-1].append(played)
                    start = False
                else:
                    tiles[-1].append('.')

        return tiles, start

    def Check_Words(self, board):

        # matches = {}
        # found_words = []
        rows = len(board)
        cols = len(board[0])
        score = 0

        # print("Check Words")

        # search left to right
        for i in range(rows):
            for j in range(cols):
                if board[i][j] != '.':
                    # print(board[i][j])
                    # print(j)
                    if j == 0 or board[i][j - 1] == '.':
                        # search horizontally
                        # print("Search Horizontally")
                        h_word = ''
                        h_tiles = []
                        for k in range(j, cols):
                            if board[i][k] == '.':
                                break
                            h_word += board[i][k]
                            h_tiles.append(self.board.get_tile_on_board(i, k))

                        # print("Horizontal Word: ", h_word)
                        if len(h_word) > 1:
                            if self.valid_word(h_word):
                                # print("Valid Word: ", h_word)
                                word_score = self.board.get_word_score(h_tiles)
                                score = score + word_score
                            else:
                                return -1

                    if i == 0 or board[i - 1][j] == '.':
                        # search vertically
                        # print("Search Vertically")
                        v_word = ''
                        v_tiles = []
                        for k in range(i, rows):
                            if board[k][j] == '.':
                                break
                            v_word += board[k][j]
                            v_tiles.append(self.board.get_tile_on_board(k, j))

                        # print("Vertical Word: ", v_word)
                        if len(v_word) > 1:
                            if self.valid_word(v_word):
                                word_score = self.board.get_word_score(v_tiles)
                                score = score + word_score
                            else:
                                return -1

        # print("Score: ", score)

        return score

    def valid_word(self, input_word):
        # Checks the length of the input word
        word_length = len(input_word)

        # print("Check if word")
        # Creates a file name according to word length
        word_file = 'scrabble/dictionary/' + str(word_length) + 'letterwords.txt'

        # Open and read only the file that matches the word length
        with open(word_file, 'r') as file:
            words = file.read().splitlines()

        # Checks if the input word matches a word in the file
        # Returns valid if the word is found in the text file
        # If the word is not found in the text file, prints invalid word
        if input_word in words:
            # Use bool values to return whether true/valid or false/invalid
            return True
        else:
            return False

    def find_index(self, word, letter):
        start = 0
        while True:
            start = word.find(letter, start)
            if start == -1: return
            yield start
            start += len(letter)  # use start += 1 to find overlapping matches

    def computer_player(self, board_array, letters_in_hand):
        alphabet = ''

        for row in board_array:
            for letter in row:
                if not letter in alphabet and not letter == '.':
                    alphabet = alphabet + letter

        # alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # print(alphabet)

        # replace any '_' in letters_in_hand with a random vowel
        letters_in_hand = [random.choice(['A', 'E', 'I', 'O', 'U']) if letter == '_' else letter for letter in
                           letters_in_hand]

        print(letters_in_hand)

        # initialize a dictionary to store the words for each letter of the alphabet
        alphabet_words = {}
        for letter in alphabet:
            alphabet_words[letter] = []
        # print(alphabet_words)

        # iterate through each letter in the alphabet and find all possible words
        # basically is adds one letter at a time to the letters_in_hand, sees what words it can make with it and adds those words to a dictionary for that letter
        # then it removes that letter from the letters_in_hand and moves on to the next one
        # for horizontal and vertical plays later, it iterates through all letters again
        # if finds where that letter is on the board and trys to make sure it can place words from that letters dictionary
        for letter in alphabet:
            # print(letter)
            words_for_letter = []
            letters_in_hand.append(letter)
            for length in range(2, len(letters_in_hand) + 1):
                # print(length)
                for tiles in itertools.combinations(letters_in_hand, length):
                    # print(tiles)
                    word = ''.join(tiles)
                    if self.valid_word(word):
                        if not word in words_for_letter and letter in word:
                            # print(word)
                            words_for_letter.append(word)
            # print('Next')
            letters_in_hand.pop()
            alphabet_words[letter] = words_for_letter

        possible_words = []

        for letter in alphabet:
            # print('Letter: ', letter)
            num_words = 0
            letter_positions = []
            for row in range(len(board_array)):
                for col in range(len(board_array[row])):
                    if board_array[row][col] == letter:
                        letter_positions.append((row,col))

            for word in alphabet_words[letter]:
                if num_words >= 10:
                    break
                # print('Word: ', word)
                indexes = self.find_index(word, letter)
                for index in indexes:
                    for letter_position in letter_positions:
                        horizontal, vertical = True, True
                        horizontal_word, vertical_word = [], []
                        for i in range(len(word)):
                            if i < index or i > index:
                                # check horizontal
                                if horizontal and 0 < letter_position[1] - (index - i) < len(board_array) and board_array[letter_position[0]][letter_position[1] - (index - i)] == '.':
                                    horizontal_word.append((word[i], letter_position[0], letter_position[1] - (index - i)))
                                else:
                                    horizontal = False
                                # check vertical
                                if vertical and 0 < letter_position[0] - (index - i) < len(board_array) and board_array[letter_position[0] - (index - i)][letter_position[1]] == '.':
                                    vertical_word.append((word[i], letter_position[0] - (index - i), letter_position[1]))
                                else:
                                    vertical = False
                        if horizontal and 0 < letter_position[1] - index - 1 < len(board_array) and board_array[letter_position[0]][letter_position[1] - index - 1] != '.' and  0 < letter_position[1] - index + len(word) < len(board_array) and board_array[letter_position[0]][letter_position[1] - index + len(word)] != '.':
                            horizontal = False
                        if vertical and 0 < letter_position[0] - index - 1 < len(board_array) and board_array[letter_position[0] - index - 1][letter_position[1]] != '.' and  0 < letter_position[0] - index + len(word) < len(board_array) and board_array[letter_position[0] - index + len(word)][letter_position[1]] != '.':
                            vertical = False
                        if horizontal:
                            print('Word: ', word)
                            print('Horizontal Word: ', horizontal_word)
                            possible_words.append(horizontal_word)
                            num_words += 1
                        if vertical:
                            print('Word: ', word)
                            print('Vertical Word: ', vertical_word)
                            possible_words.append(vertical_word)
                            num_words += 1
        if len(possible_words) > 0:
            return possible_words
        return None
