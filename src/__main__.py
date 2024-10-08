from ipa import IPA_SYMBOLS, Word
from pprint import pprint

def main():
    from spanish import spanish_to_ipa
    words = []
    with open("data.txt", "r") as file:
        words = [line[:-1].strip(' ') for line in file.readlines()]

    for word in words:
        ipa : Word = spanish_to_ipa(word)
        print(f'{word}: {ipa}')

    return

if __name__ == "__main__":
    main()

