import sys
from convertPicture import grid_to_letters

if __name__ == "__main__":
    letter_grid_pth = sys.argv[1]
    words_pth = sys.argv[2]

    word_search = grid_to_letters(letter_grid_pth, True)
    words = grid_to_letters(words_pth, False)

    for w in word_search:
        print(w)
    
    print(words)

