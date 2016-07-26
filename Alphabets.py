# coding=utf-8
class Alphabet:
    name = None,
    members = None

    def __init__(self, name="unlabeled", members=None):
        # type: (object, object) -> object
        if members is None:
            members = set()
        self.members = members
        self.name = name


vocals = Alphabet("vocals", {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"})

standard_alphabet = Alphabet("standard",
                             {"a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F", "g", "G", "h", "H", "i",
                              "I", "j", "J", "k", "K", "l", "L", "m", "M", "n", "N", "o", "O", "p", "P", "q", "Q", "r",
                              "R", "s", "S", "t", "T", "u", "U", "v", "V", "w", "W", "x", "X", "y", "Y", "z", "Z"})

consonants = Alphabet("consonants", standard_alphabet.members - vocals.members)

lowercase_alphabet = Alphabet("lowercase",
                              {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                               "s",
                               "t", "u", "v", "w", "x", "y", "z"})

uppercase_alphabet = Alphabet("uppercase", standard_alphabet.members - lowercase_alphabet.members)

german_umlauts = Alphabet("german_umlauts", {"ä", "Ä", "ö", "Ö", "ü", "Ü", "ß"})
german_alphabet = Alphabet("german", standard_alphabet.members | german_umlauts.members)
german_lowercase_alphabet = Alphabet("lowercase_german", lowercase_alphabet.members | {"ä", "ö", "ü", "ß"})
german_uppercase_alphabet = Alphabet("lowercase_german", german_alphabet.members - german_lowercase_alphabet.members)

numbers = Alphabet("numbers", {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"})
punctuation = Alphabet("punctuation", {".", "-", ",", ";", ":", "\"", "\'", "(", ")", "/"})
