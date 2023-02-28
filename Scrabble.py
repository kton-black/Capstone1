#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Variables
lst = []
score = 0
i = 0

#Getting a valid User input
WordInput: str = input("Please Enter a valid word (If you have a blank tile, use an underscore in the loaction of where you'd like to use it): \n")

#Making letters uppercase
Word = WordInput.upper()

#Making sure the word is within the space allowed
if len(Word) > 15:
    print("Invalid word, must be smaller than 15 letters")
else:

    print("\n\n\nYou typed the word: ", Word)

    #For an i in the word
    for letter in Word:
        #Split the up the word
        lst.append(letter)

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

    print("The score of your word is: ", score)

            