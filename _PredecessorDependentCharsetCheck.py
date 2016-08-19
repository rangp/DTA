import _GeneralCharsetCheck
import SupervisedValidator


class Classifier:
    validator = None  # type: SupervisedValidator.Validator
    general_check = None  # type: _GeneralCharsetCheck.Classifier
    sub_phrase_function_maps = []
    sub_phrase_position_function_maps = []

    def __init__(self, validator, general_check):
        self.validator = validator
        self.general_check = general_check
        self.__train()

    def classify(self, phrase):
        sub_phrases = self.validator.split_into_sub_phrases(phrase)
        if len(sub_phrases) is 0:
            return False

        for i, sub_phrase in enumerate(sub_phrases):
            pred_map = self.sub_phrase_function_maps[i]
            pred_pos_map = self.sub_phrase_position_function_maps[i]
            for pos, char in enumerate(sub_phrase):
                prev_pos = pos - 1
                while prev_pos >= 0:
                    key = sub_phrase[prev_pos: pos]
                    if key in pred_map and char not in pred_map[key]:
                        return False
                    key = key + self.validator.reserved_delimiter_sequence + str(prev_pos)
                    if key in pred_pos_map and char not in pred_pos_map[key]:
                        return False
                    prev_pos -= 1
        return True

    def __train(self):
        for i, sub_phrase_list in enumerate(self.validator.valid_sub_phrases):
            pred_map = {}
            pred_pos_map = {}
            for sub_phrase in sub_phrase_list:
                for pos, char in enumerate(sub_phrase):
                    prev_pos = pos - 1
                    while prev_pos >= 0:
                        key = sub_phrase[prev_pos: pos]
                        if key in pred_map:
                            pred_map[key].append(char)
                        else:
                            pred_map[key] = [char]

                        key = key + self.validator.reserved_delimiter_sequence + str(prev_pos)
                        if key in pred_pos_map:
                            pred_pos_map[key].append(char)
                        else:
                            pred_pos_map[key] = [char]

                        prev_pos -= 1

            self._check_coverage_for_map(pred_map, i)
            self.sub_phrase_function_maps.append(pred_map)
            self._check_coverage_for_map(pred_pos_map, i)
            self.sub_phrase_position_function_maps.append(pred_pos_map)

    def _check_coverage_for_map(self, rule_map, i):
        for rule in rule_map.keys():
            p, pc = SupervisedValidator.coverage_probability(
                float(len(self.general_check.sub_phrase_data[i].full_charset)),
                float(len(set(rule_map[rule]))),
                float(len(rule_map[rule])))
            if p < 0.01 or pc < 0.9:
                del rule_map[rule]
            else:
                rule_map[rule] = set(rule_map[rule])