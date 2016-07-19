import PrimitiveSyntaxClassifier

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
        return  (position_from_start + 1) / word_length


class Classifier:
    inner_classifier = None  # type: PrimitiveSyntaxClassifier.Classifier

    known_position_measures = [DefaultPositionMeasure(), ReversePositionMeasure(), RelativePositionMeasure()]
    position_maps = []

    def __init__(self, syntax_classifier: PrimitiveSyntaxClassifier.Classifier):
        self.inner_classifier = syntax_classifier

    def classify(self, phrase):
        if not self.inner_classifier.classify(phrase):
            # not valid as per primitive check
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
                        measure_dict, index = classifier.position_maps[i][measure.name], measure.extract(p, len(sub_phrase))
                        if index in measure_dict:
                            measure_dict[index].add(char)
                        else:
                            measure_dict[index] = set(char)
        return classifier
