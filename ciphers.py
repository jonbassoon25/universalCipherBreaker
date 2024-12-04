import time
import random

#classes for different cipher encryptors

class baseCipher:
	abc = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
	ABC = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
	str_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
	sym = [" ", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "{", "}", "[", "]", "\\", "|", ";", ":", "'", "\"", ",", ".", "<", ">", "/", "?", "`", "~"]

	maxEncryptionRatio = 1
	outputType = "string"

	def to_cipher(self, message, verbose = False):
		return message

	def from_cipher(self, message, verbose = False):
		return message
	
class customCipher(baseCipher):
	abc_convert = [80172599, 19018775, 55223788, 82169340, 79652671, 82581483, 84294070, 70323581, 68217152, 39173726, 41574762, 54594244, 63173486, 57087313, 83762575, 33749897, 69284039, 11780575, 42644065, 11343149, 82295201, 72871967, 29858213, 65717980, 46314573, 65540694]
	ABC_convert = [57460057, 51834534, 63739554, 95099535, 74789106, 66823612, 92758169, 27580856, 64499828, 96959279, 14772520, 75320592, 82573996, 80172507, 35185382, 89382482, 70887567, 66194744, 96161381, 68765556, 38789629, 89881155, 70344414, 28098141, 90613848, 69915053]
	num_convert = [45754997, 59461008, 51356057, 82877230, 94865623, 21367471, 67364218, 12628429, 19460772, 56610826]
	sym_convert = [34126067, 58998412, 32875130, 79083743, 67862083, 44480042, 21831723, 28085888, 32167575, 14441370, 85498183, 15771041, 38874783, 93557146, 53741500, 14067993, 54366332, 97117593, 43797144, 91726098, 20635680, 58013905, 65799134, 95233936, 83236379, 13584113, 73063268, 75282796, 91660433, 67919505, 16491396, 28717900, 10824176]
	undefined_convert = 11111111

	maxEncryptionRatio = 36

	def _scramble(self, num):
		'''scrambles num, num can be string or int, num is returned as string'''
		num = str(num)
		num1 = []
		num2 = []
		for i in range(len(num)):
			if i < (len(num)/2):
				num1.append(num[i])
			else:
				num2.append(num[i])
		num1.reverse()
		num2.reverse()
		return ''.join(num1) + ''.join(num2)
	
	def _make_list(self, string):
		end_list = []
		for i in range(len(string)):
			end_list.append(string[i])
		return end_list

	def _special_list(self, string, length):
		#print(string)
		end_list = []
		for i in range(round(len(string)/length)):
			thing_to_add = ''
			for k in range(length):
				thing_to_add += string[k + (i * length)]
			end_list.append(thing_to_add)
		return end_list
	
	def _collide(self, short_num, long_num):
		'''
			collides num with another num
			nums can be strings or ints
			one num is returned as string
			long num should be 2 times the length of short num
		'''
		short_num = str(short_num)
		long_num = str(long_num)
		short_num = self._make_list(short_num)
		long_num = self._make_list(long_num)
		final_num = []
		for i in range(len(short_num)):
			final_num.append(short_num[i])
			final_num.append(long_num.pop(0))
			final_num.append(long_num.pop(0))
		return ''.join(final_num)

	def _encrypt(self, number):
		'''
			encrypts number by multiplying by a random one
			output is short num followed by long num
			number can be int or string
			output is list with 2 strings inside
		'''
		number = int(number)
		rand_num = random.randint(10000000, 99999999)
		number = self._scramble(number)
		end_number = str(int(rand_num) * int(number))
		while len(end_number) < 16:
			end_number = "0" + end_number

		return [str(self._scramble(rand_num)), end_number]
	
	def _convert_to_num(self, character):
		for i in range(len(self.sym)):
			if i < len(self.str_num):
				if self.str_num[i] == character:
					return self.num_convert[i]

			if i < len(self.abc):
				if self.abc[i] == character:
					return self.abc_convert[i]

				if self.ABC[i] == character:
					return self.ABC_convert[i]

			if i < len(self.sym):
				if self.sym[i] == character:
					return self.sym_convert[i]
					
		#print(f"Warning: Character {character} Not Found.")
		return -1
	
	def _compress(self, num):
		'''
			output is string
			input is string or int
		'''
		#print(num)
		num = str(num)
		num = self._make_list(num)
		result = ""
		for i in range(round(len(num)/2)):
			bit = num[i * 2] + num[1 + (i * 2)]
			#print(int(bit) + 33)
			if bit[0] == 0:
				del bit[0]
			#print(bit)
			if bit == "93" or bit == "94" or bit == "95" or bit == "96" or bit == "97" or bit == "98" or bit == "99":
				result += " " + bit
			else:
				result += chr(int(bit) + 33)
			
		return result

	def _uncompress(self, character):
		'''
			output is string
		'''
		result = ''
		ignore_step = 0
		for i in range(len(character)):
			#print(ord(character[i]))
			if character[i] == " ":
				result += (character[i + 1] + character[i + 2])
				ignore_step = 2
			elif ignore_step == 0:
				num = ord(character[i]) - 33
				num = str(num)
				if len(num) < 2:
					num = "0" + num
				result += num
			else:
				ignore_step -= 1
		return result
	
	def _convert_to_char(self, num):
		if num == self.undefined_convert:
			return "_"
		
		for i in range(len(self.sym)):
			if i < len(self.str_num):
				if self.num_convert[i] == num:
					return self.str_num[i]

			if i < len(self.abc):
				if self.abc_convert[i] == num:
					return self.abc[i]

				if self.ABC_convert[i] == num:
					return self.ABC[i]

			if i < len(self.sym):
				if self.sym_convert[i] == num:
					return self.sym[i]
					
		print(f"Code {num} Not Found")
		return '-'

	def _decrypt(self, key, letter):
		key = self._unscramble(key)
		return self._unscramble(round(int(letter) / int(key)))

	def _uncollide(self, num):
		'''
			num should be a string
			output is list with short num then long num in string format
		'''
		short_num = ""
		long_num = ""
		num = str(num)
		for i in range(round(len(num) / 3)):
			short_num += num[i * 3]
			long_num += num[1 + (i * 3)]
			long_num += num[2 + (i * 3)]
		return [short_num, long_num]
	
	def _unscramble(self, num):
		'''unscrambles num, num can be string or int, num is returned as int'''
		num = str(num)
		num1 = []
		num2 = []
		for i in range(len(num)):
			if i < (len(num)/2):
				num1.append(num[i])
			else:
				num2.append(num[i])
		num1.reverse()
		num2.reverse()
		return int(''.join(num1) + ''.join(num2))
	
	def to_cipher(self, message, verbose = False):
		messageLength = len(message)
		message = self._make_list(message)
		pastTime = time.time()
		for i in range(len(message)):
			num = self._convert_to_num(message.pop(0))
			if num != -1:
				num = self._encrypt(num)
			else:
				continue
			message.append(self._compress(self._collide(num[0], num[1])))
			if verbose and i % 5000 == 0:
				print(f"Progress: {(100 * i) // messageLength}%\t{i}/{messageLength}\tEstimated Time Remaining: {((messageLength - i) * ((time.time() - pastTime)))//5000}s")
				pastTime = time.time()
		return ''.join(message)

	def from_cipher(self, encryptedMessage):
		encryptedMessage = self._uncompress(encryptedMessage)
		encryptedMessage = self._special_list(encryptedMessage, 24)
		for i in range(len(encryptedMessage)):
			num = self._uncollide(encryptedMessage.pop(0))
			encryptedMessage.append(self._convert_to_char(self._decrypt(num[0], num[1])))
		return ''.join(encryptedMessage)
	
class uncompressedCustomCipher(customCipher):
	maxEncryptionRatio = 24
	outputType = "num"

	def to_cipher(self, message):
		return self._uncompress(super().to_cipher(message))
	
	def from_cipher(self, encryptedMessage):
		return super().from_cipher(self._compress(encryptedMessage))

class caesarCipher(baseCipher):
	combinedChars = []
	
	def __init__(self, lshift = 3): #lshift of 3 is the original cipher shift
		self.combinedChars = self.abc + self.ABC + self.str_num + self.sym[1:] #don't inculde space in encryption symbols that change
		self.lshift = lshift
	
	def to_cipher(self, message):
		finalMessage = ""
		for char in message:
			if not char in self.combinedChars and not char == " ":
				print(f"Character {char} is not encryptable")
				char = "_"
			elif char == " ":
				finalMessage += char
			else:
				finalMessage += self.combinedChars[(self.combinedChars.index(char) - self.lshift) % len(self.combinedChars)]
		return finalMessage

	def from_cipher(self, encryptedMessage):
		finalMessage = ""
		for char in encryptedMessage:
			if not char in self.combinedChars and not char == " ":
				print(f"Character {char} is not decryptable")
				finalMessage += "_"
			elif char == " ":
				finalMessage += char
			else:
				finalMessage += self.combinedChars[(self.combinedChars.index(char) + self.lshift) % len(self.combinedChars)]
		return finalMessage