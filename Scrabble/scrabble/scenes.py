import pygame
import itertools

from scrabble.board import Scrabble_Board

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

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                self.SwitchToScene(BoardScreen())

    def Update(self):
        pass

    def Render(self, screen):
        # print("Start")
        screen.fill((255,0,0))

class BoardScreen(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.selecting = False
        self.board = Scrabble_Board()
        self.check = False

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # select/deselect tile
                self.board.select_tile(event.pos[0], event.pos[1])
                self.selecting = not self.selecting

            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                # end turn
                self.check = True

        pass

    def Update(self):
        # call functions to verify plays
        # print("Updating Scene")

        if self.check:
            if self.Verify_Turn():
                # self.board.get_score()
                self.board.next_turn()
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
        print("Verifying Turn")

        rows, cols = [], []
        horizontal = False
        vertical = False
        on_played = False
        merged, start = self.Merge_Masks()
        print(merged)

        #gets the rows and columns of the tiles in play
        if not self.board.in_play:
            return False
        for tile in self.board.in_play:
            rows.append(tile.row)
            cols.append(tile.col)

        print("Max Rows: ", max(rows))
        print("Min Rows: ", min(rows))

        print("Max Cols: ", max(cols))
        print("Min Cols: ", min(cols))

        horizontal = all(row == rows[0] for row in rows)
        vertical = all(col == cols[0] for col in cols)

        if horizontal or vertical:
            #verifies if played letters are adjacently in the same row or in the same column

            num_tiles = len(self.board.in_play.sprites())
            print("# of Tiles: ", num_tiles)

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
                    # print("Row: ", rows[0])
                    # print("Col: ", col)

                    #checks for blank in between characters
                    if merged[rows[0]][col] == '.':
                        return False
                    #checks if expanding off of played tiles in between letters (requirement to play word)
                    elif not self.board.played_tiles[rows[0]][col] == '.':
                        on_played = True
                # checks if edge tile is on starting square
                if start and (max(cols) == 7 or min(cols) == 7):
                    on_played = True
                # checks if expanding off of played tiles on edges horizontally
                elif not on_played:
                    if min(cols) - 1 > -1 and not self.board.played_tiles[rows[0]][min(cols)-1] == '.' or\
                       max(cols) + 1 < len(merged) and not self.board.played_tiles[rows[0]][max(cols)+1] == '.':
                        on_played = True

            elif vertical:
                for row in range(min(rows), max(rows)+1):
                    print("Vertical")
                    # print("Row: ", row)
                    # print("Col: ", cols[0])
                    if merged[row][cols[0]] == '.':
                        return False
                    # checks if expanding off of played tiles in between letters
                    elif not self.board.played_tiles[row][cols[0]] == '.':
                        on_played = True
                # checks if edge tile is on starting square
                if start and (max(rows) == 7 or min(rows) == 7):
                    on_played = True
                # checks if expanding off of played tiles on edges vertically
                elif not on_played:
                    if min(rows) - 1 > -1 and not self.board.played_tiles[min(rows)-1][cols[0]] == '.' or\
                       max(rows) + 1 < len(merged) and not self.board.played_tiles[max(rows)+1][cols[0]] == '.':
                        on_played = True

            print("On Played: ", on_played)
            if on_played:

                score = self.Check_Words(merged) - self.Check_Words(self.board.played_tiles)
                print("On Played Score: ", score)
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

        print("Check Words")

        # search left to right
        for i in range(rows):
            for j in range(cols):
                if board[i][j] != '.':
                    print(board[i][j])
                    print(j)
                    if j == 0 or board[i][j - 1] == '.':
                        # search horizontally
                        print("Search Horizontally")
                        h_word = ''
                        h_tiles = []
                        for k in range(j, cols):
                            if board[i][k] == '.':
                                break
                            h_word += board[i][k]
                            h_tiles.append(self.board.get_tile_on_board(i, k))

                        print("Horizontal Word: ", h_word)
                        if len(h_word) > 1:
                            if self.valid_word(h_word):
                                print("Valid Word: ", h_word)
                                word_score = self.board.get_word_score(h_tiles)
                                score = score + word_score
                            else:
                                return -1

                    if i == 0 or board[i - 1][j] == '.':
                        # search vertically
                        print("Search Vertically")
                        v_word = ''
                        v_tiles = []
                        for k in range(i, rows):
                            if board[k][j] == '.':
                                break
                            v_word += board[k][j]
                            v_tiles.append(self.board.get_tile_on_board(k, j))

                        print("Vertical Word: ", v_word)
                        if len(v_word) > 1:
                            if self.valid_word(v_word):
                                word_score = self.board.get_word_score(v_tiles)
                                score = score + word_score
                            else:
                                return -1

        print("Score: ", score)

        return score

    def valid_word(self, input_word):
        # Checks the length of the input word
        word_length = len(input_word)

        print("Check if word")
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