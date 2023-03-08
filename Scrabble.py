#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
from validword import valid_word




def gathering_letters(n, player_leters):

    #List of all letters in scrabble
    player_letters = ['E','E','E','E','E','E','E','E','E','E','E','E','A','A','A','A','A','A','A','A','A','I','I','I','I','I','I','I','I','I','O','O','O','O','O','O','O','O','N','N','N','N','N','N','R','R','R','R','R','R','T','T','T','T','T','T','L','L','L','L','S','S','S','S','U','U','U','U','D','D','D','D','G','G','G','B','B','C','C','M','M','P','P','F','F','H','H','V','V','W','W','Y','Y','K','J','X','Q','Z','_','_']
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


def gather_score(username, player_num, letter_tiles, letter_pool, player_moves):
    #Variables
    lst = []
    score = 0
    total = 0
    i = 0

    #Resetting Score
    score = 0

    #Getting the input for the word the user would like to use
    WordInput: str = input("Please Enter a valid word from you tiles: ")
    valid_input = False

    while valid_input == False:
        #Making letters uppercase
        Word = WordInput.upper()

        #check input is made from tiles in hand
        for char in Word:
       	    if char in letter_tiles:
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
        #For an i in the word
        for letter in Word:
                #Split the up the word
                lst.append(letter)
                temp = 0

                #Finding the letter and change it to its numerical value
                #Blank tile is worth 0 points
                if lst[i] == '_':
                        score = score + 0
                if lst[i] == 'A':
                        score = score + 1 
                if lst[i] == 'E':
                        score = score + 1
                if lst[i] == 'I':
                        score = score + 1
                if lst[i] == 'L':
                        score = score + 1
                if lst[i] == 'N':
                        score = score + 1
                if lst[i] == 'O':
                        score = score + 1
                if lst[i] == 'R':
                        score = score + 1
                if lst[i] == 'S':
                        score = score + 1
                if lst[i] == 'T':
                        score = score + 1
                if lst[i] == 'U':
                        score = score + 1
                if lst[i] == 'D':
                        score = score + 2
                if lst[i] == 'G':
                        score = score + 2
                if lst[i] == 'B':
                        score = score + 3
                if lst[i] == 'C':
                        score = score + 3
                if lst[i] == 'M':
                        score = score + 3
                if lst[i] == 'P':
                        score = score + 3
                if lst[i] == 'F':
                        score = score + 4
                if lst[i] == 'H':
                        score = score + 4
                if lst[i] == 'V':
                        score = score + 4
                if lst[i] == 'W':
                        score = score + 4
                if lst[i] == 'Y':
                        score = score + 4
                if lst[i] == 'K':
                        score = score + 5
                if lst[i] == 'J':
                        score = score + 8
                if lst[i] == 'X':
                        score = score + 8
                if lst[i] == 'Q':
                        score = score + 10
                if lst[i] == 'Z':
                        score = score + 10

                #Increments through the list
                i += 1
                temp = score

                letter_tiles, letter_pool = add_letters(letter_tiles, letter_pool)
        
                player_moves.append(Word)

        print("The score of your word is: ", score) 
        
    
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

        if Continue_game == "c" or Continue_game == "C":
            player1_score_addition, player1_tiles, letter_pool, player1_moves =  gather_score(username1, player_num, player1_tiles, letter_pool, player1_moves)
            player1_score += player1_score_addition
        elif Continue_game == "q" or Continue_game == "Q":
            print("\nGame Over!")
            game_over = True
        else:
            print("\nInvalid Input")

        if Continue_game == "c" or Continue_game == "C":
            player_num = 2;
            #Player 2 Turn
            print("\nPlayer 2 -", username2, "it is your turn! Continue game(type 'c') or quit(type 'q')?")
            Continue_game = input() 
            print("\n")

            if Continue_game == "c" or Continue_game == "C":
                player2_score_addition, player2_tiles, letter_pool, player2_moves =  gather_score(username2, player_num, player2_tiles, letter_pool, player2_moves)
                player2_score += player2_score_addition
            elif Continue_game  == "q" or Continue_game == "Q":
                print("\nGame Over!")
                game_over = True
            else:
                print("\nInvalid Input")
    print("Player 1 Score: ", player1_score)
    print("Player 1 Moves: ", player1_moves)
    print("Player 2 Score: ", player2_score)
    print("Player 2 Moves: ", player2_moves) 


if __name__ == '__main__':
    main()
