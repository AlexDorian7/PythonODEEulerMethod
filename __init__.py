import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl

import Euler

import Token

print("Please enter your equation: ", end="")

ode = Euler.ODE(Token.Parser(input()))

method = Euler.EulerMethod(ode)

x, y = method.start()

# x = np.linspace(0, 2 * np.pi, 200)
# y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
