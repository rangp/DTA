import _GeneralCharsetCheck
import SupervisedValidator
import itertools


class Classifier:
    validator = None  # type: SupervisedValidator.Validator
    general_check = None  # type: _GeneralCharsetCheck.Classifier
    sub_phrase_map = {}

    def __init__(self, validator, general_check):
        self.validator = validator
        self.general_check = general_check
        self.__train()

    def classify(self, phrase):
        sub_phrases = self.validator.split_into_sub_phrases(phrase)
        if len(sub_phrases) is 0:
            return False

        for pos, sub_phrase in enumerate(sub_phrases):
            prev_phrases = sub_phrases[:pos]
            for i in range(1, pos + 1):
                    tmp = prev_phrases[:]
                    tmp[:-i] = [self.validator.reserved_wildcard_sequence for t in range(pos - i)]
                    key = self.validator.reserved_delimiter_sequence.join(tmp)
                    if key in self.sub_phrase_map and sub_phrase not in self.sub_phrase_map[key]:
                        return False
        return True

    def __train(self):
        for (phrase, is_valid) in self.validator.phrases:
                if is_valid:
                    sub_phrases = self.validator.split_into_sub_phrases(phrase)
                    for pos, sub_phrase in enumerate(sub_phrases):
                        prev_phrases = sub_phrases[:pos]
                        for i in range(1, pos+1):
                                tmp = prev_phrases[:]
                                tmp[:-i] = [self.validator.reserved_wildcard_sequence for t in range(pos - i)]
                                key = self.validator.reserved_delimiter_sequence.join(tmp)
                                if key in self.sub_phrase_map:
                                    self.sub_phrase_map[key].append(sub_phrase)
                                else:
                                    self.sub_phrase_map[key] = []

        sub_phrase_lengths = []
        for sp in self.validator.valid_sub_phrases:
            sub_phrase_lengths.append(float(len(set(sp))))

        for rule in list(self.sub_phrase_map.keys()):
            i = rule.count(self.validator.reserved_delimiter_sequence) + 1
            p, pc = SupervisedValidator.coverage_probability(
                sub_phrase_lengths[i],
                float(len(set(self.sub_phrase_map[rule]))),
                float(len(self.sub_phrase_map[rule])))
            if p < 0.01 or pc < 0.9:
                del self.sub_phrase_map[rule]
            else:
                self.sub_phrase_map[rule] = set(self.sub_phrase_map[rule])
