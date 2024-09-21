import sys
from typing import List

type NodeT = Node

class Sound:
    value : str = ""
    ipa   : bool = False
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

def main():
    root = Node("[START]")
    end = Node("[END]")

    sylls = []
    data = "data.txt" if len(sys.argv) == 1 else sys.argv[1]
    with open(data, "r") as file:
        buf_sylls = file.readlines()
        for syll in buf_sylls:
            sylls.append(syll.replace('\n', ''))

    for syll in sylls:
        current = root
        for i in range(0, len(syll), 2):
            c = syll[i]
            if c not in current :
                current = current.new(c)
            else:
                current = current[c]

            if i + 1 < len(syll):
                current[syll[i + 1]] 
        current.append(end)

    print(root)
    pass

if __name__ == "__main__":
    main()
