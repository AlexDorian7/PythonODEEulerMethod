from Token import Parser

parse = Parser("x+1")
print(parse.tok.input)

if parse.equ():
    print ("It works!")
else: 
    print ("It failed!")