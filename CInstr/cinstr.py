from CParser.statement import StatementObject
from CParser.asttree import AST
from CInstr import settings


class CInstrumentation:
    def __init__(self):
        self.appendDirective = "#include <Library/UefiAflProxy2.h>\n"
        self.appendInitFunction = "EFI_AFL_PROXY2_PROTOCOL *AflProxy2 = init_afl(%d);"
        self.appendFunctions = "AflProxy2->afl_maybe_log(%d);"

    def __checkNext(self, asttree):
        state = asttree.get_statement()
        stateName = state.get_name()
        if stateName == "EMPT":
            state = self.__checkNext(asttree.get_next())
        return state

    def __getEndedNextNode(self, asttree):
        nextNode = asttree.get_next()
        if nextNode != None:
            retNode = self.__getEndedNextNode(asttree.get_next())
        else:
            retNode = asttree
        return retNode

    def __astModify(self, asttree):
        if asttree == None:
            return
        statement = asttree.get_statement()
        statementName = statement.get_name()
        if statementName in ["IF", "ELSE", "FOR", "WHIL", "DO"]:
            nextStateName = self.__checkNext(asttree.get_under()).get_name()
            if nextStateName not in ["MUST", "END"]:
                astUnderNode = asttree.get_under()
                astEndedNode = self.__getEndedNextNode(astUnderNode)

                mustAddedBegin = StatementObject("MUST", (0, 0), "{")
                mustAddedEnd = StatementObject("MEND", (0, 0), "}")

                astEndedNode.set_next(AST(mustAddedEnd))
                newASTnode = AST(mustAddedBegin)
                newASTnode.set_next(astUnderNode)
                asttree.set_under(newASTnode)
        self.__astModify(asttree.get_next())

    def __add_instruction_begin_info(self, asttree, instr_command):
        statement = asttree.get_statement()
        statement.change_text(instr_command % settings.rnd.rand() + "\n" + statement.get_info())

    def __add_instruction_end_info(self, asttree, instr_command):
        statement = asttree.get_statement()
        statement.change_text(statement.get_info() + "\n" + instr_command % settings.rnd.rand())

    def __ast_instrumentation(self, asttree):
        statement = asttree.get_statement()
        statementName = statement.get_name()
        if statementName in ["MEND", "RET", "BRE", "CONT"]:
            self.__add_instruction_begin_info(asttree, self.appendFunctions)
        elif statementName in ["MUST", "END", "CASE", "DEF"]:
            self.__add_instruction_end_info(asttree, self.appendFunctions)


    def __ast_viewer(self, asttree):
        self.__ast_instrumentation(asttree)
        if asttree.get_statement().get_name() == "RET":
            return
        next = asttree.get_next()
        under = asttree.get_under()
        if under != None:
            self.__ast_viewer(under)
        if next != None:
            self.__ast_viewer(next)

    def instr(self, asttree):
        self.__astModify(asttree)
        self.__add_instruction_end_info(asttree, self.appendInitFunction)
        self.__ast_viewer(asttree.get_next())