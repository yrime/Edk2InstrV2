import json
import os.path

from InfParser.infparser import infParser

def parseConfig(text):
    conf = json.loads(text)
    return conf["files"]

if __name__ == '__main__':
    with open("config.txt", "r") as conffile:
        conf = conffile.read()

    files = parseConfig(conf)
    infParser = infParser()

    with open("instrfiles.txt", "w") as inst:
        for f in files:
            with open(f, "r") as inffile:
                text = inffile.read()
            ginf = infParser.getInfClasses(text)
            inftext = infParser.setLibraryClasses("UefiAflProxy2", text)

            with open(f, "w") as inffile:
                inffile.write(inftext)

            dirname = os.path.dirname(f) + "\\"
            for fg in ginf:
                inst.write(dirname+fg + ".i\n")


