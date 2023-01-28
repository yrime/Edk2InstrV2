
import sys
import re
import os.path

class DPPChecker:


    def __get_flag_headers(self, flags_list):
        out = re.findall('(?<=/FI)[^\s]+.h', flags_list)
        return out

    def __get_includes(self, file):
        pattern = '#include *[<"].+[>"]'
        with open(file, "r") as f:
            text = f.read()
       # text = file
        incudes = re.findall(pattern, text)
        out = []
        pattern2 = '(?<=[<"]).+(?=[>"])'
        for inc in incudes:
            out.append(re.search(pattern2, inc).group(0))
        return out

    def __get_include_files(self, header_files, include_file_string):
        out = []
        include_file_list = re.findall('(?<=/I)[^\s]+(?=[ ])', include_file_string+ " ")
      #  print(include_file_list)
        for file in header_files:
            for incl in include_file_list:
                f = incl + "/" + file
                if os.path.exists(f) == True:
                    if f not in out:
                        out.append(f)
        return out

    def __get_preproc_directives(self, include_files):
        pattern = "(?<=#define )[^\s]+(?=[\n\r\t ])"
        out = []
        for f in include_files:
            print(f)
            with open(f, "r", encoding="utf-8") as ff:
                text = ff.read()
            out += re.findall(pattern, text)
        out = list(set(out))
        out = []
        return out


    def __exclude_if_directive(self, file, directives):
        textOut = ""
        iterText = 0
        with open(file, "r") as f:
            text = f.read()
        multi = re.finditer(r'#ifdef .+|#ifndef .+|#endif|#else', text)
      #  print(directives)
        for i in multi:
            for g in directives:
                if i.group().find(g) != -1:
                  #  print(i.start(), i.end(), i.group())
                    if i.group().find("#ifdef") != -1:
                        textOut += text[iterText: i.start()]
                        iterText = i.end()
                        i = next(multi)
                        textOut += text[iterText: i.start()]
                        if i.group().find("#else") != -1:
                            i = next(multi)
                        iterText = i.end()
                    elif i.group().find("#ifndef") != -1:
                        textOut += text[iterText: i.start()]
                        i = next(multi)
                        iterText = i.end()
                        if i.group().find("#else") != -1:
                            i = next(multi)
                            textOut += text[iterText: i.start()]
                            iterText = i.end()
        textOut += text[iterText: ]
        return textOut


   # '''
    def check(self, file, includes_str, flags_list):
        headers = self.__get_flag_headers(flags_list)
        headers += self.__get_includes(file)
        include_files = self.__get_include_files(headers, includes_str)
       # print(include_files)
        directives = self.__get_preproc_directives(include_files)
        modify_file = self.__exclude_if_directive(file, directives)
    #    print(modify_file)
        with open(file + ".c", "w") as f:
            f.write(modify_file)
        return file + ".c"
    #'''

    def test(self):
        str = '#include <a.h>\n#include "..v/f.h"'
        inc = "/Ic:\\uefiafl\\forvisual2\\sb_fuzzing\\MdePkg\\Library\\PeiMemoryAllocationLib  /Ic:\\uefiafl\\forvisual2\\" \
               "sb_fuzzing\\Build\\NT32X64\\DEBUG_VS2017x86\\X64\\MdePkg\\Library\\PeiMemoryAllocationLib\\PeiMemoryAllocationLib\\" \
               "DEBUG  /Ic:\\uefiafl\\forvisual2\\sb_fuzzing\\MdePkg  /Ic:\\uefiafl\\forvisual2\\sb_fuzzing\\MdePkg\\Include" \
               " /Ic:\\uefiafl\\forvisual2\\sb_fuzzing\\MdePkg\\Include\\X64"
        cc_flags = "/nologo /c /wd4804 /DUEFI /FI../fuzzing_settings.h /DPEDANTIC /WX- /GS- /Gs32768 /D UNICODE /Od /Gy " \
                   "/FIAutoGen.h /EHs-c- /GR- /GF /Zi /Gm"
        file = "C:\\UefiAfl\\ForVisual2\\SB_fuzzing\\InfotecsPkg\\Driver\\ItAuth\\auth.c"
        self.check(file, inc, cc_flags)

#a = DPPChecker()
#a.test()