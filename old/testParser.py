from Token import Parser
from Tree import Node, NodeType
import Tree

# #test 1: ALPHA
# print ("[TESTING PART]")
# equation = "x"
# parse = Parser(equation)
# print(parse.tok.input)

# if parse.equ():
#     print ("works!\n")
# else: 
#     print ("failed!")



# #test 2: INT
# equation = "100"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.equ():
#     print ("works!\n")
# else: 
#     print ("failed!")



# #test 3: REAL
# equation = "100.31415"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.equ():
#     print ("works!\n")
# else: 
#     print ("failed!")




# #test 4: LPAREN equ RPAREN
# equation = "(y^2 + 7)"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.equ():
#     print ("works!\n")
# else: 
#     print ("failed!")


# #test 4.1: LPAREN equ RPAREN
# equation = "y^2 + 7"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.equ():
#     print ("works!\n")
# else: 
#     print ("failed!")


# #test 5: ID LPAREN equ RPAREN
# equation = "a(a^2 * 7)"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.equ():
#     print ("works!\n")
# else: 
#     print ("failed!")



# print("[TESTING FACTOR]")

# #test 6: part <b>EXP_CHAR</b> part 
# equation = "a^(y+1)+3a"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.equ():
#     print ("works!\n")
# else: 
#     print ("failed!")


# print("[TESTING TERM]")

# #test 7: factor <b>MD</b> term
# equation = "a^(y+1)+3a * a(a^2 * 7)"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.factor():
#     print ("works!\n")
# else: 
#     print ("failed!")

# #test 7.1: factor <b>MD</b> term
# equation = "a^(y+1)+3a * a^(y+1)+3a"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.factor():
#     print ("works!\n")
# else: 
#     print ("failed!")


# #test 8: factor term
# equation = "a^(y+1)+3a a"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.factor():
#     print ("works!\n")
# else: 
#     print ("failed!")


# print('[TESTING EQU]')
# #test 9: term <b>PM</b> equ
# equation = "a^(y+1)+3a * a^(y+1)+3a + a^(y+1)+3a"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.factor():
#     print ("works!\n")
# else: 
#     print ("failed!")

# #test 10: term
# equation = "a^(y+1)+3a * a^(y+1)+3a + a^(y+1)+3a * a^(y+1)+3a"
# parse = Parser(equation)
# print(parse.tok.input)
# if parse.factor():
#     print ("works!\n")
# else: 
#     print ("failed!")


#test 11: Tree Node Example
equation = "sin(x^2)*x+y"
parse = Parser(equation)
print(parse.tok.input)

bV, rootNode = parse.equ()
print (rootNode)

if parse.equ():
    print ("works!\n")
else: 
    print ("failed!")
