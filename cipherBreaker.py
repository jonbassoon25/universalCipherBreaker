import MLRunner
import MLDC
import numpy as np
import joblib


def trainClf(encryptor, clf, TDTLR, testingPercent = 0.05):
	yTrain, xTrain, yTest, xTest = MLDC.generateData(encryptor, round(TDTLR * (1 + testingPercent)), ((TDTLR * (1 + testingPercent) - TDTLR) / TDTLR))

	clf, score, trainingTime = MLRunner.runML(xTrain, yTrain, xTest, yTest, clf) #also prints training results
	
	joblib.dump(clf, "./CCCs/cipherCharacterClassifier.pkl")
	with open("./CCCs/cipherClassifierDescription.txt", "w") as CCDFile:
		CCDFile.write(f"{type(clf).__name__} trained with {TDTLR} values per letter on the {type(encryptor).__name__} cipher\nScore of {round(score,3)}. Training Time of {round(trainingTime,2)}s")

def score(actual, result):
	'''
	Scores the similarity of the result string against the actual string

	Parameters:
		actual (str): real string
		result (str): predicted string
	
	Returns:
		(float): similarity of the result string and the actual string to 3 decimal places
	'''
	correct = 0
	for i in range(len(result)):
		if i >= len(actual):
			break
		if actual[i] == result[i]:
			correct += 1
	return round(correct/len(actual), 3)

def breakCipher(clf, encryptedChars, encryptorOutputType, encryptorMaxEncryptionRatio):
	'''
	Uses the provided classifier model to decrypt the encrypted message

	Parameters:
		clf (clf): trained decryption model
		encryptedMessage (str): message to decrypt
		encryptorOutputType (str): output data format of the encryptor
		encryptorMaxEncryptionRatio (int): maximum expansion ratio of a translated message
	
	Returns:
		(str): predicted decryption of message
	'''
	#format data for ml, match to training data format
	print("Encrypted Message:\n\t" + "".join([str(thing) for thing in encryptedChars.ravel()]) + "\n")

	encryptedChars = MLDC.formatData(None, encryptedChars, encryptorOutputType, encryptorMaxEncryptionRatio)

	result = "".join(clf.predict(encryptedChars))
	return result

def encryptAndBreak(encryptor, clf, message):
	'''
	Encryptes the given message and decrypts it with the given classifier

	Parameters:
		encryptor (cipher): encryptor to use to encrypt data
		clf (clf): trained decryption model
		message (str): message to encrypt
	
	Returns:
		(str): predicted decryption of the encryption of message
	'''
	encryptedMessage = encryptor.to_cipher(message)
	return breakCipher(clf, np.array(encryptor.convert_to_chars(encryptedMessage)), encryptor.outputType, encryptor.maxEncryptionRatio)

def decryptUserMessages(encryptor, charClassifier):
	'''
	Allows the user to input messages to encrypt and displays the encrypted message as well as the predicted decryption

	Parameters:
		encryptor (cipher): cipher to use to encrypt data
		charClassifier (clf): trained decryption model
	'''
	while True:
		messageToEncrypt = ""
		while messageToEncrypt == "":
			messageToEncrypt = input("Enter a message to encrypt:\n\t")
		
		result = encryptAndBreak(encryptor, charClassifier, messageToEncrypt)

		print("Decrypted Message:\n\t" + result)
		print("Decryption Score: " + str(score(messageToEncrypt, result)))
		print("\n")