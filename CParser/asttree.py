#from statement import Statement

class AST:

    def __init__(self, statement):
        self.statement = statement
        self.next_node = None
        self.under_node = None

    def set_next(self, new_node):
        self.next_node = new_node

    def set_under(self, new_node):
        self.under_node = new_node

    def get_next(self):
        return self.next_node

    def get_under(self):
        return self.under_node

    def get_statement(self):
        return self.statement

    def print(self):
        self.statement.print()
        if self.under_node != None:
            print("     start under")
            self.under_node.print()
            print("     end of under")
        if self.next_node != None:
            self.next_node.print()

    def toListStrings(self):
        out = [self.statement.get_info()]
        if self.under_node != None:
            out += self.under_node.toListStrings()
        if self.next_node != None:
            out += self.next_node.toListStrings()
        return out



