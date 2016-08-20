import random
import numpy
import SupervisedValidator
import json
import time
import sys

if 1 not in sys.argv or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print "Usage: python Main.py [pathToDataSet] [dataSetFormat] [iterations]"
    print "Trains the DTA using a dataset and performs a benchmark. Returns benchmark data."
    print '--------'
    print "[pathToDataSet]: file path to a dataset with training data for validation. e.g. test_sets/dates.json"
    print '[dataSetFormat]: format the dataset is in.'
    print 'Can be either GP for the format used by Bartoli et al. or DTA for the default format.'
    print 'default: DTA'
    print '[iterations]: the number of times the DTA is trained using a random excerpt of the datase.t'
    print 'Use more iterations for a more general performance indication. Use less iterations if you are in a hurry.'
    print 'default: 10'
    sys.exit(0)

data = json.loads(open(sys.argv[1]).read())
data_format = "DTA" if 2 not in sys.argv else sys.argv[3]
if data_format is not "DTA" and data_format is not "GP":
    raise "Unknown format: " + data_format

iterations = 10 if 3 not in sys.argv else int(sys.argv[3])

if data_format is "DTA":
    valid_phrases = [(phrase, True) for phrase in data["valid"]]
    invalid_phrases = [(phrase, False) for phrase in data["invalid"]]
else:


train_times = []
test_times = []
precisions = []
recalls = []
train_sizes = []
test_sizes = []

for i in range(iterations):
    random.shuffle(valid_phrases)
    random.shuffle(invalid_phrases)
    split_v, split_i = int(round(len(valid_phrases) * 0.75)), int(round(len(invalid_phrases) * 0.3))

    train_set = valid_phrases[split_v:] + invalid_phrases[split_i:]
    test_set = valid_phrases[:split_v] + invalid_phrases[:split_i]

    training_time1 = time.clock()
    clf = SupervisedValidator.Validator.from_data(train_set)
    training_time2 = time.clock()

    test_time1 = time.clock()
    prec, rec = SupervisedValidator.measure_performance(clf, test_set)
    test_time2 = time.clock()

    train_times.append(training_time2 - training_time1)
    test_times.append(test_time2 - test_time1)
    precisions.append(prec)
    recalls.append(rec)
    train_sizes.append(len(train_set))
    test_sizes.append(len(test_set))

prec, rec = numpy.mean(precisions), numpy.mean(recalls)

print("training size: " + str(numpy.mean(train_sizes)))
print("test size: " + str(numpy.mean(test_sizes)))
print("time for training: " + str(round(numpy.mean(train_times), 3)) + " s")
print("time for testing: " + str(round(numpy.mean(test_times), 3)) + " s")
print("precision: " + str(round(prec, 3)))
print("recall: " + str(round(rec, 3)))
print("f-measure: " + str(round((2 * prec * rec / prec + rec), 3)))
