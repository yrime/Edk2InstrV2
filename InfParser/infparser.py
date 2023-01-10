import re

class infParser:
    def __getSourceSectionSt(self, text):
        match = re.finditer("\[Sources\]", text).__next__().end()
        return match

    def __getSourceSectionEn(self, text, start):
        return re.finditer("\[[a-zA-Z]+\]", text[start:]).__next__().start() + start

    def __getClasses(self, text):
        filePathPattern = "[\n\r\t ][a-zA-Z\/$\(\)0-9_]+.c[^p]"
        match = re.findall(filePathPattern, text)
        return match

    def __getDefine(self, text):
        ret= []
        match = re.finditer("\[Defines\]", text).__next__().end()
        en = self.__getSourceSectionEn(text, match)
        defPattern = "DEFINE [a-zA-Z0-9_\- ]+="
        res = re.finditer(defPattern, text[match:en])
        for i in res:
            p = re.match("[ ]*[a-zA-Z\.\/0-9_\-]+", text[match + i.end():])
            ret.append((re.split('[ =]',text[match+i.start():match+i.end()])[1],
                        text[match + i.end()+ p.start():match + i.end()+p.end()]))
        return ret

    def __checkClasses(self, classes, defines):
        ret = []
        b = False
        for c in classes:
            for i in defines:
                # print(i[0], i[1],"$("+i[0]+")",c)
                rep = c.replace("$("+i[0]+")",i[1])
             #   rep = re.sub("[ ]+../","../",rep)
                if rep !=c:
                    ret.append(rep.lstrip().replace("\n", ""))
                    b = True
            if b != True:
                ret.append((c.lstrip()).replace("\n", ""))
                b = False
        return ret

    def getInfClasses(self, text):
        st = self.__getSourceSectionSt(text)
        ed = self.__getSourceSectionEn(text, st)
        cl = self.__getClasses(text[st:ed])
        gr = self.__getDefine(text)
        ret = self.__checkClasses(cl, gr)
        return ret

    def setLibraryClasses(self, cl, str):
        if str.find("[LibraryClasses]\nUefiAflProxy2") == -1:
            out = str.replace("[LibraryClasses]","[LibraryClasses]\nUefiAflProxy2")
        else:
            out = str
        return out