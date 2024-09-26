from .ipa import *

from typing import List

type NodeT = Node

class Sound:
    value : str = ""
    ip   : bool = False
    vowel : bool
    pass

class Connection:
    strenght: int = 1
    node: NodeT

class Node:
    letter : str
    vowel  : bool
    childs : List[Connection]

    def __init__(self, letter) -> None:
        self.letter = letter
        self.vowel = letter in ['a', 'e', 'i', 'o', 'u', 'ę', 'ą', 'ó']
        self.childs = []
        pass

    def __contains__(self, b : str):
        for child in self.childs:
            if child.node.letter == b:
                return True
        return False

    def new(self, letter) -> NodeT:
        node = Node(letter)
        conn = Connection()
        conn.node = node
        self.childs.append( conn )
        return node

    def __getitem__(self, letter: str) -> NodeT:
        if letter in self:
            for child in self.childs:
                if child.node.letter == letter:
                    child.strenght += 1
                    return child.node
        return self.new(letter)

    def append(self, node: NodeT):
        conn = Connection()
        conn.node = node
        self.childs.append(conn)
        pass

    def __print__(self, depth: int) -> str:
        init = lambda: '\t' * depth
        out = ''
        for child in self.childs:
            if child.node.letter == "[END]":
                continue
            out += f'{init()}{child.node.letter}\n'
            out += child.node.__print__(depth + 1) 
        return out


    def __str__(self) -> str:
        return self.__print__(0)

    pass


REPLACE_MAP = {
    'qu': 'k',

    'ch': 'S',
    'h' : '',
    'ce': 'se',
    'ci': 'si',
    'cé': 'sé',
    'cí': 'sí',

    'c' : 'k',
    'gu': 'g',
    'ü' : 'u',
    'x' : 'ks',
    'll': 'y',

    # xs/xc => kss => ks
    'kss': 'ks',
}

VOWELS = [
    'a','á','e','é','i','í','o','ó','u','ú',
]

CONSONANTS = [
    'b','c','d','g','j','k','l','m','n','p','r','s','t','v','w','y','z',
]

def sanatize_spanish(word: str) -> str:
    new_word = word
    for k in REPLACE_MAP:
        new_word = new_word.replace(k, REPLACE_MAP[k])

    # weird conditions
    if new_word[-1] == 'y':
        new_word = new_word[:-1] + 'i'

    return new_word

STOP = [ 'p','t','k','d','g', ]
SECN = [ 'r', 'l', ]
ANYB = [ 'ñ', 'j', ]

SEMI = [ 'w', 'u', 'i', 'ú', 'í' ]


# SYLL_PSEUDO_REGEX = '(^STOP|(STOP(r|l)))?((iu)?V(iu)?)(ANYB?s)?'
def process_word(word: str) :
    equivalent = ''
    for _, letter in enumerate(word):
        if letter in VOWELS:
            equivalent += 'v'
        else:
            equivalent += 'c'

    start = 0
    triple = equivalent.find('vvv', start)
    while triple != -1:
        if word[triple] in SEMI and word[triple + 1] in VOWELS and word[triple + 2] in SEMI:
            equivalent = equivalent[:triple] + 'svs' + equivalent[triple + 3:]
        start = triple + 3
        triple = equivalent.find('vvv', start)
        
    start = 0
    double = equivalent.find('vv', start)
    while double != -1:
        if word[double] in SEMI and word[double + 1] in VOWELS:
            equivalent = equivalent[:double] + 'sv' + equivalent[double + 2:]

        if word[double] in VOWELS and word[double + 1] in SEMI:
            equivalent = equivalent[:double] + 'vs' + equivalent[double + 2:]

        start = double + 2
        double = equivalent.find('vv', start)
        pass

    roots = []
    for index, letter in enumerate(equivalent):
        if letter == 'v':
            roots.append(index)

    # expand the syllables roots into syllables
    roots = roots.reverse()


    return (word, (equivalent, roots), )

def main():
    return

if __name__ == "__main__":
    main()
