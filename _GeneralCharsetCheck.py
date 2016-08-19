import SupervisedValidator

import Alphabets


class Classifier:
    validator = None  # type: SupervisedValidator.Validator
    sub_phrase_data = []  # type: List[SubPhraseData]

    known_alphabets = [
        Alphabets.lowercase_alphabet,
        Alphabets.uppercase_alphabet,
        Alphabets.consonants,
        Alphabets.vocals,
        Alphabets.numbers,
    ]

    def __init__(self, validator):
        self.validator = validator
        self.__train()

    def classify(self, phrase):
        sub_phrases = self.validator.split_into_sub_phrases(phrase)
        if len(sub_phrases) is 0:
            return False

        for i, sub_phrase in enumerate(sub_phrases):
            data = self.sub_phrase_data[i]
            if data.min_charset.difference(_char_info(sub_phrase)):
                # sub_phrase does not consist of the minimal ordered alphabet
                return False
            if data.min_length > len(sub_phrase) or data.max_length < len(sub_phrase):
                # sub_phrase is either too long or too short compared to the valid data
                return False
            for char in sub_phrase:
                # sub_phrase has characters that are not in the full alphabet
                if char not in data.full_charset:
                    return False
        return True

    def __train(self):

        for valid_sub_phrase_list, invalid_sub_phrase_list in zip(self.validator.valid_sub_phrases, self.validator.invalid_sub_phrases):
            v_occs, required_items = _char_occurrences(valid_sub_phrase_list)
            i_occs, temp = _char_occurrences(invalid_sub_phrase_list)
            alphabets = _find_alphabets({x[-1] for x in v_occs}, {x[-1] for x in i_occs}, self)
            self.sub_phrase_data.append(
                SubPhraseData(set(required_items), alphabets,
                              len(min(valid_sub_phrase_list, key=len)),
                              len(max(valid_sub_phrase_list, key=len))))


class SubPhraseData:
    min_charset = set()
    full_charset = set()
    diagnostic_charset = []
    min_length = 9999999.0
    max_length = 0.0

    def __init__(self, min_charset, diagnostic_charset, min_length, max_length):
        self.min_charset = min_charset
        self.diagnostic_charset = diagnostic_charset
        self.full_charset = frozenset().union(*[a.members for a in diagnostic_charset])
        self.max_length = max_length
        self.min_length = min_length


def _char_info(phrase):
    chars_in_word_map = {}
    char_list = []
    for i, char in enumerate(phrase):
        chars_in_word_map[char] = chars_in_word_map[char] + 1 if char in chars_in_word_map else 1
        char_list.append(str(chars_in_word_map[char]) + "_" + char)
    return char_list


def _char_occurrences(word_list):
    """
    Counts the occurrences of characters in a list of words and analyses how often
    a particular char is used
    :param word_list: list of words to analyse
    :return: A dictionary of absolute counts of usage keyed by the character and its order of appearance in each word
             and a list of characters that are common among all words
    """
    char_map, required_characters = {}, []
    for i, word in enumerate(word_list):
        chars_in_word_map = {}
        for i, char in enumerate(word):
            chars_in_word_map[char] = chars_in_word_map[char] + 1 if char in chars_in_word_map else 1
            key = str(chars_in_word_map[char]) + "_" + char
            char_map[key] = char_map[key] + 1 if key in char_map else 1
            if char_map[key] == len(word_list):
                required_characters.append(key)

    return char_map, required_characters


def _find_alphabets(valid_char_dist, invalid_char_dist, classifier):

    processed_alphabets = set()
    used_alphabets = []
    unlabeled = Alphabets.Alphabet()

    for char in valid_char_dist:
        is_in_alphabet = False
        for i, alphabet in enumerate(classifier.known_alphabets):
            if char in alphabet.members:
                is_in_alphabet = True
                if alphabet.name not in processed_alphabets:
                    used_alphabets.append(alphabet)
                processed_alphabets.update([alphabet.name])
        if not is_in_alphabet:
            unlabeled.members.update([char])

    if len(unlabeled.members) > 0:
        used_alphabets.append(unlabeled)

    chars_not_used_in_valid_phrases = set(invalid_char_dist) - set(valid_char_dist)
    for char in chars_not_used_in_valid_phrases:
        for i, alphabet in enumerate(used_alphabets):
            if char in alphabet.members:
                used_alphabets[i] = Alphabets.Alphabet(alphabet.name + " -" + char, alphabet.members - {char})

    return used_alphabets
