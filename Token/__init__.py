from enum import Enum

class TokenType(Enum):							# TokenType Enum
	ERROR	= -1
	ADDOP	= 1
	MULOP	= 2
	REAL	= 3
	EXP_CHAR = 6 # ^
	ALPHA	= 7
	RPAREN	= 8
	LPAREN	= 9
	EOF		= 10
	SIN		= 11
	COS		= 12
	TAN		= 13
	ASIN	= 14
	ACOS	= 15
	ATAN	= 16
	ABS		= 17
	SIGN	= 18
	EXP		= 19 # e^() 
	LN		= 20
	LOG		= 21
	LOG2	= 22

class Token:

	def __init__(self, inp):					# Constructor
		self.input = inp					# The string
		self.cursor = 0						# Position on the string
		self.DFA = [[TokenType.ERROR]*256 for r in range(10)]	# 256 = amount of chars (Current 10 final states)

		# map out the graph

			#PM
		# START(0) -> + (1)
		self.DFA [0][ord( '+' )] = TokenType.ADDOP		# ord() returns ASSCI value of a char`
		# START(0) -> - (1)
		self.DFA [0][ord( '-' )] = TokenType.ADDOP


			#MD
		# START(0) -> * (2)
		self.DFA [0][ord( '*' )] = TokenType.MULOP
		# START(0) -> / (2)
		self.DFA [0][ord( '/' )] = TokenType.MULOP


			#EXP
		# START(0) -> ^ (6)
		self.DFA [0][ord( '^' )] = TokenType.EXP_CHAR


			#LPAREN
		# START(0) -> ( (9)
		self.DFA [0][ord( '(' )] = TokenType.LPAREN
			#RPAREN
		# START(0) -> ) (9)
		self.DFA [0][ord( ')' )] = TokenType.RPAREN


			#ID (upper and lowercase)
		for i in range( ord('A'), ord('Z')+1):			# [97,122]
			self.DFA [0][i] = TokenType.ALPHA			# START(0) -> ID (7) uppercase
			self.DFA [0][i+32] = TokenType.ALPHA		# lowercase

			self.DFA [7][i] = TokenType.ALPHA			# ID(7) -> ID (7) uppercase
			self.DFA [7][i+32] = TokenType.ALPHA		# lowercase


			#INT
		for i in range(10):	# [0,9]
			self.DFA [0][ord('0')+i] = TokenType.REAL 	# START(0) -> DIGIT(3)
			self.DFA [3][ord('0')+i] = TokenType.REAL 				# DIGIT(3) -> DIGIT(3)
			self.DFA [3][ord( '.' )] = TokenType.REAL 				# DIGIT(3) -> . (4)
			self.DFA [4][ord('0')+i] = TokenType.REAL 				# . (4) -> DIGIT (5)
			self.DFA [5][ord('0')+i] = TokenType.REAL				# DIGIT(5) -> DIGIT (5)

		# done mapping graph

	def __iter__(self):						# Init the iterator
		self.cursor = 0
		return self

	def __next__(self):						# get the next character
		try:
			character = self.input[self.cursor]
			self.cursor = self.cursor + 1
			return character
		except:
			self.cursor = self.cursor + 1
			return chr(4)					# Index out of bounds return ^D EOT End of Transmission [EOF End of File] character

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
		if ch == chr(4):
			return (TokenType.EOF, "")			# EOF [ just because we read past the end of the string does not mean that we are an EOF token. There could have still been data before us ]

		# put char
		self.putBack()

		# THE algorithm
		while currState != TokenType.ERROR:			# not ERROR
			ch = next(self)
			prevState = currState
			

			intCurrState = 0 # cannot index on enum. 
			for currEnum in TokenType: 	# Grabbing enum int value
				if currState == currEnum:
					intCurrState = currEnum.value


			currState = self.DFA[intCurrState][ord(ch)]

			if currState != TokenType.ERROR:
				value += ch

		# we read an extra character ... put it back for the next get()
		self.putBack()
		# insure we are not at the end of the line [ we could be at the end of the file and still just have read a valid token. No need to return EOF

		# encountered a invalid state
		return (prevState, value);


class Parser:						# Create the parser class

	def __init__(self, input):
		self.tok = Token(input)
		
	# * equ = term <b>PM</b> equ | term
	def equ (self):
		if self.term(): # -> term

			# need to remember position
			savePos = self.tok.cursor

			# grab token 
			tokType, tokVal = self.tok.getToken() # -> term PM 
			if tokType == TokenType.ADDOP:

				if self.equ: # -> term PM equ
					return True;
				else:
					return False;
			else: # -> term
				# need to unget token
				self.tok.cursor = savePos
				return True
		else:
			return False

	# * term = factor <b>MD</b> term | factor term | factor
	def term(self):
		if self.factor: # -> factor
			savePos = self.tok.cursor # remember position	
			tokType, tokVal = self.tok.getToken() # get token
			
			if tokType == TokenType.MULOP: # -> factor MD
				if self.term: # -> factor MD term
					return True
				else:
					return False
			else:
				self.tok.cursor = savePos # put back character

				if self.term(): # -> factor term
					return True
				else:  # -> factor
					return True 
		else:
			return False

	# * factor = part <b>EXP_CHAR</b> part | part
	def factor(self):
		if self.part(): # -> part
			#get token
			savePos = self.tok.cursor
			tokType, tokVal = self.tok.getToken()

			if tokType == TokenType.EXP_CHAR: # -> part EXPR_CHAR
				
				if self.part(): # -> part EXPR_CHAR part
					return True
				else:
					return False
			else: 
				#unget token
				self.tok.cursor = savePos
				return True 
		else:
			return False


	# * part = <b>ALPHA</b> | <b>ALPHA</b> <b>LPAREN</b> equ <b>RPAREN</b> | <b>INT</b> | <b>NUM_REAL</b> | <b>LPAREN</b> equ <b>RPAREN</b>
	def part(self):
		# read a token first
		tokType,tokVal = self.tok.getToken()

		if tokType == TokenType.ALPHA: # -> Alpha
			savePos = self.tok.cursor
			tokType, tokVal = self.tok.getToken()

			if tokType == TokenType.LPAREN: # -> Alpha LPAREN
				if (self.equ()): # -> Alpha LPAREN equ
					tokType, tokVal = self.tok.getToken()
					if tokType == TokenType.RPAREN: # -> Alpha LPAREN equ RPAREN
						return True
					else:
						return False
				else:
					return False
			else: # -> Alpha
				self.tok.cursor = savePos # put back character
				return True		
		elif tokType == TokenType.REAL: # -> REAL
			return True
		elif tokType == TokenType.LPAREN: # -> LPAREN
			if self.equ(): # -> LPAREN equ
				tokType,tokVal = self.tok.getToken()
				if tokType == TokenType.RPAREN: # -> LPAREN equ RPAREN
					return True
				else:
					return False
			else:
				return False
		else:
			return False