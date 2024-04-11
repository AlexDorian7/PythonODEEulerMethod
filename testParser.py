from Token import Parser

#test 1: ALPHA
print ("Testing     part")
equation = "x"
parse = Parser(equation)
print(parse.tok.input)

if parse.equ():
    print ("works!")
else: 
    print ("failed!")

print("\n\n")

#test 2: INT
equation = "100"
parse = Parser(equation)
print(parse.tok.input)
if parse.equ():
    print ("works!")
else: 
    print ("failed!")

print("\n\n")

#test 3: REAL
equation = "100.31415"
parse = Parser(equation)
print(parse.tok.input)
if parse.equ():
    print ("works!")
else: 
    print ("failed!")

print("\n\n")


#test 4: LPAREN equ RPAREN
equation = "(y^2 + 7)"
parse = Parser(equation)
print(parse.tok.input)
if parse.equ():
    print ("works!")
else: 
    print ("failed!")

#test 4.1: LPAREN equ RPAREN
equation = "y^2 + 7"
parse = Parser(equation)
print(parse.tok.input)
if parse.equ():
    print ("works!")
else: 
    print ("failed!")

#test 4.1: LPAREN equ RPAREN
equation = "(y^2 + 7) + 1"
parse = Parser(equation)
print(parse.tok.input)
if parse.equ():
    print ("works!")
else: 
    print ("failed!")

print ("\n\n")

#test 5: ID LPAREN equ RPAREN
equation = "a(a^2 * 7)"
parse = Parser(equation)
print(parse.tok.input)
if parse.equ():
    print ("works!")
else: 
    print ("failed!")

#test 5: ID LPAREN equ RPAREN
equation = "a(7)"
parse = Parser(equation)
print(parse.tok.input)
if parse.equ():
    print ("works!")
else: 
    print ("failed!")
