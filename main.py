#main control file for all cipher breaker tools
import joblib

from sklearn.neighbors import NearestCentroid, KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

import ciphers
import MLRunner
import MLTrainingAnalysis
import cipherBreaker
import modelAnalyzer
import cipherPredictor

#/------------------------------------------------------------------------------------------------/
#MLRunner
'''
#KNeighbors takes almost no time to train, but takes ages to predict. Same with SVC rbf


#yTrain, xTrain, yTest, xTest = MLRunner.loadData("all")

#runML(xTrain, yTrain, xTest, yTest, NearestCentroid("euclidean"))
#runML(xTrain, yTrain, xTest, yTest, KNeighborsClassifier(n_neighbors=3, weights = "uniform"))
#runML(xTrain, yTrain, xTest, yTest, GaussianNB())
#runML(xTrain, yTrain, xTest, yTest, DecisionTreeClassifier(criterion="gini", splitter="best"))
#runML(xTrain, yTrain, xTest, yTest, RandomForestClassifier(n_estimators=5))
#runML(xTrain, yTrain, xTest, yTest, SVC(kernel="linear", C=1.0, degree = 3, gamma = "scale"))

#max run size < 1048576 before zsh: killed error. Not enough RAM
#multiRun(runs, clf(), "", 1, "compressed")
#cipher = ciphers.customCipher()
runs = [2 ** i for i in range(1, 12)] #custom run range



#extremly short run range (2^1 - 2^6)
#runs = [2 ** i for i in range(1, 6)]
#MLRunner.multiRun([1024], cipher, DecisionTreeClassifier(criterion="gini", splitter="best"), "gini,best", 1)

#short run range (2^6 - 2^11)

#runs = [2 ** i for i in range(6, 12)]

cipher = ciphers.caesarCipher()
#MLRunner.multiRun(runs, cipher, AdaBoostClassifier(DecisionTreeClassifier(criterion="gini", splitter="best"), 50), "DecisionTreeClassifier(gini,best),50", 3)
#MLRunner.multiRun(runs, cipher, QuadraticDiscriminantAnalysis(), "", 3)

#MLRunner.multiRun(runs, cipher, GaussianNB(), "", 3)


cipher = ciphers.ZacCipher()

#MLRunner.multiRun(runs, cipher, GaussianNB(), "", 3)

cipher = ciphers.uncompressedCustomCipher()

#MLRunner.multiRun(runs, cipher, GaussianNB(), "", 3)

cipher = ciphers.customCipher()

#MLRunner.multiRun(runs, cipher, GaussianNB(), "", 3)



#SVC Runs (they take a long time)
cipher = ciphers.caesarCipher()


cipher = ciphers.ZacCipher()


cipher = ciphers.customCipher()


cipher = ciphers.uncompressedCustomCipher()



#medium run range (2^12 - 2^17)
runs = [2 ** i for i in range(12, 18)]


#log run range (2^18 - 2^20)
runs = [2 ** i for i in range(18, 20)]


runs = [2 ** i for i in range(6, 10)]

#exceptions / long run time sets

'''
#/------------------------------------------------------------------------------------------------/
#Result Analysis
'''
cipherName = "caesarCipher" #uncompressedCustomCipher customCipher ZacCipher caesarCipher
#MLTrainingAnalysis.compareClassifierParameters(cipherName, "DecisionTreeClassifier", [], "score")
#MLTrainingAnalysis.compareClassifierParameters(cipherName, "GaussianNB", [], "score")
#MLTrainingAnalysis.compareClassifierParameters(cipherName, "KNeighborsClassifier", [], "score")
#MLTrainingAnalysis.compareClassifierParameters(cipherName, "NearestCentroid", [], "score")
#MLTrainingAnalysis.compareClassifierParameters(cipherName, "RandomForestClassifier", [], "score")
#MLTrainingAnalysis.compareClassifierParameters(cipherName, "SVC", [], "score")

#MLTrainingAnalysis.compareClassifiers("caesarCipher", ["DecisionTreeClassifier-entropy,random", "SVC-linear,1.0,3,scale"], "score", "all", "compressed")

MLTrainingAnalysis.graph(classifiers=["RandomForestClassifier"])
'''

#/------------------------------------------------------------------------------------------------/
#Cipher Breaker Trainer
'''
trainingDataToLetterRatio = 512

cipher = ciphers.ZacCipher()
cipherBreaker.trainClf(cipher, DecisionTreeClassifier(), trainingDataToLetterRatio)

'''

#/------------------------------------------------------------------------------------------------/
#Cipher Breaker
'''
charClassifier = joblib.load(f"./CCCs/cipherCharacterClassifier.pkl")
decryptUserMessages(cipher, charClassifier)
'''

#/------------------------------------------------------------------------------------------------/
#Model Analyzer
'''
numTests = 5000 #number of times each character is tested for accuracy
charClassifier = joblib.load("./CCCs/cipherCharacterClassifier.pkl")
#charClassifier = joblib.load(f"./CCCs/saved/clf-1.pkl")

analysis = modelAnalyzer.analyze(ciphers.caesarCipher(), charClassifier, numTests, 0.0)
modelAnalyzer.plotAnalysis(ciphers.caesarCipher(), analysis)
'''

#/------------------------------------------------------------------------------------------------/
#Breaker Predictor
#'''
print("Loading Model...")
#clf = joblib.load("./CCCs/cipherCharacterClassifier.pkl")
clf = charClassifier = joblib.load(f"./CCCs/saved/uncompressed/clf-3.pkl")
cipher = ciphers.uncompressedCustomCipher()

cipherPredictor.predictUserInput(cipher, clf, includePredictedTextAsWords = False) #third option has to be true if orignal text contains non-words or unknown words
#'''