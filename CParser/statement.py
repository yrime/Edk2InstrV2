import re

class Statement:
    def __init__(self):
        self.statetment = [
            ("IF", "if[ \t\n\r]*\("),
            ("ELSE", "else[\{ \r\t\n]*"),
            ("FOR", "for[ \t\n\r]*\("),
            ("WHIL", "while[ \t\n\r]*\("),
            ("DO", "do[^a-zA-Z0-9_-][ \t\n\r]*"),
            ("SWIT", "switch[ \r\t\n]*\("),
            ("CASE", "case[ \r\t\n]* [^:]+[ \n\t\r]*:"),
            ("RET", "return"),
            ("BRE", "break[ ]*;"),
            ("CONT", "continue[ ]*;"),
            ("DEF", "default[ ]*:"),
            ("EMPT", "[ \n\t\r]+"),
            ("MUST", "{"),
            ("MEND", "}"),
            ("END", ";[ \n\t\r]*"),
            ("DIRV", "#[^\n]+\s+"),
            ("OPER", "[a-zA-Z0-9_]+[:\r\t ]*\n")
        ]

    def __state_pos(self, text, state):
        match state[0]:
            case "IF":
                ind = self.__get_indexes_struct(text, state[1][0], '(', ')')
                ret = (state[1][0], ind[1])
            case "FOR":
                ind = self.__get_indexes_struct(text, state[1][0], '(', ')')
                ret = (state[1][0], ind[1])
            case "WHIL":
                ind = self.__get_indexes_struct(text, state[1][0], '(', ')')
                ret = (state[1][0], ind[1])
            case "SWIT":
                ind = self.__get_indexes_struct(text, state[1][0], '(', ')')
                ret = (state[1][0], ind[1])
            case "ELSE":
                ret = (state[1][0], state[1][0] + 3 + 1)
            case "DO":
                ret = (state[1][0], state[1][0] + 1 + 1)
            case "CASE":
                ret = (state[1][0], state[1][1])
            case "RET":
                iret = self.__get_first_symbol(text, state[1][0] + 5 + 1, ';') + 1
                ret = (state[1][0], iret)
            case "BRE":
                ret = (state[1][0], state[1][1])
            case "CONT":
                ret = (state[1][0], state[1][1])
            case "DEF":
                ret = (state[1][0], state[1][1])
            case "EMPT":
                ret = (state[1][0], state[1][1])
            case "MUST":
                #   ind = self.__get_indexes_struct(text, state[1][0], '{', '}')
                #   ret = (state[1][0], ind[1])
                ret = (state[1][0], state[1][0] + 1)
            case "MEND":
                ret = (state[1][0], state[1][0] + 1)
            case "END":
                ret = (state[1][0], state[1][0] + 1)
            case "DIRV":
                ret = (state[1][0], state[1][1])
            case "OPER":
                ret = (state[1][0], state[1][1])
        return ret

    def __get_first_symbol(self, text, pos, sym):
        i = 0
        for c in text[pos:]:
            if c == sym:
                return pos + i
            i = i + 1

    def __get_indexes_struct(self, text, index, symbol1, symbol2):
        # print("sdf")
        fi = 0
        i = 0
        for c in text[index:]:
            if c == symbol1:
                fi = fi + 1
                if fi == 1:
                    a1 = index + i
            elif c == symbol2:
                fi = fi - 1
                if fi <= 0:
                    a2 = index + i
                    return (a1, a2 + 1)
            i = i + 1

    def get_state(self, text, i):
        if len(text) <= i:
            return None
        for o in self.statetment:
           # print(o)
            prog = re.compile(o[1])
            res = prog.match(text, i)
            if res != None:
                ret = self.__state_pos(text, (o[0], (res.start(), res.end())))
                return StatementObject(o[0], ret, text[ret[0]:ret[1]])#(o[0], ret)

        iret = self.__get_first_symbol(text, i, ';') + 1
        return StatementObject("UDEF", (i, iret), text[i:iret])#("UDEF", (i, iret))

class StatementObject:

    def __init__(self, name, indexes, info):
        self.name = name
        self.indexes = indexes
        self.info = info

    def get_name(self):
        return self.name

    def get_first_index(self):
        return self.indexes[0]

    def get_last_index(self):
        return self.indexes[1]

    def get_info(self):
        return self.info

    def change_text(self, text):
        self.info = text

    def print(self):
        print(self.name, self.info)

class StatementBuilder:

    def __init__(self, text):
        self.text = text
        self.index = 0
        self.statement = Statement()

    def get_next_statement(self):
        state = self.statement.get_state(self.text, self.index)
        self.index = state.get_last_index()
        return state

    def check_next_statement(self):
        state = self.statement.get_state(self.text, self.index)
        if state == None:
            return state
        ii = state.get_last_index()
        if state.get_name() == "EMPT":
            state = self.statement.get_state(self.text, ii)
        return state