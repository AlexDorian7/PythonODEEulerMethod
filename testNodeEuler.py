import numpy as np

import Tree
# from Token import Parser
import Token

from Tree import Node, NodeType

#[EXAMPLE 1]
# n = Node(NodeType.CONST)
# n.constant = 5
# print("n = ",n(x=10))

# v = Node(NodeType.VAR)
# v.var = "x" 	# declare variable name
# print("v = ", v(x=10)) 	# init var value

# #sin(5)
# c = Node(NodeType.CALL)
# c.func = "sin" 	# function name
# c.right = n	# function param.
# print(str(c.func) + '(' + str(c.right.constant) + ') = ', c(y=50)) 	# Notice y here is never used

# a = Node(NodeType.ADD)
# a.left = v
# a.right = c
# print(a(x=200)) # Notice x here is different from aboves


# [EXAMPLE 2]:

# y' = sin(x^2)*x+y


# root = Tree.Node(Tree.NodeType.ADD)

# root.right = Tree.Node(Tree.NodeType.VAR)
# root.right.var = "y"

# mult = Tree.Node(Tree.NodeType.MUL)
# root.left = mult

# mult.right = Tree.Node(Tree.NodeType.VAR)
# mult.right.var = "x"

# call = Tree.Node(Tree.NodeType.CALL)
# call.func = "sin"
# mult.left = call


# exp = Tree.Node(Tree.NodeType.EXP_C)
# call.right = exp

# exp.left = Tree.Node(Tree.NodeType.VAR)
# exp.left.var = "x"

# exp.right = Tree.Node(Tree.NodeType.CONST)
# exp.right.constant = 2

equation = "sin(x^2)*x+y"

parseObj = Token.Parser(equation)

boolVal, root = parseObj.equ()


print("x, y")

h = 0.01 # np.pi/4

x = 0 # Starting x
y = 1 # starting y

while x <= np.pi*2: # Euler's Method
	print(str(x) + ", " + str(y))
	y = y + (h * root(x=x, y=y))
	x += h

print(str(x) + ", " + str(y))