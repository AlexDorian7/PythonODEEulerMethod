import Token

tok = Token.Token("1 123 1.1 12.1 123.123 + - * / ^ (( )( TESTING UPPERCASE testing lowercase ")


num_tokens = len(tok.input.split())
print (tok.input)
for i in range (num_tokens):
	type, val = tok.getToken()

	print("type: ", type, "  value: ", val)
