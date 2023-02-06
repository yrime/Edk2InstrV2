import os
import subprocess
import sys
from CParser.cparser import CParser
from edk2DPPChecker import DPPChecker

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #  filename = "C:\\work\\tests\\base64.i"
    cp = CParser()
    instrFile = sys.argv[1].lower()
    ccflag = sys.argv[2]
    inc = sys.argv[3]
    forinstrfiles = sys.argv[4]
    runcmd = sys.argv[5].replace("\'","\"")
    with open(forinstrfiles, "r", encoding="utf-8") as inst:
        rea = inst.read().lower()
        # print(sys.argv[2], sys.argv[3])
        k = rea.find(instrFile)
        ci = instrFile
        try:
            if rea.find(instrFile) > 0:
                print(instrFile)
                a = DPPChecker()
                instrFile = a.check(instrFile, inc, ccflag)
                cp.parse(instrFile)
        except:
            instrFile = ci
   # print(runcmd + " " + instrFile)
    subprocess.call(runcmd + " " + instrFile, shell=True)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
