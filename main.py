import sys
import cv2
from convertPicture import grid_to_letters
from wordsearch import solve_word_search

def change_background(color, img, x, y, w, h):
    outer_end = min(y+h, img.shape[0])
    inner_end = min(x+w, img.shape[1])
    for i in range(y, outer_end):
        for j in range(x, inner_end):
            if sum(img[i, j, :]) > 750:
                img[i, j, :] = color

if __name__ == "__main__":
    puzzle_pth = sys.argv[1]
    words_pth = sys.argv[2]

    puzzle, puzzle_grids = grid_to_letters(puzzle_pth, True)
    words_arr, _ = grid_to_letters(words_pth, False)
    
    words = [''.join(w) for w in words_arr]
    
    solved_puzzle = solve_word_search(puzzle, words)


    img = cv2.imread(puzzle_pth)
    img = cv2.resize(img, (img.shape[1], img.shape[0] * 2), interpolation = cv2.INTER_AREA) 
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #print(gray.shape)
    #cv2.imwrite('zzz.PNG', gray[471:471+18, 740:740+18])

    
    for i in range(len(solved_puzzle)):
        for j in range(len(solved_puzzle[0])):
            if solved_puzzle[i][j] != '0':
                print(i,j)
                x, y, w, h = puzzle_grids[i][j][0] - 3, puzzle_grids[i][j][1] - 3, puzzle_grids[i][j][2] + 3, puzzle_grids[i][j][3] + 3
                #cv2.imwrite(f'images/output/w{i*18 + j}.PNG', img[y:y+h, x:x+w, :])
                change_background([239, 255, 0], img, x, y, w, h)

 
    cv2.imwrite(f'zzz.PNG', img)



    # Other puzzles do not look very hot right now
    # Look into the w2 one and see what is happening
    # Something is getting screwed up in the order
    # Idea iterate once and create the rows myself by deciding if the y is within 10 of last
    # Then iterate second time and actually analyze the images
    # It seems that if the height difference is more then 1 it starts a new "row"
    # So for the first round I will up my grids in a row then sort by x since that should line up with grid

    # Do that later
    # In Order To Fill In The Gaps For WordSearch I will have each node check up, left, and up left
    # If one of those things are also filled in fill in area in between

