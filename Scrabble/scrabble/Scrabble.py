#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import pygame
# from scrabble.board import Scrabble_Board
from scrabble.scenes import StartScreen, BoardScreen

def main():
    window = Scrabble()



    #List of all letters in scrabble
    # player_letters = ['E','E','E','E','E','E','E','E','E','E','E','E','A','A','A','A','A','A','A','A','A','I','I','I','I','I','I','I','I','I','O','O','O','O','O','O','O','O','N','N','N','N','N','N','R','R','R','R','R','R','T','T','T','T','T','T','L','L','L','L','S','S','S','S','U','U','U','U','D','D','D','D','G','G','G','B','B','C','C','M','M','P','P','F','F','H','H','V','V','W','W','Y','Y','K','J','X','Q','Z','_','_']
    # letters_in_hand = []
    #letters_in_hand[7]

    #Variables
    # lst = []
    # score = 0
    # total = 0
    # i = 0
    # count = 0

    # screen = pygame.display.set_mode((1000, 600))
    # background = pygame.Surface((1000, 1000))
    # background.fill((255, 0, 255))
    # screen.blit(background, (0, 0))
    # board = Scrabble_Board(screen)
    # board.create_board()
    # board.display(screen)
    # pygame.display.flip()

    # screen.blit(pygame.transform.scale(board.window, (1000, 1000)), (0, 0))

    #grabs username
    # username: str = input("Please enter a username: ")
    # print("Is-", username, "-playing? If yes, type Yes, if no, type No: ")
    # player = input()
    # print("\n\n\n")

    # board.start()

    #Keep total for user playing
    # if player == "Yes":
    #
    #     #Keeping track of user's points
    #     while player == "Yes":
    #
    #         #Grabbing letters from the letter pool
    #         for randomletter in player_letters:
    #             while count <= 7:
    #                 if count == 7:
    #                     break
    #                 else:
    #                     randomletter = random.choices(player_letters)
    #                     letters_in_hand.append(randomletter)
    #                     count = count + 1
    #
    #         print("Here are the letters you currently have: ", letters_in_hand)
    #
    #         #Resetting Score
    #         score = 0
    #
    #         #Getting the input for the word the user would like to use
    #         WordInput: str = input("Please Enter a valid word With the letters you received (If you have a blank tile, use an underscore in the loaction of where you'd like to use it): \n")
    #
    #         #Making letters uppercase
    #         Word = WordInput.upper()
    #
    #         #Making sure the word is within the space allowed
    #         if len(Word) > 15:
    #             print("Invalid word, must be smaller than 15 letters")
    #         else:
    #             print("\n\nYou typed the word: ", Word)
    #
    #             #For an i in the word
    #             for letter in Word:
    #                 #Split the up the word
    #                 lst.append(letter)
    #                 temp = 0
    #
    #                 #Finding the letter and change it to its numerical value
    #                 #Blank tile is worth 0 points
    #                 if lst[i] == '_':
    #                     score = score + 0
    #                 elif lst[i] == 'A':
    #                     score = score + 1
    #                 elif lst[i] == 'E':
    #                     score = score + 1
    #                 elif lst[i] == 'I':
    #                     score = score + 1
    #                 elif lst[i] == 'L':
    #                     score = score + 1
    #                 elif lst[i] == 'N':
    #                     score = score + 1
    #                 elif lst[i] == 'O':
    #                     score = score + 1
    #                 elif lst[i] == 'R':
    #                     score = score + 1
    #                 elif lst[i] == 'S':
    #                     score = score + 1
    #                 elif lst[i] == 'T':
    #                     score = score + 1
    #                 elif lst[i] == 'U':
    #                     score = score + 1
    #                 elif lst[i] == 'D':
    #                     score = score + 2
    #                 elif lst[i] == 'G':
    #                     score = score + 2
    #                 elif lst[i] == 'B':
    #                     score = score + 3
    #                 elif lst[i] == 'C':
    #                     score = score + 3
    #                 elif lst[i] == 'M':
    #                     score = score + 3
    #                 elif lst[i] == 'P':
    #                     score = score + 3
    #                 elif lst[i] == 'F':
    #                     score = score + 4
    #                 elif lst[i] == 'H':
    #                     score = score + 4
    #                 elif lst[i] == 'V':
    #                     score = score + 4
    #                 elif lst[i] == 'W':
    #                     score = score + 4
    #                 elif lst[i] == 'Y':
    #                     score = score + 4
    #                 elif lst[i] == 'K':
    #                     score = score + 5
    #                 elif lst[i] == 'J':
    #                     score = score + 8
    #                 elif lst[i] == 'X':
    #                     score = score + 8
    #                 elif lst[i] == 'Q':
    #                     score = score + 10
    #                 elif lst[i] == 'Z':
    #                     score = score + 10
    #
    #                 #Increments through the list
    #                 i += 1
    #                 temp = score
    #
    #         print("The score of your word is: ", score)
    #
    #         #Gathering the total after every 'round'
    #         total = total + temp
    #         print(username, "total score is: ", total, "\n\n")
    #
    #         print("Is", username, "Still playing? If yes, type Yes. If not, type No:")
    #         player = input()
    #         print("\n\n")
    #
    # elif player == "No":
    #     print("Don't cheat!")
    #
    # else:
    #     print("Invalid Input")

class Scrabble(object):
    def __init__(self, window_width=1000, window_height=600):
        self.screen = pygame.display.set_mode((window_width,window_height))
        self.run()

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

            scene.ProcessInput(inputs, key_inputs)
            scene.Update()
            scene.Render(self.screen)

            scene = scene.next

            pygame.display.flip()

if __name__ == "__main__":
    main()
