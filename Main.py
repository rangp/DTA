import random
import datetime
import PrimitiveSyntaxClassifier
import PrimitiveSemanticsClassifier

mail_addresses = ["p.rang@yellostrom.de", "adade@web.de", "patrick@enbw.com", "test1223@123.co.uk",
                  "dae2231hsdacaee@mail-v.com", "asd@wsdl.to"]
false_dates = ["206-01-03", "1993-22-07", "2014-13-11", "1993-00-10", "1994-02-31", "4002-11-07", "2002-10-50"]

true_names = ["Joelle Larger", "Verda Fiorenza", "Odessa Beachum", "Darius Fichter", "Cleopatra Pfannenstiel",
              "Johnsie Hillebrand", "Rona Wigley", "Angila Coulston", "Cynthia Paradise", "Sadie Maheux",
              "Akilah Gaetano",
              "Sherill Ryer", "Mireya Sy", "Bobbi Mosher", "Carmela Segawa", "Hugo Mcnatt", "Agustina Rossow",
              "Brant Clemente", "Rodney Edney", "Edwin Giffin", "Federico Herwig", "Matha Martin", "Merilyn Kerfoot",
              "Riley Resh", "Mellissa Vogt", "Yolanda Berlanga", "Alina Rippe", "Ka Bernabe", "Genaro Bockelman",
              "Leisa Govea", "Elisabeth Aron", "Gisele Bieber", "Rheba Sia", "Winifred Byers", "Sabra Caban",
              "Audria Messina", "Glynis Liss", "Adina Khan", "Kelle Oriley", "Rosy Ramthun", "Mariela Overfelt",
              "Nicolasa Seger", "Malik Sabine", "Shakira Trinkle", "Emiko Bee", "Tandy Warkentin", "Gertha Faas",
              "Mara Miyamoto", "Pandora Macintyre", "Marchelle Parish", "Zacharias Smith", "Igor Waschter",
              "Aveline Mueller", "Ivonne Innerlaub", "Natalischkassonamosterad Adeadanleiandsa", "Shonda Elfrink",
              "Rhiannon Sthilaire", "Stefany Gowins", "Gaylord Brayman", "Deedra Harewood", "Adelina Thompson",
              "Alexis Vanleer", "Roselee Machado", "Nereida Eldridge", "Alla Estrella", "Eloise Ricard",
              "Cleotilde Ferraro", "Tanesha Victorian", "Kathey Wiener", "Lilli Breau", "Angelena Mcleish",
              "Louvenia Elser", "Loyce Isreal", "Easter Perin", "Faustina Calfee", "Gavin Kirkham", "Lakisha Grand",
              "Malka Obrian", "Hunter Orum", "Conchita Wilton", "Latesha Kenner", "Virgina Harari", "Antione Polly",
              "Ebony Weirich", "Charise Plain", "Cecilia Rakowski", "Elinor Mass", "Debbi Trice", "Ollie Dorrell",
              "Lavina Beumer", "Catrice Correia", "Rueben Youssef", "Latoria Pernice", "Rossana Kurth",
              "Rosena Fluellen", "Olin Negus", "Avril Tanksley", "Desmond Ahumada", "Markus Blansett", "Vania Mara",
              "Aurora Parrett", "Mae Swing", "Margy Christie", "Randa Fambro", "Grayce Pattison", "Dorcas Soderberg",
              "Kelle Sanroman", "Margene Farnham", "Izetta Mathes", "Christopher Brownson", "Nguyet Denicola",
              "Bambi Ellington", "Henry Shackelford", "Kelly Colwell", "Vonnie Taplin", "Kathrine Kron",
              "Tajuana Mooring", "Krystal Bartos", "Randolph Gettings", "Maisie Wilkison", "Kecia Mettler",
              "Elisa Avey", "Cicely Pruneda", "Deedee Hartson", "Eustolia Nottage", "Douglas Ensign", "Cleveland Geer",
              "Lizzette Mccollum", "Loyce Duval", "Agatha Hampton", "Jonnie Agrawal", "Darci Ridinger", "Cari Elledge",
              "Neva Cuneo", "Billye Gilmore", "France Elvin", "Mariann Porta", "Wendolyn Gittens", "Nicole Almon",
              "Corrine Settles", "Thomasena Rabin", "Rossana Manderscheid", "Cristopher Pearman", "Tiffaney Beland",
              "Adrien Riddle", "Brittanie Dade", "Ike Bedoya", "Shanice Viramontes", "Sacha Mangione",
              "Reginald Dumont", "Caleb Matthies", "Caroyln Mcelveen", "Shanelle Fray", "Laverna Laramee",
              "Sol Banaszak",
              ]

false_names = ["Claudio P1zzaro", "EINSZweiDrei Vier", "MaddonA MIA", "ALLESSANDR4", "A-vdeds <dsae", "ei1f4l land",
               "eifel turm"]

names = [(name, True) for name in true_names] + [(name, False) for name in false_names]
dates = [(date, False) for date in false_dates] + [
    (datetime.datetime.fromtimestamp(random.randint(0, 4119604448)).date().isoformat(), True) for i in range(300)]

clf = PrimitiveSemanticsClassifier.Classifier.from_data(dates)

print(clf.classify("2016-12-10"))
