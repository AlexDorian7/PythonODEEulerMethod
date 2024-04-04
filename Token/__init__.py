from enum import Enum

class TokenType(Enum):							# TokenType Enum
	ERROR = 0
	ADDOP = 1
	MULOP = 2
	REAL = 3
	EXP = 6
	ALPHA = 7
	RPAREN = 8
	LPAREN = 9
	EOF = 10


class Token:
	def __init__(self, inp):					# Constructor
		self.input = inp					# The string
		self.cursor = 0						# Position on the string
		self.DFA = [[TokenType.ERROR]*256 for r in range(10)]	# 256 = amount of chars (Current 10 final states)

		# map out the graph

			#PM
		# START(0) -> + (1)
		self.DFA [0][ord( '+' )] = TokenType.ADDOP		# ord() returns ASSCI value of a char
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
		for i in range( ord('A'), ord('Z')+1):			# [97,122]
			self.DFA [0][i] = 7				# START(0) -> ID (7) uppercase
			self.DFA [0][i+32] = 7				# lowercase

			self.DFA [7][i] = 7				# ID(7) -> ID (7) uppercase
			self.DFA [7][i+32] = 7				# lowercase


			#INT
		for i in range(10):					# [0,9]
			self.DFA [0][ord(i)] = 3 			# START(0) -> DIGIT(3)
			self.DFA [3][ord(i)] = 3 			# DIGIT(3) -> DIGIT(3)
			self.DFA [3][ord( '.' )] = 4 			# DIGIT(3) -> . (4)
			self.DFA [4][ord(i)] = 5 			# . (4) -> DIGIT (5)
			self.DFA [5][ord(i)] = 5			# DIGIT(5) -> DIGIT (5)

		# done mapping graph

	def __iter__(self):						# Init the iterator
		self.cursor = 0
		return self

	def __next__(self):						# get the next character
		character = self.input[self.cursor]
		self.cursor = self.cursor + 1
		return character

	def putBack(self):						# "put" back character
		self.cursor = self.cursor - 1

	def getToken(self):						# get the next token (Should return (TokenType type, auto value) )
		# Start of the algorithm

		# Keep track of the state
		currState = 0
		prevState = TokenType.ERROR

		value = ""						# store value read from input file

		ch = ''							# value read from input file
		ch = next(self)

		# handle white spaces
		while ch.isspace():
			ch = next(self)

		# make sure we are not at the end of the file
		if len(self.input) < self.cursor:
			return (TokenType.EOF, "")			# EOF [ just because we read past the end of the string does not mean that we are an EOF token. There could have still been data before us ]

		# put char
		self.putBack()

		# THE algorithm
		while currState != TokenType.ERROR:			# not ERROR
			ch = next(self)
			prevState = currState
			currState = self.DFA[currState][ord(ch)]

			if currState != TokenType.ERROR:
				value += ch


		# check if ID is not a reserved word
		# if prevState == 3:
				# do we have any reserved words? like SIN, COS, etc...?

		# we read an extra character ... put it back for the next get()
		self.putBack()
		# insure we are not at the end of the line
		if len(self.input) < self.cursor:
			return (TokenType.EOF, "") # EOF

		# encountered a invalid state
		return (prevState, value);


class Parser:						# Create the parser class
	def __init__(self):
	    pass
