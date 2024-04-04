import Token

tok = Token.Token("Hello 3.14 7")

for i in range (4):
	type, val = tok.getToken()

	print(type)
	print(val)

# Running lexical analyzer



# Below was my old stuff that was override during merge
#Create File object
File_object = open(r"Token/test.txt", "r")

#   // (try to) get the first token
#   tok.get(ifile);

#   // did the last get call say there were more tokens? 
#   while( tok.type()!=EOF_TOK )
#     {
#       if (tok.type()!=ERROR)
# 	{
# 	  // print out the successfully read Token
# 	  cout << "Resulting token = " << tok << endl;
# 	}
#       else // tok.type()==ERROR
# 	{
# 	  cout << "Syntax error detected on line " << tok.lineNumber() << endl;
# 	}
      
#       // (try to) get the next token 
#       tok.get(ifile);
#     }
