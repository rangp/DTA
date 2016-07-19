import random
import datetime
import PrimitiveSyntaxClassifier
import PrimitiveSemanticsClassifier


mail_addresses = ["p.rang@yellostrom.de", "adade@web.de", "patrick@enbw.com", "test1223@123.co.uk",
                  "dae2231hsdacaee@mail-v.com", "asd@wsdl.to"]
false_dates = ["206-01-03", "1993-22-07", "2014-13-11", "1993-00-10", "1994-02-31", "4002-11-07", "2002-10-50"]

true_names = ["J oelle Larger", "Verda Fiorenza", "Odessa Beachum", "Darius Fichter", "Cleopatra Pfannenstiel",
              "Johnsie Hillebrand", "Rona Wigley", "Angila Coulston", "Cynthia Paradise", "Sadie Maheux",
              "Akilah Gaetano",
              "Sherill Ryer", "Mireya Sy", "Bobbi Mosher", "Carmela Segawa", "Hugo Mcnatt", "Agustina Rossow",
              "Brant Clemente", "Rodney Edney", "Edwin Giffin", "Federico Herwig", "Matha Martin", "Merilyn Kerfoot",
              "Riley Resh", "Mellissa Vogt", "Yolanda Berlanga", "Alina Rippe", "Ka Bernabe", "Genaro Bockelman",
              "Leisa Govea", "Elisabeth Aron", "Gisele Bieber", "Rheba Sia", "Winifred Byers", "Sabra Caban",
              "Audria Messina", "Glynis Liss", "Adina Khan", "Kelle Oriley", "Rosy Ramthun", "Mariela Overfelt",
              "Nicolasa Seger", "Malik Sabine", "Shakira Trinkle", "Emiko Bee", "Tandy Warkentin", "Gertha Faas",
              "Mara Miyamoto", "Pandora Macintyre", "Marchelle Parish", "Zacharias Smith", "Igor Waschter",
              "Aveline Mueller", "Ivonne Innerlaub", "Natalischkassonamosterad Adeadanleiandsa"]

false_names = ["Claudio P1zzaro", "EINSZweiDrei Vier", "MaddonA MIA", "ALLESSANDR4", "A-vdeds <dsae", "ei1f4l land",
               "eifel turm"]

names = [(name, True) for name in true_names] + [(name, False) for name in false_names]
dates = [(date, False) for date in false_dates] + [(datetime.datetime.fromtimestamp(random.randint(0, 4119604448)).date().isoformat(), True) for i in range(300)]

clf = PrimitiveSemanticsClassifier.Classifier.from_data(dates)

print(clf.classify("Jason Derulo"))
