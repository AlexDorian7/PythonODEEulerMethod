import Tree
from enum import Enum
import numpy as np

class TokenType(Enum):	# TokenType Enum
	ERROR	= -1
	ADDOP	= 1
	MULOP	= 2
	REAL	= 3
	EXP_CHAR = 6 # ^
	ALPHA	= 7
	RPAREN	= 8
	LPAREN	= 9
	EOF		= 10

class Token:

	def __init__(self, inp):				# Constructor
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

	def __next__(self):						# Returns the next character from input
		try:
			character = self.input[self.cursor]
			self.cursor = self.cursor + 1
			return character
		except:
			self.cursor = self.cursor + 1
			return chr(4)					# Index out of bounds return ^D EOT End of Transmission [EOF End of File] character

	def putBack(self):						# "Puts" back character into input
		self.cursor = self.cursor - 1

	def getToken(self):						# Returns the next token (Should return <TokenType type, auto(str) value> )
		# Start of the algorithm

		# Keep track of the state
		currState = 0
		prevState = TokenType.ERROR

		value = ""						# store value read from input file

		ch = ''							# value read from input file
		ch = next(self)

		# handles white spaces
		while ch.isspace():
			ch = next(self)

		# makes sure we are not at the end of the file
		if ch == chr(4):
			return (TokenType.EOF, "")			# EOF [ just because we read past the end of the string does not mean that we are an EOF token. There could have still been data before us ]

		# put char
		self.putBack()

		# THE algorithm
		while currState != TokenType.ERROR:
			ch = next(self)
			prevState = currState

			intCurrState = 0 # cannot index on enum in Python... 
			for currEnum in TokenType: 	# ...grabbing enum int value
				if currState == currEnum:
					intCurrState = currEnum.value

			currState = self.DFA[intCurrState][ord(ch)] # see if valid state in our DFA look up table

			# store the token value
			if currState != TokenType.ERROR:
				value += ch 

		# we read an extra character ... put it back for the next get()
		self.putBack()

		# insure we are not at the end of the line [ we could be at the end of the file and still just have read a valid token. No need to return EOF

		# encountered a invalid state
		return (prevState, value)


class Parser: # check if equation entered matches the grammar and returns the corresponding parse tree

	def __init__(self, equation): # constructor
		self.tok = Token(equation) # the equation entered by the user
		self.vars = {} # Any constants that we find will have their value stored here
		
	# equ = term <b>PM</b> equ | term
	def equ (self):

		root = None # the root node

		boolVal, nodeReturned = self.term()
		if boolVal: # -> term

			# need to remember position
			savePos = self.tok.cursor
			# grab token 
			tokType, tokVal = self.tok.getToken() 

			if tokType == TokenType.ADDOP: # -> term PM 

				#select correct operation
				if tokVal == '+':
					root = Tree.Node(Tree.NodeType.ADD)
				elif tokVal == '-':
					root = Tree.Node(Tree.NodeType.SUB)
					
				root.left = nodeReturned # from term()	

				boolVal, nodeReturned = self.equ()
				if boolVal: # -> term PM equ
					root.right = nodeReturned # from equ()
					return (True, root)
				else:
					return (False, root)
			else: # -> term
				# need to unget token
				self.tok.cursor = savePos
				return (True, nodeReturned)
		else:
			return (False, root)

	# term = factor <b>MD</b> term | factor term | factor
	def term(self):
		node = None # construct new blank node

		boolVal, nodeReturned = self.factor() 
		if boolVal: # -> factor

			savePos = self.tok.cursor # remember position	
			tokType, tokVal = self.tok.getToken() # get token

			if tokType == TokenType.MULOP: # -> factor MD

				# select correct operation
				if tokVal == '*':
					node = Tree.Node(Tree.NodeType.MUL)
				elif tokVal == '/':
					node = Tree.Node(Tree.NodeType.DIV)

				node.left = nodeReturned # from factor()

				boolVal, nodeReturned = self.term()
				if boolVal: # -> factor MD term
					node.right = nodeReturned # from term()
					return (True, node)
				else:
					return (False, node)
			else:
				self.tok.cursor = savePos # put back character

				saveNodeReturned = nodeReturned # save node from factor() before calling term()

				boolVal, nodeReturned = self.term()
				if boolVal: # -> factor term
					return (True, nodeReturned) # from term()
				else:  # -> factor
					self.tok.cursor = savePos # from factor()
					return (True, saveNodeReturned)
		else:
			return (False, node)

	# factor = part <b>EXP_CHAR</b> part | part
	def factor(self):
		node = None # construct new blank node

		boolVal, nodeReturned = self.part()
		if boolVal: # -> part

			#get token
			savePos = self.tok.cursor
			tokType, tokVal = self.tok.getToken()

			if tokType == TokenType.EXP_CHAR: # -> part EXPR_CHAR

				node = Tree.Node(Tree.NodeType.EXP_C)
				node.left = nodeReturned # from beginning part()

				boolVal, nodeReturned = self.part()
				if boolVal: # -> part EXPR_CHAR part
					node.right = nodeReturned # from ending part()
					return (True, node)
				else:
					return (False, node)
			else: 
				#unget token
				self.tok.cursor = savePos
				return (True, nodeReturned) # -> part
		else:
			return (False, node)


	# part = <b>ALPHA</b> | <b>ALPHA</b> <b>LPAREN</b> equ <b>RPAREN</b> | <b>INT</b> | <b>NUM_REAL</b> | <b>LPAREN</b> equ <b>RPAREN</b>
	def part(self):
		node = None # construct new blank node

		# read a token first
		tokType,tokVal = self.tok.getToken()

		if tokType == TokenType.ALPHA: # -> ALPHA

			savePreVal = tokVal # save previous token value before reading new token

			savePos = self.tok.cursor
			tokType, tokVal = self.tok.getToken()

			if tokType == TokenType.LPAREN: # -> ALPHA LPAREN

				boolVal, nodeReturned = self.equ()
				if boolVal: # -> ALPHA LPAREN equ

					tokType, tokVal = self.tok.getToken()

					if tokType == TokenType.RPAREN: # -> ALPHA LPAREN equ RPAREN
						node = Tree.Node(Tree.NodeType.CALL) # it is a function
						node.func = savePreVal # ALPHA
						node.right = nodeReturned # equ
						return (True, node)
					else:
						return (False, node)
				else:
					return (False, node)
			else: # -> ALPHA

				node = Tree.Node(Tree.NodeType.VAR)
				node.var = savePreVal # ALPHA # store variable name

				self.tok.cursor = savePos # put back character

				flag = False
				if savePreVal == "pi":
					node.type = Tree.NodeType.CONST
					node.constant = np.pi
					flag = True
				if savePreVal == "e":
					node.type = Tree.NodeType.CONST
					node.constant = np.e
					flag = True
				if savePreVal != "x" and savePreVal != "y" and not flag:
					if self.vars.get(savePreVal, None) == None:
						print("WARNING: Unknown variable [" + savePreVal + "] found! Known variables include [x, y, pi, e].")
						print("    The Program will now prompt for a constant value to assign to this variable")
						print("    " + savePreVal + ": ", end="")
						self.vars[savePreVal] = float(input())
					node.type = Tree.NodeType.CONST
					node.constant = self.vars[savePreVal]
				return (True, node)

		elif tokType == TokenType.REAL: # -> REAL
			node = Tree.Node(Tree.NodeType.CONST) # a CONST node
			node.constant = float(tokVal) # tokVal is a string... initialize constant value
			return (True, node)
		
		elif tokType == TokenType.LPAREN: # -> LPAREN

			boolVal, nodeReturned = self.equ()
			if boolVal: # -> LPAREN equ
				tokType,tokVal = self.tok.getToken()
				if tokType == TokenType.RPAREN: # -> LPAREN equ RPAREN
					return (True, nodeReturned)
				else:
					return (False, node)
			else:
				return (False, node)
		else:
			return (False, node)
