from enum import Enum

class TokenType(Enum):				# TokenType Enum
	ERROR = -1
	ADD_ME = 0

class __main__:
	def __init__(self, inp):		# Constructor
		self.input = inp
		self.cursor = 0
		self.DFA = [[-1]*256 for r in range(10)]	# 256 = amount of chars (Current 10 final states) #KD

	def __iter__(self):				# Init the iterator
		self.cursor = 0
		return self

	def __next__(self):				# get the next character
		character = self.input[self.cursor]
		self.cursor = self.cursor + 1
		return character

	def getToken(self):				# get the next token (Should return a token type)
		# map out the graph

			#PM
		# START(0) -> + (1)
		self.DFA [0][ord( '+' )] = 1 # ord() returns ASSCI value of a char
		# START(0) -> - (1)
		self.DFA [0][ord( '-' )] = 1


			#MD
		# START(0) -> * (2)
		self.DFA [0][ord( '*' )] = 2
		# START(0) -> / (2)
		self.DFA [0][ord( '/' )] = 2


			#EXP
		# START(0) -> ^ (6)
		self.DFA [0][ord( '^' )] = 6


			#LPAREN
		# START(0) -> ( (9)
		self.DFA [0][ord( '(' )] = 9
			#RPAREN
		# START(0) -> ) (9)
		self.DFA [0][ord( ')' )] = 9


			#ID (upper and lowercase)
		for i in range( ord('A'), ord('Z')+1): # [97,122]
			self.DFA [0][i] = 7	# START(0) -> ID (7) uppercase 
			self.DFA [0][i+32] = 7 # lowercase

			self.DFA [7][i] = 7 	# ID(7) -> ID (7) uppercase
			self.DFA [7][i+32] = 7 # lowercase


			#INT	
		for i in range(10): # [0,9]
			self.DFA [0][ord(i)] = 3 		# START(0) -> DIGIT(3)
			self.DFA [3][ord(i)] = 3 		# DIGIT(3) -> DIGIT(3)	
			self.DFA [3][ord( '.' )] = 4 	# DIGIT(3) -> . (4)	
			self.DFA [4][ord(i)] = 5 		# . (4) -> DIGIT (5)
			self.DFA [5][ord(i)] = 5		# DIGIT(5) -> DIGIT (5)

		# done mapping graph
			
		# THE algorithm


