import Token as Token
import Parser as Parser

# Running lexical analyzer


#Create File object
File_object = open(r"Token/test.txt", "r")


# Create Token object
tok = Token.__main__(File_object)
tok.printTok() 
print("HI")



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