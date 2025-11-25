# This is a sample Python script for testing your TRIPLA parser.

# In PyCharm press Umschalt+F10 to execute it.

import triplayacc

def test_parser(name):
    source = "\n".join(open(name).readlines())
    ast = triplayacc.parser.parse(source, debug=True)
    print("AST:")
    print(ast)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_parser('triplaprograms/invalidProgram.tripla')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
