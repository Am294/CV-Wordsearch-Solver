import pygtrie


def solve_word_search(words, puzzle):
    trie = pygtrie.CharTrie()
    for w in words:
        trie[w] = True
    
    print(trie.has_key("caca"))
    print(trie.has_subtrie("ca"))

words = ['ape', 'carton', 'wine', 'apple', 'cat', 'winner', 'care', 'design', 'carry', 'fine']
grid = [
    'ghjjwqcdsbtearxdx',
    'baaphizaexwipzbrjo',
    'lkukmbnyrsngpoapei',
    'icwehsmnzritlilbxg',
    'bazfjlqzevygeinqiz',
    'rtenrpuslqhkpffbrg',
    'rooeqrrffptkyjwkil',
    'cnnbwcareicatacirk',
    'qvzmywtgaokfjztxni',
    'ilfqnxxikyejzdmxge',
    'nmzhwiqgurosoggiuo'
]

grid = [list(g) for g in grid]


#solve_word_search(words,"")


