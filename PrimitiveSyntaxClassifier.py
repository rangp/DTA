import collections
import itertools

import Alphabets


class Classifier:
    anchors = []
    sub_phrase_data = [] # type: List[SubPhraseData]
    valid_sub_phrases = []
    invalid_sub_phrases = []
    phrases = []

    known_alphabets = [
        Alphabets.lowercase_alphabet,
        Alphabets.uppercase_alphabet,
        Alphabets.consonants,
        Alphabets.vocals,
        Alphabets.numbers,
        Alphabets.punctuation,
    ]

    def __init__(self, anchors):
        self.anchors = anchors

    def classify(self, phrase):
        sub_phrases = []
        for anchor in self.anchors:
            split = phrase.split(anchor, 1)
            if len(split) != 2:
                return False
            phrase = split[1]
            sub_phrases.append(split[0])
        for i, sub_phrase in enumerate(sub_phrases):
            data = self.sub_phrase_data[i]
            if data.min_alphabet.difference(_char_info(sub_phrase)):
                # sub_phrase does not consist of the minimal ordered alphabet
                return False
            if data.min_length > len(sub_phrase) or data.max_length < len(sub_phrase):
                # sub_phrase is either too long or too short compared to the valid data
                return False
            for char in sub_phrase:
                # sub_phrase has characters that are not in the full alphabet
                if char not in data.full_alphabet:
                    return False
        return True

    @staticmethod
    def from_data(phrases):
        valid_phrases, invalid_phrases = set(), set()

        # split up into valid and invalid data
        for (phrase, validity) in phrases:
            if validity is True:
                valid_phrases.update([phrase])
            else:
                invalid_phrases.update([phrase])

        anchors = anchor_points(valid_phrases)[-1]
        valid_sub_phrases = [[] for t in range(len(anchors) + 1)]
        invalid_sub_phrases = [[] for t in range(len(anchors) + 1)]

        classifier = Classifier(anchors)

        # split up into sub phrases
        for i, (phrase, is_valid) in enumerate(phrases):
            forced_break = False
            for i, anchor in enumerate(anchors):
                split = phrase.split(anchor, 1)
                if len(split) != 2:
                    # item is invalid by anchor test and can be safely removed
                    invalid_phrases.remove(phrase)
                    forced_break = True
                    break
                phrase = split[1]
                valid_sub_phrases[i].append(split[0]) if is_valid else invalid_sub_phrases[i].append(split[0])
            if forced_break is False:
                valid_sub_phrases[-1].append(phrase) if is_valid else invalid_sub_phrases[-1].append(phrase)

        for valid_sub_phrase_list, invalid_sub_phrase_list in zip(valid_sub_phrases, invalid_sub_phrases):
            v_occs, required_items = _char_occurrences(valid_sub_phrase_list)
            i_occs, temp = _char_occurrences(invalid_sub_phrase_list)
            alphabets = _find_alphabets({x[-1] for x in v_occs}, {x[-1] for x in i_occs}, classifier)
            classifier.sub_phrase_data.append(
                SubPhraseData(set(required_items), alphabets,
                              len(min(valid_sub_phrase_list, key=len)),
                              len(max(valid_sub_phrase_list, key=len))))

        classifier.phrases = phrases
        classifier.valid_sub_phrases = valid_sub_phrases
        classifier.invalid_sub_phrases = invalid_sub_phrases
        return classifier


def _char_info(phrase):
    chars_in_word_map = {}
    char_list = []
    for i, char in enumerate(phrase):
        chars_in_word_map[char] = chars_in_word_map[char] + 1 if char in chars_in_word_map else 1
        char_list.append(str(chars_in_word_map[char]) + "_" + char)
    return char_list


class SubPhraseData:
    min_alphabet = set()
    full_alphabet = set()
    diagnostic_alphabets = []
    min_length = 9999999.0
    max_length = 0.0

    def __init__(self, min_alphabet, diagnostic_alphabets, min_length, max_length):
        self.min_alphabet = min_alphabet
        self.diagnostic_alphabets = diagnostic_alphabets
        self.full_alphabet = frozenset().union(*[a.members for a in diagnostic_alphabets])
        self.max_length = max_length
        self.min_length = min_length


def _all_possible_orderings(word_list, anchors):
    """
    Returns a list of all orderings of a given set of anchors
    that would work on the provided word_list
    :param word_list: list of words to fit
    :param anchors: anchors to be ordered
    :return: If no order would work, an empty list is returned. Else a list of all orderings, represented as ordered lists, is returned.
    """
    if len(anchors) == 1:
        return [anchors]

    orderings = []

    def get_key(custom):
        return custom[1]

    for word in word_list:
        indexes = []
        for anchor in anchors:
            indexC = []
            for a, x in enumerate(word):
                if x == anchor:
                    indexC.append((anchor, a))
            indexes.append(indexC)

        product, result = list(map(list, itertools.product(*indexes))), []
        for i, entry in enumerate(product):
            if len(entry) != len(set(entry)): continue
            result.append(tuple(t[0] for i, t in enumerate(sorted(entry, key=get_key))))
        if len(orderings) == 0:
            orderings = result
        else:
            orderings = [val for val in orderings if val in result]
            if len(orderings) == 0:
                return orderings
    return orderings


# ! Has to take anchors longer than one char into consideration as well
def anchor_points(inputs):
    """
    From a set of inputs generated all possible ordered lists of characters that could serve as anchor points
    :param inputs: any list of non-random words
    :return: A list of possible anchor sets
    """
    anchors = list(next(iter(inputs)))
    for current in inputs:
        new_anchors = []
        for char in current:
            if char in anchors:
                if char not in new_anchors or collections.Counter(new_anchors)[char] < \
                        collections.Counter(anchors)[char]:
                    new_anchors.append(char)
        anchors = new_anchors
    result = []
    for i in range(1, len(anchors) + 1):
        combis = itertools.combinations(anchors, i)
        for a, combi in enumerate(combis):
            result += _all_possible_orderings(inputs, combi)

    return list(set(result))


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
