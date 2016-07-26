import PrimitiveSyntaxClassifier
from scipy import special
from decimal import Decimal

class DefaultPositionMeasure:
    name = "from_start"

    def extract(self, position_from_start, word_length):
        return position_from_start


class ReversePositionMeasure:
    name = "from_end"

    def extract(self, position_from_start, word_length):
        return word_length - (position_from_start + 1)


class RelativePositionMeasure:
    name = "relative"

    def extract(self, position_from_start, word_length):
        return float(position_from_start + 1) / float(word_length)


class Classifier:
    inner_classifier = None  # type: PrimitiveSyntaxClassifier.Classifier

    known_position_measures = [DefaultPositionMeasure(), ReversePositionMeasure(), RelativePositionMeasure()]
    position_maps = []

    def __init__(self, syntax_classifier):
        self.inner_classifier = syntax_classifier

    def classify(self, phrase):
        if not self.inner_classifier.classify(phrase):
            # not valid as per primitive check
            return False

        sub_phrases = []
        for anchor in self.inner_classifier.anchors:
            split = phrase.split(anchor, 1)
            phrase = split[1]
            sub_phrases.append(split[0])
        sub_phrases.append(phrase)
        for i, sub_phrase in enumerate(sub_phrases):
            for measure in self.known_position_measures:
                for pos, char in enumerate(sub_phrase):
                    if char not in self.position_maps[i][measure.name][measure.extract(pos, len(sub_phrase))]["chars"]:
                        # false by position rules
                        return False

        return True

    @staticmethod
    def from_data(phrases):
        syntax_classifier = PrimitiveSyntaxClassifier.Classifier.from_data(phrases)
        classifier = Classifier(syntax_classifier)

        for i, sub_phrase_list in enumerate(syntax_classifier.valid_sub_phrases):
            classifier.position_maps.append({m.name: {} for m in classifier.known_position_measures})
            for sub_phrase in sub_phrase_list:
                for p, char in enumerate(sub_phrase):
                    for measure in classifier.known_position_measures:
                        measure_dict, index = classifier.position_maps[i][measure.name], measure.extract(p, len(
                            sub_phrase))
                        if index in measure_dict:
                            measure_dict[index]["chars"].add(char)
                            measure_dict[index]["data_amount"] += 1
                        else:
                            measure_dict[index] = {"chars": set(char), "data_amount": 1}

        for i, map in enumerate(classifier.position_maps):
            for measure, items in map.items():
                for pos, info in items.items():
                    p, pc = coverage_probability(float(len(syntax_classifier.sub_phrase_data[i].full_alphabet)), float(len(info["chars"])),
                                             float(info["data_amount"]))
                    if p < 0.01 or pc < 0.9:
                        info["chars"] = syntax_classifier.sub_phrase_data[i].full_alphabet

        return classifier


def coverage_probability(full_amount, cover_amount, number_of_data):
    p = float(0)
    for k in range(int(full_amount - 1)):
        p += ((-1) ** k) * special.binom(full_amount, full_amount - k) * ((full_amount - k)/ full_amount) ** number_of_data

    pc = float(0)
    for k in range(int(cover_amount - 1)):
        pc += ((-1) ** k) * special.binom(cover_amount, cover_amount - k) * ((cover_amount - k)/cover_amount) ** number_of_data

    return p, pc
