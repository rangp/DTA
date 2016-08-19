# coding=utf-8
import itertools
import collections
import _GeneralCharsetCheck
import _PositionDependentCharsetCheck
import _PredecessorDependentCharsetCheck
from scipy import special

import _PredecessorDependentSubPhraseCheck


class Validator:
    def __init__(self, delimiters):
        self.delimiters = delimiters

    delimiters = []
    valid_sub_phrases = []
    invalid_sub_phrases = []
    phrases = []
    classifiers = []

    _training_precision = 0.0
    _training_recall = 0.0

    reserved_delimiter_sequence = "~"
    reserved_wildcard_sequence = "|"

    @staticmethod
    def from_data(phrases):
        valid_phrases, invalid_phrases = set(), set()

        # split up into valid and invalid data
        for (phrase, validity) in phrases:
            if validity is True:
                valid_phrases.update([phrase])
            else:
                invalid_phrases.update([phrase])

        delimiters = max(find_delimiters(valid_phrases), key=len)
        valid_sub_phrases = [[] for t in range(len(delimiters) + 1)]
        invalid_sub_phrases = [[] for t in range(len(delimiters) + 1)]

        validator = Validator(delimiters)

        # split up into sub phrases
        for i, (phrase, is_valid) in enumerate(phrases):
            forced_break = False
            for i, anchor in enumerate(delimiters):
                split = phrase.split(anchor, 1)

                if len(split) != 2:
                    # item is invalid by anchor test and can be safely removed
                    forced_break = True
                    break
                phrase = split[1]
                valid_sub_phrases[i].append(split[0]) if is_valid else invalid_sub_phrases[i].append(split[0])
            if forced_break is False:
                valid_sub_phrases[-1].append(phrase) if is_valid else invalid_sub_phrases[-1].append(phrase)

        validator.phrases = phrases
        validator.valid_sub_phrases = valid_sub_phrases
        validator.invalid_sub_phrases = invalid_sub_phrases
        validator.find_optimal_classifiers()

        return validator

    def validate(self, phrase):
        for classifier in self.classifiers:
            if classifier.classify(phrase) is False:
                return False
        return True

    def find_optimal_classifiers(self):
        classifier = _GeneralCharsetCheck.Classifier(self)
        self.__try_add(classifier)
        self.__try_add(_PositionDependentCharsetCheck.Classifier(self, classifier))
        self.__try_add(_PredecessorDependentCharsetCheck.Classifier(self, classifier))
        self.__try_add(_PredecessorDependentSubPhraseCheck.Classifier(self, classifier))

    def __try_add(self, classifier):
        if self._training_recall is 1.0 and self._training_precision is 1.0:
            return  # no need to add another classifier since results are already optimal

        self.classifiers.append(classifier)
        precision, recall = self._measure_performance()
        # if precision loss is greater than or equal to recall gain
        if self._training_precision - precision >= recall - self._training_recall:
            self.classifiers.pop()
        else:
            self._training_recall, self._training_precision = recall, precision

    def _measure_performance(self):
        return measure_performance(self, self.phrases)

    def split_into_sub_phrases(self, phrase):
        sub_phrases = []
        for delimiter in self.delimiters:
            split = phrase.split(delimiter, 1)
            if len(split) is not 2:
                return []
            phrase = split[1]
            sub_phrases.append(split[0])
        sub_phrases.append(phrase)
        return sub_phrases


def _all_possible_orderings(word_list, delimiters):
    """
    Returns a list of all orderings of a given set of delimiters
    that would work on the provided word_list
    :param word_list: list of words to fit
    :param delimiters: delimiters to be ordered
    :return: If no order would work, an empty list is returned. Else a list of all orderings, represented as ordered lists, is returned.
    """
    if len(delimiters) == 1:
        return [delimiters]

    orderings = []

    def get_key(custom):
        return custom[1]

    for word in word_list:
        indexes = []
        for anchor in delimiters:
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
def find_delimiters(inputs):
    """
    From a set of inputs generated all possible ordered lists of characters that could serve as delimiters
    :param inputs: any list of non-random words
    :return: A list of possible delimiters
    """
    delimiters = list(next(iter(inputs)))
    for current in inputs:
        new_delimiters = []
        for char in current:
            if char in delimiters:
                if char not in new_delimiters or collections.Counter(new_delimiters)[char] < \
                        collections.Counter(delimiters)[char]:
                    new_delimiters.append(char)
        delimiters = new_delimiters
    result = []
    for i in range(1, len(delimiters) + 1):
        combis = itertools.combinations(delimiters, i)
        for a, combi in enumerate(combis):
            result += _all_possible_orderings(inputs, combi)

    return set(result)


def coverage_probability(full_amount, cover_amount, number_of_data):
    if cover_amount == full_amount:
        return 0.0, 0.0  # since the full range is already covered, the coverage possibility would be 100%
        # but as this indicates that no significant rule can be determined, 100% are treated as 0%

    p = float(0)
    for k in range(int(full_amount - 1)):
        p += ((-1) ** k) * special.binom(full_amount, full_amount - k) * ((
                                                                              full_amount - k) / full_amount) ** number_of_data

    pc = float(0)
    for k in range(int(cover_amount - 1)):
        pc += ((-1) ** k) * special.binom(cover_amount, cover_amount - k) * ((
                                                                                 cover_amount - k) / cover_amount) ** number_of_data

    return p, pc


def measure_performance(classifier, phrases):
    false_positives, false_negatives = 0, 0
    retrievals = 0
    for (phrase, is_valid) in phrases:
        classification = classifier.validate(phrase)
        if is_valid is False:
            if classification is True:
                false_positives += 1
                retrievals += 1
        if is_valid is True:
            if classification is False:
                false_negatives += 1
            else:
                retrievals += 1

    return float(retrievals - false_positives) / float(retrievals), float(retrievals - false_positives) / float(retrievals - false_positives + false_negatives)