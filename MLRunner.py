import json
import time
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import ciphers #for testing
import util
import MLDC


def saveRun(encryptorName, clfname, label, score, trainingTime, trainingDataToLetterRatio):
	'''
	Saves a run to the correct classifier results json file and updates the text file to display the new data

	Parameters:
		name (str): classifier name
		label (str): dtype-dataFormat-parameters
		score (float): run score
		trainingTime (float): run training time
		trainingDataToLetterRatio: training data to letter ratio of the run
	'''
	trainingDataToLetterRatio = str(round(trainingDataToLetterRatio))
	trainingTime = round(trainingTime, 2)
	score = round(score, 3)

	#open files
	jsonFile = open(f"./testResults/{encryptorName}/jsonFiles/{clfname}.json", "r")
	textFile = open(f"./testResults/{encryptorName}/textFiles/{clfname}.txt", "w")

	#load json file and close
	currentRuns = json.load(jsonFile)
	jsonFile.close()

	#add run data to the currentRuns dict
	if label in currentRuns:
		if trainingDataToLetterRatio in currentRuns[label]:
			currentRuns[label][trainingDataToLetterRatio].append([score, trainingTime])
		else:
			currentRuns[label][trainingDataToLetterRatio] = [[score, trainingTime]]
	else:
		currentRuns[label] = {trainingDataToLetterRatio: [[score, trainingTime]]}

	#create new text to write to the text file
	textToWrite = "dtype-dataFormat-params:\n\ttraining values per letter:\n\t\tscore\ttrainingTime\n\n"
	for label in currentRuns.keys():
		textToWrite += f"{label}:\n"
		for trainingDataToLetterRatio in currentRuns[label].keys():
			textToWrite += f"\t{trainingDataToLetterRatio}:\n"
			for trainingResult in currentRuns[label][trainingDataToLetterRatio]:
				tempResult = [str(num) for num in trainingResult]
				textToWrite += f"\t\t{"\t".join(tempResult)}\n"
		textToWrite += "\n\n"
	
	#write to dict to the json file and text to the text file
	jsonFile = open(f"./testResults/{encryptorName}/jsonFiles/{clfname}.json", "w")
	json.dump(currentRuns, jsonFile)
	textFile.write(textToWrite.strip())

	#close files
	jsonFile.close()
	textFile.close()


def runML(xTrain, yTrain, xTest, yTest, clf):
	'''
	Runs a ML classifier and prints updates, guesses on testing values, testing values, and the score

	Parameters:
		xTrain (npArray): training data
		yTrain (npArray): training labels
		xTest (npArray): testing data
		yTest (npArray): testing labels
		clf (classifier): ML classifier to use
	
	Returns:
		clf: trained classifier
		str: classifier name
		float: score
		float: training time
	'''
	startTime = time.time()
	score = 0.0
	predictedValues = []

	print(f"\nTraining {type(clf).__name__} with {yTrain.shape[0]} values")
	clf.fit(xTrain, yTrain)
	trainingTime = time.time() - startTime
	print(f"Training completed in {round(trainingTime, 2)} seconds")

	print(f"\nResults against {yTest.shape[0]} values:")
	score = clf.score(xTest, yTest)
	predictedValues = clf.predict(xTest)

	print("  Predictions:\t", predictedValues)
	print("  Actual Labels:", yTest)
	print("  Score:\t", score, end="\n\n")

	return clf, score, trainingTime


def multiRun(trainingDataToLetterRatios, encryptor, clf, params, trainingReps = 1, testingPercent = 0.05):
	'''
	Runs multiple iterations of runML with different training data to letter ratios, saves run data to the appropriate file, and updates the classifier's text file

	Parameters:
		trainingDataToLetterRatios (iterable): iterable of training data to letter ratios to use
		clf (classifier): classifier to train with
		params (str): params of the classifier
		trainingReps (int): training repetitions for each training data to letter ratio
		testingPercent (float): portion of data that should be used for testing (out of 1)
	'''
	for i in range(len(trainingDataToLetterRatios)):
		currentTDTLR = trainingDataToLetterRatios[i]
		for k in range(trainingReps):
			#1st calculation to find set the TDTLR to the ratio of training to testing data
			#2nd calculation to find testing percent to make currentTDTLR for training data instead of for testing data
			yTrain, xTrain, yTest, xTest = MLDC.generateData(encryptor, round(currentTDTLR * (1 + testingPercent)), ((currentTDTLR * (1 + testingPercent) - currentTDTLR) / currentTDTLR))

			clf, score, trainingTime = runML(xTrain, yTrain, xTest, yTest, clf)

			print("Saving Run")
			saveRun(type(encryptor).__name__, type(clf).__name__, params, score, trainingTime, currentTDTLR)

multiRun([64, 128, 256], ciphers.caesarCipher(), DecisionTreeClassifier(), "gini-best", 3)