# This is a sample Python script for testing your TRIPLA compiler.

# In PyCharm press Umschalt+F10 to execute it.

import triplayacc
from instruction import print_prog

def test_compiler(name):
    source = "\n".join(open(name).readlines())
    ast = triplayacc.parser.parse(source)  # ,debug=True)
    print("AST:")
    print(ast)
    tram_code=ast.code({},0)
    print_prog(tram_code)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_compiler('whileprograms/complex.while')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
