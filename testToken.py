import Token

tok = Token.Token("Hello 3.14 7")

for i in range (4):
	type, val = tok.getToken()

	print(type)
	print(val)
