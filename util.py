import json
import glob

def loadTestResultDict(encryptorName, classifierName):
	'''
	Loads the specifid test result dictionary from ./testResults/jsonFiles/type.json

	Parameters:
        encryptorName (str): encryptor results to take from
		classifierName (str): test result type to load (name of learning alg)
	
	Returns:
		(dict): test results of the given type of learning alg
	'''
	with open(f"./testResults/{encryptorName}/jsonFiles/{classifierName}.json") as jsonFile:
		return json.load(jsonFile)

def loadAllTestResultDicts(encryptorName):
	'''
	Loads all known test results from ./testResults/jsonFiles
	
	Parameters:
        encryptorName (str): encryptor results to take from

	Returns:
		(dict): all test results of learning alg tests
	'''
	testData = {}
	#find all paths to classifer test result json files
	classifiers = glob.glob(f"./testResults/{encryptorName}jsonFiles/*.json")
	#translate paths into classifier names
	for i in range(len(classifiers)):
		classifiers[i] = classifiers[i][len("./testResults/jsonFiles/"):-len(".json")]
	#load test data for each classifier
	for classifier in classifiers:
		testData[classifier] = loadTestResultDict(classifier)
	return testData