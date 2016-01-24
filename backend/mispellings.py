_key_maps = {
             'a': 'qwsz',
             'b': 'vghn ',
             'c': 'xdfv ',
             'd': 'swerfvcx',
             'e': '34rfdsw',
             'f': 'rtgvcd',
             'g': 'thbvf',
             'h': 'gyjnb',
             'i': '89okju',
             'j': 'uikmnh',
             'k': 'jil,m',
             'l': 'op;.,k',
             'm': 'njk, ',
             'n': 'bhjm ',
             'o': '90plki',
             'p': '0-[;lo',
             'q': '12wa\t',
             'r': '45tfde',
             's': 'wedxza',
             't': '56ygfr',
             'u': '78ijhy',
             'v': 'cfgb ',
             'w': '23esaq',
             'x': 'zsdc ',
             'y': '67uhgt',
             'z': 'asx',
             ' ': 'cvbnm'
}

def first_pass(word):
    lst = []
    for i in range(len(word)):
        lst.append(word[:i] + word[i+1:])
    for i in range(len(word)-1):
        c = [x for x in word.lower()]
        c[i] = word[i+1]
        c[i+1] = word[i]
        lst.append("".join(c))
    return lst

def second_pass(word):
    words = open("words.txt").read().split()
    lst = []
    for i in range(len(word)):
        for e in _key_maps[word.lower()[i]]:
            w = word.lower()[:i] + e + word.lower()[i+1:]
            if w not in words:lst.append(w)
    return lst

if __name__ == '__main__':
    print(first_pass("test"))
    print(second_pass("test"))         