
import sys
from CParser.asttree import AST
from CParser.cparser import CParser

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #  filename = "C:\\work\\tests\\base64.i"
    cp = CParser()
    argv = sys.argv[1]
    with open("instrfiles.txt", "r") as inst:
        rea = inst.read()
        if rea.find(argv) > 0:
            cp.parse(argv)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
