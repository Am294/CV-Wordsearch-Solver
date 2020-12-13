import sys
import cv2
from convertPicture import grid_to_letters
from wordsearch import solve_word_search

def change_background(color, img, x, y, w, h):
    for i in range(y,y+h):
        for j in range(x, x+h):
            if sum(img[i, j, :]) == sum([255,255,255]) and sum([255,255,255]) > 300:
                img[i, j, :] = color

if __name__ == "__main__":
    puzzle_pth = sys.argv[1]
    words_pth = sys.argv[2]

    puzzle, puzzle_grids = grid_to_letters(puzzle_pth, True)
    words, _ = grid_to_letters(words_pth, False)

    solved_puzzle = solve_word_search(puzzle, words)

    for s in solved_puzzle:
        print(s)
    img = cv2.imread(puzzle_pth)

    #print(img.shape)
    #img = cv2.resize(img, (img.shape[1], img.shape[0]), interpolation = cv2.INTER_AREA) 
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #print(gray.shape)
    #cv2.imwrite('zzz.PNG', gray[471:471+18, 740:740+18])

    count = 0
    for i in range(len(solved_puzzle)):
        for j in range(len(solved_puzzle[0])):
            if solved_puzzle[i][j] != '0':
                print(i,j, puzzle[i][j])
                x, y, w, h = puzzle_grids[i][j][0], puzzle_grids[i][j][1], puzzle_grids[i][j][2], puzzle_grids[i][j][3]
                cv2.imwrite(f'images/output/w{i*18 + j}.PNG', img[y:y+h, x:x+h, :])
                change_background([239, 255, 0], img, x, y, w, h)
    

   
    
    cv2.imwrite(f'zzz.PNG', img)


    

