class ODE:
	def __init__(self):
		print("Welcome to the ODE Input Wizard!\nYou will need to provide three numbers from the following form;\ny'(x) = Ay(x) + Bx + C")
		print("A = ", end='')
		self.A = float(input())
		print("B = ", end='')
		self.B = float(input())
		print("C = ", end='')
		self.C = float(input())
		print("You now need to provide the starting point!\ny(X0) = Y0")
		print("X0 = ", end='')
		self.X0 = float(input())
		print("Y0 = ", end='')
		self.Y0 = float(input())
		print("Now you need to provide the step size!")
		print("H = ", end='')
		self.H = float(input())

		self.currX = self.X0
		self.currY = self.Y0

	def __iter__(self):			# Iterate using Euler's Method
		self.currX = self.X0
		self.currY = self.Y0
		return self

	def __next__(self):			# Iterate using Euler's Method
		self.currY = self.currY + self.H * (self.A * self.currY + self.B * self.currX + self.C)
		self.currX = self.currX + self.H
		return (self.currX, self.currY)

class EulerMethod:
	def __init__(self, ode):
		self.ODE = ode
		self.xVec = []
		self.yVec = []
		self.xVec.append(ode.X0)
		self.yVec.append(ode.Y0)
		self.steps = 0
		self.it = iter(self.ODE)

	def reset(self):
		self.xVec = []
		self.yVec = []
		self.xVec.append(self.ODE.X0)
		self.yVec.append(self.ODE.Y0)
		self.it = iter(self.ODE)

	def start(self):
		print("How many steps of Euler's Method would you like to preform? ", end='')
		self.steps = int(input())
		step = 0
		while step < self.steps:
			x,y = next(self.it)
			self.xVec.append(x)
			self.yVec.append(y)
			step = step + 1
		# print(self.xVec)
		# print(self.yVec)
		return (self.xVec, self.yVec)
