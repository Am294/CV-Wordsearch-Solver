import sys
import cv2
from convertPicture import grid_to_letters
from wordsearch import solve_word_search
from PIL import Image

# Change background color for diagonal
def change_background_diag(color, img, x, y, w, h, first, letter):
    y = max(0, y-10)
    outer_end = min(y+h+20, img.shape[0])
    inner_end = min(x+w, img.shape[1])
    if letter == "I":
        change1, change2 = 5, 29
    elif first:
        change1, change2 = -12, 12
    else:
        change1, change2 = -12, 12
    while  y < outer_end and x < inner_end-5:
        for i in range(x+change1, x+change2):
            if sum(img[y, i, :]) > 725:
                img[y, i, :] = color
        y += 2
        x += 1

# Changes background color for non-diagonal
def change_background(color, img, x, y, w, h):
    outer_end = min(y+h, img.shape[0])
    inner_end = min(x+w, img.shape[1])
    for i in range(y, outer_end):
        for j in range(x, inner_end):
            if sum(img[i, j, :]) > 725:
                img[i, j, :] = color

# Combines photos for the puzzle and words
def combine_photos(puzzle, words):
    images = [Image.open(x) for x in [puzzle, words]]
    widths, heights = zip(*(i.size for i in images))

    total_height = sum(heights)
    max_width = max(widths)

    for i in range(len(images)):
        if images[i].size[0] < max_width:
            images[i] = images[i].resize((max_width, images[i].size[1]))

    new_im = Image.new('RGB', (max_width, total_height))
    y_offset = 0
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]

    new_im.save('images/output/combined.PNG')

if __name__ == "__main__":
    puzzle_pth = sys.argv[1]
    words_pth = sys.argv[2]

    puzzle, puzzle_grids = grid_to_letters(puzzle_pth, True)
    words_arr, _ = grid_to_letters(words_pth, False)
    words = [''.join(w) for w in words_arr]

    
    solved_puzzle = solve_word_search(puzzle, words)

    
    img = cv2.imread(puzzle_pth)
    img = cv2.resize(img, (img.shape[1], img.shape[0] * 2), interpolation = cv2.INTER_AREA) 


    colors = [[239, 255, 0], [	57, 255, 20]]
    
   
    # Colors in characters of solved puzzle
    for i in range(len(solved_puzzle)):
        for j in range(len(solved_puzzle[0])):
            if solved_puzzle[i][j][0] != '0':
                x, y, w, h = puzzle_grids[i][j][0] - 3, puzzle_grids[i][j][1] - 3, puzzle_grids[i][j][2] + 3, puzzle_grids[i][j][3] + 3
                #cv2.imwrite(f'images/output/w{i*18 + j}.PNG', img[y:y+h, x:x+w, :])
                # Makes boxes more uniform
                if w < 10:
                    x -= 10
                elif w< 15:
                    x -= 5
                #puzzle_grids[i][j][0] = x
                change_background(colors[1], img, x, y, 25, h)

                # Connects the words
                
                if solved_puzzle[i][j][1] != "N":
                    if solved_puzzle[i][j][1] == "L":
                        x2, w2 = puzzle_grids[i][j+1][0] - 3, puzzle_grids[i][j+1][2] + 3
                        change_background(colors[1], img, x+w, y, x2-x, h)
                    elif solved_puzzle[i][j][1] == "U":
                        x2, y2 = puzzle_grids[i+1][j][1] - 3, puzzle_grids[i+1][j][1] - 3
                        
                        
                       # puzzle_grids[i][j][0] = temp_x

                        change_background(colors[1], img, x, y+h, 25, y2-y)
                    else:
                        if i == 0 or j == 0:
                            first = True
                        elif solved_puzzle[i-1][j-1][1] != "D":
                            first = True
                        else:
                            first = False
                        x2, y2 = puzzle_grids[i+1][j+1][0] - 3, puzzle_grids[i+1][j+1][1] - 3
                        change_background_diag(colors[1], img, x+w, y+h, x2-x, y2-y, first, solved_puzzle[i][j][0])
                
 
    img = cv2.resize(img, (img.shape[1], img.shape[0]//2), interpolation = cv2.INTER_AREA) 
    cv2.imwrite(f'images/output/final.PNG', img)

    combine_photos('images/output/final.PNG', words_pth)

