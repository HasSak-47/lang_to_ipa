from ipa import *

REPLACE_MAP = {
    'qu': 'k',

    'ch': 'tś',
    'sh': 'ś',
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

    'á': 'a',
    'é': 'e',
    'í': 'i',
    'ó': 'o',
    'ú': 'u',

    'w':'gu',
}

# a e i o u
VOWELS =  { v : find_vowel(name)
    for v, name in {
        'a': 'open central', 'e': 'mid front',
        'i': 'close front', 'o': 'mid back', 'u': 'close back',
    }.items()
}
          

CONSONANTS = { c: find_consonant_symbol(name)
    for c, name in {
    'b'  : 'b',
    # 'b'  : 'β',
    'd'  : 'd',
    # 'd'  : 'ð',
    'f'  : 'f',
    'g'  : 'ɡ',
    # 'g'  : 'ɣ',
    'j'  : 'x',
    # 'y'  : 'ɟʝ',
    'k'  : 'k',
    'l'  : 'l',
    'm'  : 'm',
    # 'n'  : 'ɱ',
    'n'  : 'n',
    'ñ'  : 'ɲ',
    # 'ng' : 'ŋ',
    'p'  : 'p',
    # 'r'  : 'r',
    'r'  : 'ɾ',
    's'  : 's',
    't'  : 't',
    'v'  : 'β',
    'z'  : 'θ',
    'ś'  : 'ʃ',
    'y'  : 'ʎ',
    'y'  : 'ʝ',
    }.items()
}



def sanatize_spanish(word: str) -> str:
    new_word = word
    for k in REPLACE_MAP:
        new_word = new_word.replace(k, REPLACE_MAP[k])

    # weird conditions
    if new_word[-1] == 'y':
        new_word = new_word[:-1] + 'i'
    return new_word

def spanish_to_ipa(word: str) -> Word:
    l = []
    w = sanatize_spanish(word)
    for k in w:
        if k in CONSONANTS:
            l.append(CONSONANTS[k])
        else:
            l.append(VOWELS[k])
    return Word(l)

