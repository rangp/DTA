import random
import datetime
import SupervisedValidator
import json
import time

data = json.loads(open('test_sets/email.json').read())


valid_phrases = [(phrase, True) for phrase in data["valid"]]
random.shuffle(valid_phrases)
invalid_phrases = [(phrase, False) for phrase in data["invalid"]]
random.shuffle(invalid_phrases)
split_v, split_i = int(round(len(valid_phrases)*0.75)), int(round(len(invalid_phrases)*0.3))

train_set = valid_phrases[:split_v] + invalid_phrases[:split_i]
test_set = valid_phrases[split_v:] + invalid_phrases[split_i:]


training_time1 = time.clock()
clf = SupervisedValidator.Validator.from_data(train_set)
training_time2 = time.clock()

test_time1 = time.clock()
perf = SupervisedValidator.measure_performance(clf, test_set)
test_time2 = time.clock()

print("training size: " + str(len(train_set)))
print("test size: " + str(len(test_set)))
print("time for training: " + str(round(training_time2-training_time1*1000, 3)) + " ms")
print("time for testing: " + str(round(test_time2-test_time1*1000, 3)) + " ms")
print("precision: " + str(round(perf[0], 3)))
print("recall: " + str(round(perf[1], 3)))
print("f-measure: " + str(round((perf[1]*perf[0])/(perf[1]+perf[0]), 3)))




