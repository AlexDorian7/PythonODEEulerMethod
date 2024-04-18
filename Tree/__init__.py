from enum import Enum

import numpy as np

class NodeType(Enum):
	CONST	= 0
	VAR	= 1
	ADD	= 2
	SUB	= 3
	MUL	= 4
	DIV	= 5
	EXP_C	= 6 # e^(x)
	CALL	= 7


class Node:
	def __init__(self, type):
		self.right = None
		self.left = None
		self.type = type
		self.constant = None		# The number constant to return (for constant value nodes)
		self.var = None			# The var name to access (For var value nodes)
		self.func = None		# The numpy function to call (for call nodes)

	def __call__(self, *args, **kwargs):
		if self.type == NodeType.CONST:	# 0 Children
			return self.constant
		if self.type == NodeType.VAR:	# 0 Children
			return kwargs[self.var]
		if self.type == NodeType.ADD:	# Both Children
			return self.left(*args, **kwargs) + self.right(*args, **kwargs)
		if self.type == NodeType.SUB:	# Both Children
			return self.left(*args, **kwargs) - self.right(*args, **kwargs)
		if self.type == NodeType.MUL:	# Both Children
			return self.left(*args, **kwargs) * self.right(*args, **kwargs)
		if self.type == NodeType.DIV:	# Both Children
			return self.left(*args, **kwargs) / self.right(*args, **kwargs)
		if self.type == NodeType.EXP_C:	# Both Children
			return self.left(*args, **kwargs) ** self.right(*args, **kwargs)
		if self.type == NodeType.CALL:	# Only Right Child. Func Name stored in parent (aka this node)
			return eval("np."+self.func+"("+str(self.right(*args, **kwargs))+")")
		raise Error			# Not a valid Node Type

