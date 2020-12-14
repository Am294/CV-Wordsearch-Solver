import pygtrie
import json

'''
print(trie.has_key("caca"))
print(trie.has_subtrie("ap"))

Rules of wordsearch:
    Only left right and diagonal words
    Words cannot be backwards
    Words cannot share letters
'''

def search_word(trie, copy, puzzle, x, y, word, state):
    if y < 0 or x < 0 or y >= len(puzzle) or x >= len(puzzle[0]):
        return False

    if copy[y][x][0] != '0':
        return False
    

    copy[y][x][0] = puzzle[y][x]

    if trie.has_key(word + puzzle[y][x]):
        #print(word + puzzle[y][x])
        return True
    
    if not trie.has_subtrie(word + puzzle[y][x]):
        copy[y][x][0] = '0'
        return False

    # Vertical
    if state == "n" or state == "v":
        ret = search_word(trie, copy, puzzle, x, y+1, word + puzzle[y][x], "v")
        if ret:
            copy[y][x][1] = 'U'
            return True

    #Horizontal
    if state == "n" or state == "h":
        ret = search_word(trie, copy, puzzle, x+1, y, word + puzzle[y][x], "h")
        if ret:
            copy[y][x][1] = 'L'
            return True
    
    # Diag 1
    if state == "n" or state == "d1":
        ret = search_word(trie, copy, puzzle, x+1, y+1, word + puzzle[y][x], "d1")
        if ret:
            copy[y][x][1] = 'D'
            return True
        ret = search_word(trie, copy, puzzle, x-1, y-1, word + puzzle[y][x], "d1")
        if ret:
            copy[y][x][1] = 'D'
            return True
    
    # Diag 2
    if state == "n" or state == "d2":
        ret = search_word(trie, copy, puzzle, x+1, y-1, word + puzzle[y][x], "d2")
        if ret:
            copy[y][x][1] = 'D'
            return True
        
        ret = search_word(trie, copy, puzzle, x-1, y+1, word + puzzle[y][x], "d2")
        if ret:
            copy[y][x][1] = 'D'
            return True
    
    
    

    copy[y][x][0] = '0'
    copy[y][x][1] = 'N'
    return False
    


def solve_word_search(puzzle, words):
    copy = [[['0', 'N'] for i in range(len(puzzle[0]))] for j in range(len(puzzle))]
    trie = pygtrie.CharTrie()
    for w in words:
        trie[w] = True
    
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if trie.has_subtrie(puzzle[y][x]):
                out = search_word(trie, copy, puzzle, x, y, "", "n")

    return copy
            
    
'''
words = ['ape', 'carton', 'wine', 'apple', 'cat', 'winner', 'care', 'design', 'carry', 'fine']
grid = [
    'ghjjwqcdsbtearxdxh',
    'baaphizaexwipzbrjo',
    'lkukmbnyrsngpoapei',
    'icwehsmnzritlilbxg',
    'bazfjlqzevygeinqiz',
    'armioynjmrwzngqkiy',
    'rtenrpuslqhkpffbrg',
    'rooeqrrffptkyjwkil',
    'cnnbwcareicatacirk',
    'qvzmywtgaokfjztxni',
    'ilfqnxxikyejzdmxge',
    'nmzhwiqgurosoggiuo'
]


grid = [list(g) for g in grid]
for g in grid:
    print(g)

solve_word_search(words,grid)
'''

