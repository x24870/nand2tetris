import os
import xml.etree.ElementTree as ET

class SubroutineTable():
    def __init__(self):
        self.local_count = 0
        self.arg_count = 0

class SymbolTable():
    def __init__(self):
        self.field_count = 0
        self.static_count = 0
        self.subroutine_table = SubroutineTable()

    def startSubroutine(self):
        pass

    def define(self, name, type, kind):
        pass

    def VarCount(self, kind):
        pass

    def KindOf(self, name):
        pass
    
    def TypeOf(self, name):
        pass

    def IndexOf(self, name):
        pass

if __name__ == '__main__':
    s_table = SymbolTable()
    print(s_table.subroutine_table.arg_count)