#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import pygame
# from scrabble.board import Scrabble_Board
from scrabble.scenes import StartScreen, BoardScreen

def main():
    window = Scrabble()
    window.run()

class Scrabble(object):
    def __init__(self, window_width=1000, window_height=600):
        pygame.init()

        self.screen = pygame.display.set_mode((window_width,window_height))

    def run(self):
        scene = StartScreen()


        while scene:
            key_inputs = pygame.key.get_pressed()
            inputs = []
            for event in pygame.event.get():
                quit = False
                if event.type == pygame.QUIT:
                    quit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit = True


                if quit:
                    scene = None
                else:
                    inputs.append(event)

            if scene:
                scene.ProcessInput(inputs, key_inputs)
                scene.Update()
                scene.Render(self.screen)

                scene = scene.next

                pygame.display.flip()

if __name__ == "__main__":
    main()
