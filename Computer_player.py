
import itertools
import random


alphabet = 'abcdefghijklmnopqrstuvwxyz'


def computer_player(board_array, letters_in_hand):
    #replace any '_' in letters_in_hand with a random vowel
    letters_in_hand = [random.choice(['a', 'e', 'i', 'o', 'u']) if letter == '_' else letter for letter in letters_in_hand]

    #initialize a dictionary to store the words for each letter of the alphabet
    alphabet_words = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        alphabet_words[letter] = []

    #iterate through each letter in the alphabet and find all possible words
    #basically is adds one letter at a time to the letters_in_hand, sees what words it can make with it and adds those words to a dictionary for that letter
    #then it removes that letter from the letters_in_hand and moves on to the next one
    #for horizontal and vertical plays later, it iterates through all letters again
    #if finds where that letter is on the board and trys to make sure it can place words from that letters dictionary
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        words_for_letter = []
        letters_in_hand.append(letter)
        for length in range(2, len(letters_in_hand) + 1):
            for tiles in itertools.permutations(letters_in_hand, length):
                word = ''.join(tiles)
                if valid_word(word):
                    words_for_letter.append(word)
        letters_in_hand.pop()
        alphabet_words[letter] = words_for_letter
    

    possible_plays = []
    for letter in alphabet:
        for i in range(len(board_array)):
            for j in range(len(board_array[i])):
                if board_array[i][j] != letter:
                    continue

                # check for valid horizontal play
                #checks 7 left and 7 right as an overarching check for all cases
                left = max(0, j-7)
                right = min(len(board_array[i])-1, j+7)
                if board_array[i][left-1] != '.' or board_array[i][right+1] != '.':
                    continue
                is_valid_play = True
                #checks above and below of the same range to make sure its empty
                for k in range(left, right+1):
                    if (i > 0 and board_array[i-1][k] != '.') or (i < len(board_array)-1 and board_array[i+1][k] != '.'):
                        is_valid_play = False
                        break
                if not is_valid_play:
                    continue
                for word in alphabet_words[letter]:
                    if word not in words_for_letter:
                        continue
                    #finding the positions of each letter to be placed on the board
                    for idx in range(len(word)):
                        if word[idx] == letter and (j-idx < left or j-idx > right):
                            positions = [(letter, i, j)]
                            for k in range(1, len(word)):
                                if j-idx+k < left or j-idx+k > right:
                                    break
                                positions.append((word[k], i, j-idx+k))
                            #removes the letter already on the board from the positions of tiles to be placed
                            if len(positions) == len(word):
                                for pos_idx, pos in enumerate(positions):
                                    if pos[0] == letter and pos_idx != 0:
                                        positions.pop(pos_idx)
                                        break
                                possible_plays.append(positions)



                # check for valid vertical play
                #checks 7 up and 7 down as an overarching check for all cases
                top = max(0, i-7)
                bottom = min(len(board_array)-1, i+7)
                if board_array[top-1][j] != '.' or board_array[bottom+1][j] != '.':
                    continue
                is_valid_play = True
                #checks right and left of the same range to make sure its empty
                for k in range(top, bottom+1):
                    if (j > 0 and board_array[k][j-1] != '.') or (j < len(board_array[i])-1 and board_array[k][j+1] != '.'):
                        is_valid_play = False
                        break
                if not is_valid_play:
                    continue
                letter = board_array[i][j]
                for word in alphabet_words[letter]:
                    if word not in words_for_letter:
                        continue
                    #finding the positions of each letter to be placed on the board
                    for idx in range(len(word)):
                        if word[idx] == letter and (i-idx < top or i-idx > bottom):
                            positions = [(letter, i, j)]
                            for k in range(1, len(word)):
                                if i-idx+k < top or i-idx+k > bottom:
                                    break
                                positions.append((word[k], i-idx+k, j))
                            #removes the letter already on the board from the positions of tiles to be placed
                            if len(positions) == len(word):
                                for pos_idx, pos in enumerate(positions):
                                    if pos[0] == letter and pos_idx != 0:
                                        positions.pop(pos_idx)
                                        break
                                possible_plays.append(positions)

    #If there are no possible plays, return None
    if not possible_plays:
        return None

    #Randomly select one of the possible plays and return it
    selected_play = random.choice(possible_plays)
    return selected_play
