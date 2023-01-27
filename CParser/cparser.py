import re

from CParser.statement import StatementBuilder
from CParser.asttree import AST
from CInstr.cinstr import CInstrumentation
from CInstr import settings


class CParser:

    def __nullstr_remover(self, text):
        lines = text.split('\n')
        new_lines = []
        for line in lines:
            if len(line) > 0 and not line.isspace():
                new_lines.append(line)
        return '\n'.join(new_lines)

    def __comment_remover(self, text):
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " "  # note: a space and not an empty string
            else:
                return s

        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        return re.sub(pattern, replacer, text)

    def __clean_text(self, text):
        data = self.__comment_remover(text)
        data = self.__nullstr_remover(data)
        return data

    def __iter_bb_fin(self, text, index):
        i = 0
        fi = 0
        while (True):
            if text[index + i] == '{':
                fi = fi + 1
            elif text[index + i] == '}':
                fi = fi - 1
                if fi == 0:
                    return index + i
            i = i + 1

    def __iter_bb(self, text):
        indexes_bb = []
        iter = 0
        while iter < len(text):
            if text[iter] == "{":
                ifin = self.__iter_bb_fin(text, iter)
                indexes_bb.append((iter, ifin))
                iter = ifin
            iter = iter + 1
        return indexes_bb

    def __get_func_bb(self, text, indexes_bb):
        indexes_fun = []
        for match in re.finditer("\)[ \t]*\n?[ \t]*\{", text):
            for index in indexes_bb:
                if (match.end() - 1) == index[0]:
                    indexes_fun.append((index[0], index[1]))
        return indexes_fun

    def __get_bb(self, text):
        i = self.__iter_bb(text)
        f = self.__get_func_bb(text, i)
        return f
###
#    return (AST, index)
###

    def __ast_tree_build(self, statetementBuilder):
        statement = statetementBuilder.get_next_statement()
        statementName = statement.get_name()
        ast = AST(statement)
        astnode = ast
        if statementName == "MUST":
            while statementName != "MEND":
                statement = statetementBuilder.get_next_statement()
                statementName = statement.get_name()
                astnode.set_next(AST(statement))
                astnode = astnode.get_next()
                next_state = statetementBuilder.check_next_statement()

                if statementName in ["IF", "ELSE", "FOR", "WHIL", "DO", "SWIT"]:
                    astnode.set_under(self.__ast_tree_build(statetementBuilder))
                elif next_state != None and statementName not in ["MEND"]:
                    if next_state.get_name() in ["MUST"]:
                        astnode.set_next(self.__ast_tree_build(statetementBuilder))
            return ast
        elif statementName == "EMPT":
            astnode.set_next(self.__ast_tree_build(statetementBuilder))
            return ast
        elif statementName in ["IF", "ELSE", "FOR", "WHIL", "DO"]:
            astnode.set_under(self.__ast_tree_build(statetementBuilder))
            if statetementBuilder.check_next_statement().get_name() in ["IF", "ELSE", "FOR", "WHIL", "DO"]:
                astnode.set_next(self.__ast_tree_build(statetementBuilder))
            return ast
        else:
            return ast

    def parse(self, file):
        cIntrumentation = CInstrumentation()
        settings.init()
        with open(file, "r") as cf:
            text = cf.read()
        text = self.__clean_text(text)
        bb = self.__get_bb(text)
        i = 0
        out = "#pragma warning(disable : 4702)\n#include <Library/UefiAflProxy2.h>\n"
        for b in bb:
            out += text[i:b[0]]
            fun = text[b[0] : b[1] + 1]
            stBuilder = StatementBuilder(fun)
            ast = self.__ast_tree_build(stBuilder)
            #   ast.print()
            cIntrumentation.instr(ast)
            aststring = ''.join(ast.toListStrings())
            #    print(ast.toListStrings())
            out += aststring
            i = b[1] + 1
        out += text[i:]
        with open(file, "w") as cf:
            cf.write(out)

        #print(out)
        #out

