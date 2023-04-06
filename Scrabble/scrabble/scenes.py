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
                #checks if expanding off of played tiles on edges horizontally
                if not on_played:
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
                # checks if expanding off of played tiles on edges vertically
                if not on_played:
                    if min(rows) - 1 > -1 and not self.board.played_tiles[min(rows)-1][cols[0]] == '.' or\
                       max(rows) + 1 < len(merged) and not self.board.played_tiles[max(rows)+1][cols[0]] == '.':
                        on_played = True

            print("On Played: ", on_played)
            if start or on_played:
                self.Check_Words()
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

    def Check_Words(self):
        pass
