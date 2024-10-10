from typing import Dict, List, Self

CONSONANT_PLACE = [
    'bilabial', 'labiodental', 'linguolabial',
    'dental', 'alveolar', 'postalveolar',
    'retroflex', 'palatal', 'velar', 'uvular', 'pharyngeal', 'glottal',
]

CONSONANT_MANNER = [
    'nasal',
    'plosive',
    'fricative',
    'affricate',
    'approximant',
    'tap',
    'trill',
    'lateral-fricative',
    'lateral-approximant',
    'lateral-tap',
    # other
    'implosive',
]


CONSONANT_VD_V_VL = [ 'voiced', 'voiceless' ]

VOWEL_BACKNESS = [
    'front',
    'central',
    'back',
]

VOWEL_HEIGHT= [
    'open',
    'near-open',
    'open-mid',
    'mid',
    'close-mid',
    'near-close',
    'close',
]

VOWEL_ROUNDNESS = [
    'undefined',
    'unrounded',
    'rounded',
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
        voiced = 'voiced' if 'voiced' in self.name else 'voiceless'
        manner = split[-1]
        place = ''
        for k in split[1:-1]:
            place += k + ' '
        place = place.strip(' ')

        self.voiced = CONSONANT_VD_V_VL.index(voiced)
        self.manner = CONSONANT_MANNER.index(manner)
        self.place  = CONSONANT_PLACE.index(place)
        pass

    def sonance(self) -> int:
        if self.manner == 'lateral':
            return 5
        if self.manner == 'tap':
            return 5
        if self.manner == 'nasal':
            return 4
        if self.manner == 'fricatives':
            return 3
        if self.manner == 'affricate':
            return 2
        if self.manner == 'plosive':
            return 1
        return 0

    def __repr__(self) -> str:
        voiced = CONSONANT_VD_V_VL[self.voiced]
        manner = CONSONANT_MANNER[self.manner]
        place  = CONSONANT_PLACE[self.place]
        return f'{self.symbol}: {voiced} {place} {manner}'

    def __lt__(self, other: Self) -> bool:
        if self.place == other.place:
            if self.manner  == other.manner:
                return self.voiced < other.voiced
            return self.manner < other.manner
        return self.place < other.place

class Vowel(Letter):
    def __init__(self, name: str, symbol: str) -> None:
        super().__init__(name, symbol)
        rounded = ''
        if 'rounded' in self.name and 'unrounded' in self.name:
            rounded = 'rounded'
        elif 'rounded' in self.name and 'unrounded' not in self.name:
            rounded = 'rounded'
        else:
            rounded = 'undefined'

        split = self.name.split(' ')
        height = split[0]
        backness = split[1]

        self.rounded  = VOWEL_ROUNDNESS.index(rounded)
        self.height   = VOWEL_HEIGHT.index(height)
        self.backness = VOWEL_BACKNESS.index(backness)
        pass

    def sonance(self) -> int:
        return 6

    def __repr__(self) -> str:
        # pad = 12 - len(self.height) 
        height =VOWEL_HEIGHT[self.height]
        backness =VOWEL_BACKNESS[self.backness]
        rounded =VOWEL_ROUNDNESS[self.rounded]
        k = f'{self.symbol}: {height} {backness}'
        if rounded != 'undefined':
            k += ' ' + rounded

        return k

    def __lt__(self, other: Self) -> bool:
        if self.height == other.height:
            if self.backness == other.backness:
                return self.rounded < self.rounded
            return self.backness < self.backness

        return self.height < other.height

class Click(Letter):
    def __init__(self, name: str, symbol: str) -> None:
        super().__init__(name, symbol)
        pass

IPA_SYMBOLS : Dict[str, List[Letter]]= {
    "consonants": [],
    "vowels"    : [],
    "clicks"    : [],
}

def find_vowel(name: str):
    va = Vowel(name, '')
    closest = None
    for v in IPA_SYMBOLS['vowels']:
        if type(v) != Vowel:
            raise RuntimeError('non vowel in vowel dict')
        if va.height == v.height and va.backness == v.backness:
            closest = v
            break
    return closest

def find_consonant(name: str):
    va = Consonant(name, '')
    closest = None
    for v in IPA_SYMBOLS['vowels']:
        if type(v) != Consonant:
            raise RuntimeError('non vowel in vowel dict')
        if v.place == va.place and v.manner == va.manner and v.voiced == va.voiced:
            closest = v
            break
    return closest

def find_consonant_symbol(symbol: str):
    for v in IPA_SYMBOLS['consonants']:
        if type(v) != Consonant:
            raise RuntimeError('non vowel in vowel dict')
        if v.symbol == symbol:
            return v
    return None

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
                continue
            IPA_SYMBOLS[tag].append(letter)

    pass

open_symbol_map()

def save_symbol_map():
    with open('ipa2.txt', 'w+') as file:
        file.write('-- tag: consonants\n');
        IPA_SYMBOLS["consonants"].sort() # pyright: ignore
        for cons in IPA_SYMBOLS["consonants"]:
            if type(cons) != Consonant:
                continue
            file.write(f'{cons}\n')

        file.write('-- tag: vowels\n');
        IPA_SYMBOLS["vowels"].sort() # pyright: ignore
        for vowel in IPA_SYMBOLS["vowels"]:
            if type(vowel) != Vowel:
                continue
            file.write(f'{vowel}\n')
    pass

save_symbol_map()

class Word:
    def __init__(self, word: List[Letter]) -> None:
        self.word = word
        pass

    def to_sonority(self) -> List[int]:
        ls = []
        for s in self.word:
            ls.append(s.sonance())

        return ls

    def syllablelize(self)  -> List[Self]:
        syllables = []
        sonance : List[int] = []
        for letter in self.word:
            sonance.append(letter.sonance())

        prev1 = None
        prev2 = None
        currn = None

        for index, son in enumerate(sonance):
            prev2 = prev1
            prev1 = currn
            currn = son

            d1 = 0
            if prev2 is None or prev1 is None:
                continue

            if prev2 < prev1 and currn < prev1:
                pass

            pass




        print(f'{syllables}')


        return syllables

    def __repr__(self) -> str:
        s = ''
        for letter in self.word:
            s += letter.symbol

        return s
