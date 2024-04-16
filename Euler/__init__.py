class ODE:
	def __init__(self, parser):
		self.success, self.root = parser.equ()
		if not self.success:
			print("WARNING: The provided equation could not be parsed!")
			exit(1)
		print("Please enter a value for x0: ", end="")
		self.X0 = float(input())
		print("Please enter a value for y0: ", end="")
		self.Y0 = float(input())
		print("Please enter a value for h:  ", end="")
		self.H = float(input())
		self.currX = self.X0
		self.currY = self.Y0

	def __iter__(self):			# Iterate using Euler's Method
		self.currX = self.X0
		self.currY = self.Y0
		return self

	def __next__(self):			# Iterate using Euler's Method
		self.currY = self.currY + self.H * self.root(x=self.currX, y=self.currY)		# y = y0+h*f(x,y(x))
		self.currX = self.currX + self.H							# x = x0+h
		return (self.currX, self.currY)

class EulerMethod:
	def __init__(self, ode):
		self.ODE = ode
		self.xVec = []
		self.yVec = []
		self.text = []
		self.xVec.append(ode.X0)
		self.yVec.append(ode.Y0)
		self.steps = 0
		self.it = iter(self.ODE)

	def reset(self):
		self.xVec = []
		self.yVec = []
		self.text = []
		self.xVec.append(self.ODE.X0)
		self.yVec.append(self.ODE.Y0)
		self.it = iter(self.ODE)

	def start(self):
		print("How many steps of Euler's Method would you like to preform? ", end='')
		self.steps = int(input())
		step = 0
		self.text.append(["x", "y"])
		while step < self.steps:
			x,y = next(self.it)
			self.xVec.append(x)
			self.yVec.append(y)
			self.text.append([str(x), str(y)])
			step = step + 1
		# print(self.xVec)
		# print(self.yVec)
		return (self.xVec, self.yVec, self.text)
