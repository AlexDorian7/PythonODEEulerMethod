from Token import Parser

parse = Parser("")
print(parse.tok.input)

if parse.equ():
    print ("It works!")
else: 
    print ("It failed!")