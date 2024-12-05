#Maching Learning Data Creator (MLDC)
#creates testing and training data with labels of a given type from a given cipher

import numpy as np
import ciphers #for testing

def createSingleCharData(encryptor, char, quantity):
	'''
		returns a numpy array of encryptions of the given char with a shape of (quantity,)

		Parameters:
			encryptor (cipher): cipher to use for encryptions
			char (char): character to encrypt
			quantity (int): quantity of encryptions of char

		Returns:
			npArray: quantity encryptions of char
	'''
	charData = np.array([" " * encryptor.maxEncryptionRatio for i in range(quantity)])

	for i in range(quantity):
		charData[i] = encryptor.to_cipher(char)

	return charData

def createCharacterEncryptions(encryptor, encryptionsPerLetter):
	'''
		Creates encrypted letter data

		Parameters:
			encryptor (cipher): cipher to use for encryptions
			encryptionsPerLetter (int): quantity of encryptions per supported letter of the encryptor

		Returns:
			(npArray): 2d array of encryptions with shape (num supported cipher chars, encryptionsPerLetter)
	'''
	characterEncryptions = []
	for char in (encryptor.abc + encryptor.ABC + encryptor.str_num + encryptor.sym):
		characterEncryptions.append(createSingleCharData(encryptor, char, encryptionsPerLetter))

	return np.array(characterEncryptions)

def formatData(encryptor, encryptedDataArray):
	'''
	Formats the given data for training

	Parameters:
		encryptor (cipher): encryptor used to create the encrypted data array
		encryptedDataArray (npArray): single or multi-dimensional array of encryptions with each element being an encryption of a character
	
	Returns:
		(npArray): 2d array with each value being an array of numbers representing each encryption
	'''
	initialShape = encryptedDataArray.shape
	encryptedDataArray = encryptedDataArray.ravel()
	finalArray = np.array([np.zeros(encryptor.maxEncryptionRatio, dtype="uint8") for i in range(len(encryptedDataArray))])
	
	if encryptor.outputType == "string":
		#for each encryption
		for i in range(len(encryptedDataArray)):
			#ords is an array of the ordinal numbers of each element of the string encryption
			ords = [ord(char) for char in encryptedDataArray[i]]
			for j in range(len(finalArray[i])):
				#if the final array index is < the length of this encryption, set the final array index to the ordinal number
				if j < len(ords): 
					finalArray[i][j] = ords[j]
				#if the final array index is >= the length of this encryption, continue to the next one
				else: 
					break
	elif encryptor.outputType == "num":
		for i in range(len(finalArray)):
			nums = [int(num) for num in encryptedDataArray[i]]
			for j in range(len(finalArray)):
				#if the final array index is < the length of this encryption, set the final array index to the ordinal number
				if j < len(nums): 
					finalArray[i][j] = nums[j]
				#if the final array index is >= the length of this encryption, continue to the next one
				else:
					break
	else:
		raise Exception(f"Unable to format data. Encryptor Output Type {encryptor.outputType} not recognized.")
	return finalArray.reshape((initialShape[0] * initialShape[1], encryptor.maxEncryptionRatio))

def generateMLDataLabels(formattedDataArray, supportedEncryptorInputs): #supportedEncryptorInputs should be in order of abc, ABC, num, sym
	'''
	Generates labels of the given data type for the given data

	Parameters:
		formattedDataArray (npArray): formatted data array to generate labels for
		supportedEncryptorInputs (array-like): list of all supported encryptor inputs (abc + ABC + str_num + sym)
	
	Returns:
		npArray: 1 dimensional label array with 1 value for each value in the given data array
	'''
	return np.array([[letter for i in range(formattedDataArray.shape[0] // len(supportedEncryptorInputs))] for letter in supportedEncryptorInputs]).ravel()

def randomizeMLData(labels, formattedDataArray):
	'''
	Randomizes the 1st dimension indicies of the given labels and data in the same way

	Parameters:
		labels (npArray): 1 dimensional label array
		formattedDataArray (npArray): 2d formatted data array

	Returns:
		npArray: randomized label array
		npArray: randomized data array
	'''
	idx = np.argsort(np.random.random(labels.shape[0]))
	data = formattedDataArray[idx]
	
	labels = labels[idx]
	return labels, data

def splitMLData(randomizedLabels, randomizedDataArray, testingPercent):
	'''
	Splits the given labels and data into testing and training sets

	Parameters:
		randomizedLabels (npArray): randomized 1 dimensional label array
		randomizedDataArray (npArray): randomized multidimensional data array
		testingPercent (float): portion of data that should be used for testing (out of 1)

	Returns:
		npArray: testing labels
		npArray: testing data
		npArray: training labels
		npArray: training data
	'''
	splitNum = int((testingPercent * randomizedLabels.shape[0]) // 1)

	testingLabels = randomizedLabels[:splitNum]
	testingData = randomizedDataArray[:splitNum]
	trainingLabels = randomizedLabels[splitNum:]
	trainingData = randomizedDataArray[splitNum:]
	return testingLabels, testingData, trainingLabels, trainingData

def generateData(encryptor, encryptionsPerLetter, testingPercent = 0.05):
	'''
	Generates randomized testing and training data and labels that works to train for the given encryptor

	Parameters:
		encryptor (cipher): cipher to encrypt characters with
		encryptionsPerLetter (int): number of encryptions for each supported letter of the encryptor
	
	Returns:
		(npArray, npArray): training labels, training data
		(npArray, npArray): testing labels, testing data
	'''
	print(f"Creating Data with TD:L of {encryptionsPerLetter}:1")

	#create raw encryptions
	encryptedData = createCharacterEncryptions(encryptor, round(encryptionsPerLetter * (1 + testingPercent))) #check this formula

	#format encryptions for training (char to num)
	print("Formatting Data for Training...")
	formattedData = formatData(encryptor, encryptedData)

	#create labels
	labels = generateMLDataLabels(formattedData, encryptor.abc + encryptor.ABC + encryptor.str_num + encryptor.sym)

	#randomize data and labels
	randomizedLabels, randomizedData = randomizeMLData(labels, formattedData)

	testingLabels, testingData, trainingLabels, trainingData = splitMLData(randomizedLabels, randomizedData, testingPercent)
	
	return testingLabels, testingData, trainingLabels, trainingData