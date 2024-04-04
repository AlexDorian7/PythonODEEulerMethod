from enum import Enum

class TokenType(Enum):				# TokenType Enum
	ERROR = 0
	ADDOP = 1
	MULOP = 2
	REAL = 3
	EXP = 6
	ALPHA = 7
	RPAREN = 8
	LPAREN = 9
	EOF = 10


class __main__:
	def __init__(self, inp):		# Constructor
		self.input = inp 			# The string 
		self.cursor = 0				# Position on the string
		self.DFA = [[TokenType.ERROR]*256 for r in range(10)]	# 256 = amount of chars (Current 10 final states)
		self.tokType = TokenType.ERROR 				# Token type
		self.tokVal = ""				# Token value

	def __iter__(self):				# Init the iterator
		self.cursor = 0
		return self

	def __next__(self):				# get the next character
		character = self.input[self.cursor]
		self.cursor = self.cursor + 1
		return character
	
	def putBack(self):				# "put" back character
		self.cursor = self.cursor - 1

	def print(self):				# print Token object info
		print("{ Type: ", self.tokType, " Value:", self.tokVal, "}")

	def getToken(self):				# get the next token (Should return a token type)
		# map out the graph

			#PM
		# START(0) -> + (1)
		self.DFA [0][ord( '+' )] = TokenType.ADDOP # ord() returns ASSCI value of a char
		# START(0) -> - (1)
		self.DFA [0][ord( '-' )] = TokenType.ADDOP


			#MD
		# START(0) -> * (2)
		self.DFA [0][ord( '*' )] = TokenType.MULOP
		# START(0) -> / (2)
		self.DFA [0][ord( '/' )] = TokenType.MULOP


			#EXP
		# START(0) -> ^ (6)
		self.DFA [0][ord( '^' )] = TokenType.EXP


			#LPAREN
		# START(0) -> ( (9)
		self.DFA [0][ord( '(' )] = TokenType.LPAREN
			#RPAREN
		# START(0) -> ) (9)
		self.DFA [0][ord( ')' )] = TokenType.RPAREN


			#ID (upper and lowercase)
		for i in range( ord('A'), ord('Z')+1): # [97,122]
			self.DFA [0][i] = TokenType.ALPHA	# START(0) -> ID (7) uppercase 
			self.DFA [0][i+32] = TokenType.ALPHA # lowercase

			self.DFA [7][i] = TokenType.ALPHA 	# ID(7) -> ID (7) uppercase
			self.DFA [7][i+32] = TokenType.ALPHA # lowercase


			#INT	
		for i in range(10): # [0,9]
			self.DFA [0][ord(i)] = TokenType.REAL 		# START(0) -> DIGIT(3)
			self.DFA [3][ord(i)] = TokenType.REAL 		# DIGIT(3) -> DIGIT(3)	
			self.DFA [3][ord( '.' )] = TokenType.REAL 	# DIGIT(3) -> . (4)	
			self.DFA [4][ord(i)] = TokenType.REAL 		# . (4) -> DIGIT (5)
			self.DFA [5][ord(i)] = TokenType.REAL		# DIGIT(5) -> DIGIT (5)

		# done mapping graph
			
		# Start of the algorithm
		
		# Keep track of the state
		currState = -1
		prevState = TokenType.ERROR

		# value = "" # store value read from input file

		ch = next(self) # value read from input file
		

		# handle white spaces
		while ch.isspace():
			ch = next(self)

		# make sure we are not at the end of the file
		if len(self.input) < self.cursor:
			self.tokType = TokenType.EOF
			return TokenType.EOF # EOF
	
		# put back char
		self.putBack()
	
		# THE algorithm
		while currState != TokenType.ERROR: # not ERROR
			ch = next(self)
			prevState = currState
			currState = self.DFA[currState][ord(ch)]

			if currState != TokenType.ERROR:
				self.tokVal += ch			


		# we read an extra character ... put it back for the next get()
		# insure we are not at the end of the line
		if len(self.input) < self.cursor:
			return TokenType.EOF # EOF

		# encountered a invalid state
		self.tokType = prevState
		return prevState; # answer will be in prevState since we hopped out of while loop