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


