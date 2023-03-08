#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
from validword import valid_word

#predefined letter values for score calculation
letter_values = {
    '_': 0, 'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
    'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10,
    'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
}


def gathering_letters(n, player_letters):

    letters_in_hand = []

    #Grabbing letters from the letter pool
    for x in range(0,7):
        #Only giving the user 7 letters

        #Grabbing random letters and adding them into the list
        randomletter = random.choices(player_letters)[0]
        letters_in_hand.append(randomletter)

        player_letters.remove(randomletter)

    #allows redrawing
    valid_input = False
    while valid_input == False:
        print("\nHere are the letters you currently have: ", letters_in_hand) 
        print("\nWould you like to redraw tiles?")
        player_input = input("Type yes or no: ")
        if player_input == "Yes" or player_input == "yes":
            redraw(letters_in_hand, player_letters)
        elif player_input == "No" or player_input == "no":
            valid_input = True
            print("\nOkay! Here are your tiles: ", letters_in_hand)
        else:
    	    print("Invalid input, please try again!\n")

    return letters_in_hand, player_letters


def redraw(letters_in_hand, player_letters):
    # Create a copy of the letters_in_hand list
    letters_copy = letters_in_hand.copy()

    # Empty tiles in hand and add them to letter pool
    for letter in letters_copy:
        if letter in player_letters:
            letters_in_hand.remove(letter)
            player_letters.append(letter)

    # Grabbing letters from the letter pool
    for x in range(len(letters_in_hand), 7):
        # Only giving the user enough letters to have 7
        if len(player_letters) == 0:
            break

        # Grabbing random letters and adding them into the list
        randomletter = random.choice(player_letters)
        letters_in_hand.append(randomletter)
        player_letters.remove(randomletter)

    return letters_in_hand, player_letters




#removes letters from letter_tiles that are in word
def remove_letters(Word, letter_tiles):
	for letter in Word:
		letter_tiles = [x for x in letter_tiles if x != letter]
	return letter_tiles




#refills hand with available tiles in letter pool
def add_letters(letter_tiles, letter_pool):
    num_tiles = len(letter_tiles)
    if num_tiles < 7:
        num_new_tiles = 7 - num_tiles
        new_tiles = random.choices(letter_pool, k=num_new_tiles)
        letter_tiles.extend(new_tiles)
        for tile in new_tiles:
            letter_pool.remove(tile)
    #allows redrawing
    valid_input = False
    while valid_input == False:
        print("\nHere are your new tiles: ", letter_tiles) 
        print("\nWould you like to redraw tiles?")
        player_input = input("Type yes or no: ")
        if player_input == "Yes" or player_input == "yes":
            redraw(letter_tiles, letter_pool)
        elif player_input == "No" or player_input == "no":
            valid_input = True
            print("\nOkay! Here are your tiles: ", letter_tiles)
        else:
    	    print("Invalid input, please try again!\n")

    return letter_tiles, letter_pool




#uses letter_values to calculate the score of a word
def calc_word_score(word):
    lst = list(word.upper())
    score = 0
    for letter in lst:
        score += letter_values.get(letter, 0)
    return score






def gather_score(username, player_num, letter_tiles, letter_pool, player_moves):
    #Variables
    score = 0

    #Getting the input for the word the user would like to use
    print(letter_tiles)
    WordInput: str = input("Please Enter a valid word from you tiles: ")
    valid_input = False

    while valid_input == False:
        #Making letters uppercase
        Word = WordInput.upper()
        temp_letter_tiles = letter_tiles

        #check input is made from tiles in hand
        for char in Word:
       	    if char in letter_tiles:
       	        temp_letter_tiles.remove(char)
        	    #valid word
                if len(Word) >= 2 and len(Word) <= 15:
                    if valid_word(Word) == True:
        	            valid_input = True
       	            else:
                        WordInput: str = input("Invalid word, please try again: ")
                else:
        	        WordInput: str = input("Invalid word, please try again: ")
            else:
        	    WordInput: str = input("Please only use tiles in your hand. Invalid word, please try again: ")

    letter_tiles = remove_letters(Word, letter_tiles)

    score = calc_word_score(Word)

    print("The score of your word is: ", score) 
    letter_tiles, letter_pool = add_letters(letter_tiles, letter_pool)
    player_moves.append(Word)

    return score, letter_tiles, letter_pool, player_moves



def main() -> None:
    #letter pool
    letter_pool = ['E','E','E','E','E','E','E','E','E','E','E','E','A','A','A','A','A','A','A','A','A','I','I','I','I','I','I','I','I','I','O','O','O','O','O','O','O','O','N','N','N','N','N','N','R','R','R','R','R','R','T','T','T','T','T','T','L','L','L','L','S','S','S','S','U','U','U','U','D','D','D','D','G','G','G','B','B','C','C','M','M','P','P','F','F','H','H','V','V','W','W','Y','Y','K','J','X','Q','Z','_','_']
    print("\nWelcome to Scrabble!\n")
    #grabs username from player 1 and 2
    username1: str = input("\nPlayer 1, please enter a username: ")
    player1_tiles, letter_pool = gathering_letters(7, letter_pool)
    username2: str = input("\nPlayer 2, please enter a username: ")
    player2_tiles, letter_pool = gathering_letters(7, letter_pool)

    player1_score = 0
    player1_moves =[]
    player2_score = 0
    player2_moves = []
    game_over = False

    print("\nLet's play Scrabble!\n")
    while game_over == False:
        player_num = 1;
        #Player 1 Turn
        print("\nPlayer 1 -", username1, "it is your turn! Continue game(type 'c') or quit(type 'q')?") 
        Continue_game = input()
        print("\n")

        valid_input = False
        while valid_input == False:
            if Continue_game == "c" or Continue_game == "C":
                player1_score_addition, player1_tiles, letter_pool, player1_moves =  gather_score(username1, player_num, player1_tiles, letter_pool, player1_moves)
                player1_score += player1_score_addition
                valid_input = True
            elif Continue_game == "q" or Continue_game == "Q":
                print("\nGame Over!")
                game_over = True
                valid_input = True
            else:
                print("\nInvalid Input, please try again! Type c to continue or q to quit")
                Continue_game = input()

        if Continue_game == "c" or Continue_game == "C":

            player_num = 2;
            #Player 2 Turn
            print("\nPlayer 2 -", username2, "it is your turn! Continue game(type 'c') or quit(type 'q')?")
            Continue_game = input() 
            print("\n")

            valid_input = False
            while valid_input == False:
                if Continue_game == "c" or Continue_game == "C":
                    player2_score_addition, player2_tiles, letter_pool, player2_moves =  gather_score(username2, player_num, player2_tiles, letter_pool, player2_moves)
                    player2_score += player2_score_addition
                    valid_input = True
                elif Continue_game  == "q" or Continue_game == "Q":
                    print("\nGame Over!")
                    game_over = True
                    valid_input = True
                else:
                    print("\nInvalid Input, please try again! Type c to continue or q to quit")
                    Continue_game = input()
    print("Player 1 Score: ", player1_score)
    print("Player 1 Moves: ", player1_moves)
    print("Player 2 Score: ", player2_score)
    print("Player 2 Moves: ", player2_moves) 


if __name__ == '__main__':
    main()
 
