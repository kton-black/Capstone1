import pygame

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

                pass
            elif event.type == pygame.MOUSEMOTION:
                # move tile
                pass
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                # end turn
                self.check = True
                pass
        pass

    def Update(self):
        # call functions to verify plays
        verified = False
        if self.check:
            print("Insert verification code")


        pass

    def Render(self, screen):
        # print("Game")
        screen.fill((250, 220, 120))
        self.board.render(screen)

    def verify_word(self):
        pass
