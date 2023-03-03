#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random

#List of all letters in scrabble
player_letters = ['E','E','E','E','E','E','E','E','E','E','E','E','A','A','A','A','A','A','A','A','A','I','I','I','I','I','I','I','I','I','O','O','O','O','O','O','O','O','N','N','N','N','N','N','R','R','R','R','R','R','T','T','T','T','T','T','L','L','L','L','S','S','S','S','U','U','U','U','D','D','D','D','G','G','G','B','B','C','C','M','M','P','P','F','F','H','H','V','V','W','W','Y','Y','K','J','X','Q','Z','_','_']
letters_in_hand = []
#letters_in_hand[7]

#Variables
lst = []
score = 0
total = 0
i = 0
count = 0

#grabs username
username: str = input("Please enter a username: ")
print("Is-", username, "-playing? If yes, type Yes, if no, type No: ")
player = input()
print("\n\n\n")

#Keep total for user playing
if player == "Yes":

    #Keeping track of user's points
    while player == "Yes":

        #Grabbing letters from the letter pool
        for randomletter in player_letters:
            while count <= 7:
                if count == 7:
                    break
                else: 
                    randomletter = random.choices(player_letters)
                    letters_in_hand.append(randomletter)
                    count = count + 1
        
        print("Here are the letters you currently have: ", letters_in_hand) 
        
        #Resetting Score
        score = 0

        #Getting the input for the word the user would like to use
        WordInput: str = input("Please Enter a valid word With the letters you received (If you have a blank tile, use an underscore in the loaction of where you'd like to use it): \n")

        #Making letters uppercase
        Word = WordInput.upper()

        #Making sure the word is within the space allowed
        if len(Word) > 15:
            print("Invalid word, must be smaller than 15 letters")
        else:
            print("\n\nYou typed the word: ", Word)

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
        
        print("The score of your word is: ", score) 

        #Gathering the total after every 'round'
        total = total + temp 
        print(username, "total score is: ", total, "\n\n")

        print("Is", username, "Still playing? If yes, type Yes. If not, type No:")
        player = input()
        print("\n\n")

elif player == "No":
    print("Don't cheat!")

else:
    print("Invalid Input")

            
