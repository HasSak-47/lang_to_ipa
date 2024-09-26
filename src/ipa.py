
from typing import Dict, List, Self


CONST_TY = [
    'bilabial', 'labiodental', 'linguolabial',
    'dental', 'alveolar', 'postalveolar',
    'retroflex', 'palatal', 'velar',
    'uvular', 'pharyngeal', 'glottal',
]

VD_V_VL = [ 'voiced', 'voiceless' ]

VOWEL_POSITION = [
    'front',
    'center',
    'back',
]

VOWEL_OPENESS = [
    'open',
    'near-open',
    'open-mid',
    'mid',
    'close-mid',
    'near-close',
    'close',
]

VOWEL_ROUNDNESS = [
    'open',
    'near-open',
    'open-mid',
    'mid',
    'close-mid',
    'near-mid',
    'close',
]

class Letter:
    def __init__(self, name: str, symbol: str) -> None:
        split = name.split(' -- alias ')
        self.name = split[0]
        self.symbol = symbol
        if len(split) == 2:
            self.alias = split[-1]
        pass

    def sonance(self) -> int:
        return 0

    def __repr__(self) -> str:
        return f'"{self.symbol}": "{self.name}"'


class Consonant(Letter):
    def __init__(self, name: str, symbol: str) -> None:
        super().__init__(name, symbol)
        
        split = self.name.split(' ')
        self.voiced = 'voiced' in self.name
        self.manner = split[-1]
        self.place = ''
        for k in split[1:-1]:
            self.place += k + ' '
        self.place = self.place.strip(' ')
        pass

    def __repr__(self) -> str:
        pad = 12 - len(self.manner)
        return f'"{self.symbol}": voiced: {self.voiced:1}  manner: "{self.manner}" {' ':{pad}} place: "{self.place}"'

class Vowel(Letter):
    def __init__(self, name: str, symbol: str) -> None:
        super().__init__(name, symbol)
        print('round' in self.name)
        print('unround' in self.name)
        print()
        defined = 'round' in self.name
        self.rounded = None
        if defined:
            self.rounded = 'unround' in self.name

        split = self.name.split(' ')
        self.height = split[0]
        self.backness = split[1]
        pass

    def __repr__(self) -> str:
        pad = 12 - len(self.height)
        k = f'"{self.symbol}": height: "{self.height}" {' ':{pad}} backness: "{self.backness}"'
        if self.rounded is not None:
            pad = 12 - len(self.backness)
            k += f' {' ':{pad}} rounded: {self.rounded:1}'

        return k

class Click(Letter):
    def __init__(self, name: str, symbol: str) -> None:
        super().__init__(name, symbol)
        pass

IPA_SYMBOLS : Dict[str, List[Letter]]= {
    "consonants":[],
    "vowels":[],
    "clicks":[],
}

def open_symbol_map():
    lines = []
    with open("ipa.txt", "r") as file:
        lines = [line[:-1] for line in file.readlines()]


    tag = ''
    for line in lines:
        if len(line) < 1 or line[0] == '#':
            continue
        if '-- tag:' in line:
            tag = line.replace('-- tag: ', '')
        else:
            parts = line.split(':')
            if len(parts) < 2:
                continue

            symbol = parts[0]
            name = parts[1][1:]
            letter : Letter | None = None
            if tag == 'consonants':
                letter = Consonant(name, symbol)
            elif tag == 'vowels':
                letter = Vowel(name, symbol)
            elif tag == 'clicks':
                letter = Click(name, symbol)
            else:
                print(f'{line} does not exists!!')
                continue
            IPA_SYMBOLS[tag].append(letter)

    pass


open_symbol_map()
