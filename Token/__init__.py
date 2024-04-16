import Tree
from enum import Enum
import numpy as np

class TokenType(Enum):	# TokenType Enum
	ERROR		= -1
	ADDOP		= 1
	MINOP		= 2
	MULOP		= 3
	REAL		= 4
	EXP_CHAR	= 6 # ^
	ALPHA		= 7
	RPAREN		= 8
	LPAREN		= 9
	EOF		= 10

class Token:

	def __init__(self, inp):				# Constructor
		self.input = inp					# The string
		self.cursor = 0						# Position on the string
		self.DFA = [[-1]*256 for r in range(11)]	# 256 = amount of chars (Current 11 states)

		# map out the graph

			#PM
		# START(0) -> + (5)
		self.DFA [0][ord( '+' )] = 5				# ord() returns ASSCI value of a char`
		# START(0) -> - (6)
		self.DFA [0][ord( '-' )] = 6


			#MD
		# START(0) -> * (7)
		self.DFA [0][ord( '*' )] = 7
		# START(0) -> / (7)
		self.DFA [0][ord( '/' )] = 7


			#EXP
		# START(0) -> ^ (8)
		self.DFA [0][ord( '^' )] = 8


			#LPAREN
		# START(0) -> ( (9)
		self.DFA [0][ord( '(' )] = 9
			#RPAREN
		# START(0) -> ) (10)
		self.DFA [0][ord( ')' )] = 10


			#ID (upper and lowercase)
		for i in range( ord('A'), ord('Z')+1):			# [97,122]
			self.DFA [0][i] = 4				# START(0) -> ID (4) uppercase
			self.DFA [0][i+32] = 4				# lowercase

			self.DFA [4][i] = 4				# ID(4) -> ID (4) uppercase
			self.DFA [4][i+32] = 4				# lowercase


			#INT
		for i in range(10):	# [0,9]
			self.DFA [0][ord('0')+i] = 1					 	# START(0) -> DIGIT(1)
			self.DFA [1][ord('0')+i] = 1		 				# DIGIT(1) -> DIGIT(1)
			self.DFA [1][ord( '.' )] = 2		 				# DIGIT(1) -> . (2)
			self.DFA [2][ord('0')+i] = 3		 				# . (2) -> DIGIT (3)
			self.DFA [3][ord('0')+i] = 3						# DIGIT(3) -> DIGIT (3)

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
		prevState = -1

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
		while currState != -1:
			ch = next(self)
			prevState = currState


			currState = self.DFA[currState][ord(ch)] # see if valid state in our DFA look up table

			# store the token value
			if currState != -1:
				value += ch

		# we read an extra character ... put it back for the next get()
		self.putBack()


		if prevState == 2:
			print("WARNING: Invalid Lexical state reached (Ex. \"3.\")")
			exit(2)

		# insure we are not at the end of the line [ we could be at the end of the file and still just have read a valid token. No need to return EOF

		# Return based on internal state
		if prevState == 1 or prevState == 3:
			return (TokenType.REAL, value)
		if prevState == 4:
			return (TokenType.ALPHA, value)
		if prevState == 5:
			return (TokenType.ADDOP, value)
		if prevState == 6:
			return (TokenType.MINOP, value)
		if prevState == 7:
			return (TokenType.MULOP, value)
		if prevState == 8:
			return (TokenType.EXP_CHAR, value)
		if prevState == 9:
			return (TokenType.LPAREN, value)
		if prevState == 10:
			return (TokenType.RPAREN, value)

		# Very bad if we got here!
		print("WARNING: Failed to match a valid internal state type!")
		exit(3)

		# return (prevState, value)


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

			if tokType == TokenType.ADDOP or tokType == TokenType.MINOP: # -> term PM 

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

		boolVal, nodeReturned = self.negator()
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

				boolVal, nodeReturned = self.negator()
				if boolVal: # -> negator EXPR_CHAR factor
					node.right = nodeReturned # from ending negator()
					return (True, node)
				else:
					return (False, node)
			else: 
				#unget token
				self.tok.cursor = savePos
				return (True, nodeReturned) # -> negator
		else:
			return (False, node)

	# negator = <b>M</b> factor | factor
	def negator(self):
		node = None
		savePos = self.tok.cursor
		tokType, tokValue = self.tok.getToken()
		if tokType == TokenType.MINOP: # M
			node = Tree.Node(Tree.NodeType.MUL)
			node.left = Tree.Node(Tree.NodeType.CONST)
			node.left.constant = -1
		else: # factor
			self.tok.cursor = savePos
		boolVal, nodeReturned = self.factor()
		if boolVal:
			if node == None:
				node = nodeReturned
			else:
				node.right = nodeReturned
		return (boolVal, node)

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
