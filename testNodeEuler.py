# y' = sin(x^2)*x+y

import numpy as np

import Tree

root = Tree.Node(Tree.NodeType.ADD)

root.right = Tree.Node(Tree.NodeType.VAR)
root.right.var = "y"

mult = Tree.Node(Tree.NodeType.MUL)
root.left = mult

mult.right = Tree.Node(Tree.NodeType.VAR)
mult.right.var = "x"

call = Tree.Node(Tree.NodeType.CALL)
call.func = "sin"
mult.left = call


exp = Tree.Node(Tree.NodeType.EXP_C)
call.right = exp

exp.left = Tree.Node(Tree.NodeType.VAR)
exp.left.var = "x"

exp.right = Tree.Node(Tree.NodeType.CONST)
exp.right.constant = 2

print("x, y")

h = 0.01 # np.pi/4

x = 0 # Starting x
y = 1 # starting y
while x <= np.pi*2: # Euler's Method
	print(str(x) + ", " + str(y))
	y = y + (h * root(x=x, y=y))
	x += h

print(str(x) + ", " + str(y))
