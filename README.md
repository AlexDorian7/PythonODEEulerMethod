# PythonODEEulerMethod

This program is meant to graph a 1st order IVP using Euler's approximation method (Euler's Method).

## Installiation
To install this program first make sure you have python3 and python venv installed (You can learn more about venv [here](https://docs.python.org/3/library/venv.html).)

To install the program,
* On Linux execute the file `install.sh`
* On Windows execute the file `install.bat`
from the command line (command prompt in windows)

## Usage
To run this program after it is installed you can run the files `start.sh` for Linux and `start.bat` for Windows on the command line.
Once run the program will prompt for your equation. (Your must be solved for y'. When entering do **NOT** include `y'=`. Also `y(x)` should be replaced with `y` when entering).
It will also prompt for the starting x and y, the h step and the amount of times to run Euler's Method.

THe program will then display a graph of the function using Euler's Method. 



### Parser Rules
*This is how the parser tries to parse your equation*

* equ = term **PM** equ | term
* term = factor **MD** term | factor term | factor
* factor = negator **EXP_CHAR** factor | negator
* negator = **M** part | part
* part = **ALPHA** | **INT** | **NUM_REAL** | **LPAREN** equ **RPAREN** | **ALPHA** **LPAREN** equ **RPAREN**
