from enum import Enum

class TokenType(Enum):			# TokenType Enum
	ERROR = -1
	ADD_ME = 0

class __main__:
	def __init__(self, inp):		# Constructor
		self.input = inp
		self.cursor = 0
		self.DFA = [[-1]*256]*AMOUNT_OF_STATE_TYPES	# 256 = amount of chars, Fill in the amount of state types

	def __iter__(self):			# Init the iterator
		self.cursor = 0
		return self

	def __next__(self):			# get the next character
		character = self.input[self.cursor]
		self.cursor = self.cursor + 1
		return character

	def getToken(self):			# get the next token (Should return a token type)
		raise "impl me"
