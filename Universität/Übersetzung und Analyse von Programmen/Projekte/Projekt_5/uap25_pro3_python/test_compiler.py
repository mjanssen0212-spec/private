
from compiler import *
from triplayacc import parser
import vistram.tram as tram


#source="\n".join(open("test.tripla").readlines())

#source="\n".join(open("triplaprograms/wrapper.tripla").readlines())

source="\n".join(open("whileprograms/simple.while").readlines())

ast = parser.parse(source) #,debug=True)
print("AST:")
print(ast)
#print(syntax.astToDOT(ast))
tram_code=ast.code({},0)
assemble(tram_code,"test.tram")

tram=tram.TRAM(tram_code)
tram.start()

