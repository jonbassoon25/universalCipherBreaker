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
		(npArray): data with initial shape and each value being an array of numbers representing each encryption
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

	return finalArray.reshape((initialShape[0], initialShape[1], encryptor.maxEncryptionRatio))

def generateMLDataLabels(data, supportedEncryptorInputs): #supportedEncryptorInputs should be in order of abc, ABC, num, sym
	pass

def randomizeMLData(labels, formattedDataArray):
	pass

def splitMLData(labels, formattedDataArray):
	pass

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

	#create raw encryptions

	#format encryptions for training (char to num)

	#create and return testing/training data