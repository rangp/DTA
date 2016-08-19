import SupervisedValidator
import _GeneralCharsetCheck

class DefaultPositionMeasure:
    def __init__(self):
        pass

    name = "from_start"

    def extract(self, position_from_start, word_length):
        return position_from_start


class ReversePositionMeasure:
    def __init__(self):
        pass

    name = "from_end"

    def extract(self, position_from_start, word_length):
        return word_length - (position_from_start + 1)


class RelativePositionMeasure:
    def __init__(self):
        pass

    name = "relative"

    def extract(self, position_from_start, word_length):
        return float(position_from_start + 1) / float(word_length)


class Classifier:
    validator = None  # type: SupervisedValidator.Validator
    known_position_measures = [DefaultPositionMeasure(), ReversePositionMeasure(), RelativePositionMeasure()]
    position_maps = []
    general_check = None  # type: _GeneralCharsetCheck.Classifier

    def __init__(self, validator, general_check):
        self.validator = validator
        self.general_check = general_check

        self.__train()

    def classify(self, phrase):
        sub_phrases = self.validator.split_into_sub_phrases(phrase)
        if len(sub_phrases) is 0:
            return False

        for i, sub_phrase in enumerate(sub_phrases):
            for measure in self.known_position_measures:
                for pos, char in enumerate(sub_phrase):
                    if char not in self.position_maps[i][measure.name][measure.extract(pos, len(sub_phrase))]["chars"]:
                        # false by position rules
                        return False

        return True

    def __train(self):
        for i, sub_phrase_list in enumerate(self.validator.valid_sub_phrases):
            self.position_maps.append({m.name: {} for m in self.known_position_measures})
            for sub_phrase in sub_phrase_list:
                for p, char in enumerate(sub_phrase):
                    for measure in self.known_position_measures:
                        measure_dict, index = self.position_maps[i][measure.name], measure.extract(p, len(
                            sub_phrase))
                        if index in measure_dict:
                            measure_dict[index]["chars"].add(char)
                            measure_dict[index]["data_amount"] += 1
                        else:
                            measure_dict[index] = {"chars": set(char), "data_amount": 1}

        for i, map in enumerate(self.position_maps):
            for measure, items in map.items():
                for pos, info in items.items():
                    p, pc = SupervisedValidator.coverage_probability(float(len(self.general_check.sub_phrase_data[i].full_charset)),
                                                 float(len(info["chars"])),
                                                 float(info["data_amount"]))
                    if p < 0.01 or pc < 0.9:
                        info["chars"] = self.general_check.sub_phrase_data[i].full_charset



