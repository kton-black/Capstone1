#!/usr/bin/python3
# -*- coding: utf-8 -*-


def valid_word(input_word):
    #Checks the length of the input word
    word_length = len(input_word)

    #Creates a file name according to word length
    word_file = 'dictionaryfiles/' + str(word_length) + 'letterwords.txt'

    #Open and read only the file that matches the word length
    with open(word_file, 'r') as file:
        words = file.read().splitlines()

    #Checks if the input word matches a word in the file
    #Returns valid if the word is found in the text file
    #If the word is not found in the text file, prints invalid word
    if input_word in words:
        #Use bool values to return whether true/valid or false/invalid
        return True
    else:
        return False



#Delete later, just the testing functionality for the valid word file
#DELETE
while True:
    input_word = input('Enter an UPPERCASE word to check (type "quit" to exit): ')

    if input_word == 'quit':
        break

    result = valid_word(input_word)

    if result:
        print('Valid Scrabble word')
    else:
        print('Invalid Scrabble word')
