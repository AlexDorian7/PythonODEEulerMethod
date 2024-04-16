# PythonODEEulerMethod


### Parser Rules
* equ = term <b>PM</b> equ | term
* term = factor <b>MD</b> term | factor term | factor
* factor = negator <b>EXP_CHAR</b> factor | negator
* negator = <b>M</b> part | part
* part = <b>ALPHA</b> | <b>INT</b> | <b>NUM_REAL</b> | <b>LPAREN</b> equ <b>RPAREN</b> | <b>ALPHA</b> <b>LPAREN</b> equ <b>RPAREN</b>

### Supported functions

* sin(x)
* cos(x)
* tan(x)
* arcsin(x)
* arccos(x)
* arctan(x)
* abs(x)
* sign(x)
* exp(x) # e^x
* ln(x)
* log(x)
* log2(x)
