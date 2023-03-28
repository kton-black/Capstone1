# the 10x10 letter array
letters = [
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', 't', 'a', 'c', '-', '-', '-', '-'],
    ['-', '-', '-', '-', 'c', 'a', 't', '-', '-', '-'],
    ['-', '-', '-', 'c', 'a', 't', 'a', '-', '-', '-'],
    ['-', '-', '-', '-', 'b', '-', 'c', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
]

# the list of words to search for
word_list = ['cat', 'act', 'cab']

# function to search for words in the grid
def search_words(grid, words):
    matches = {}
    found_words = []
    rows = len(grid)
    cols = len(grid[0])

    # search left to right
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != '-':
                # search horizontally
                h_word = ''
                for k in range(j, cols):
                    if grid[i][k] == '-':
                        break
                    h_word += grid[i][k]
                    if h_word in words:
                        if h_word in matches:
                            matches[h_word] += 1
                        else:
                            matches[h_word] = 1
                        found_words.append(h_word)

                # search vertically
                v_word = ''
                for k in range(i, rows):
                    if grid[k][j] == '-':
                        break
                    v_word += grid[k][j]
                    if v_word in words:
                        if v_word in matches:
                            matches[v_word] += 1
                        else:
                            matches[v_word] = 1
                        found_words.append(v_word)

    return matches, found_words

# main function
def main():
    num_matches, found_words = search_words(letters, word_list)
    print(f'Found {len(found_words)} matches:')
    for word in set(found_words):
        print(f'{word} was found {num_matches[word]} times.')

# call the main function
if __name__ == '__main__':
    main()
