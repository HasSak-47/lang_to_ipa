
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

def open_symbol_map():
    lines = []
    with open("ipa.txt", "r") as file:
        lines = [line[:-1] for line in file.readlines()]

    print(lines)
    pass

IPA_SYMBOLS = []
