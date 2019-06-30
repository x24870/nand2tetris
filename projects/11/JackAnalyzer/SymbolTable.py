import os
import xml.etree.ElementTree as ET

class SubroutineTable():
    def __init__(self):
        self.var_count = 0
        self.arg_count = 0
        self.table = {}

class SymbolTable():
    def __init__(self):
        self.static_count = 0
        self.field_count = 0
        self.table = {}
        self.subroutine_table = SubroutineTable()

    def startSubroutine(self):
        self.subroutine_table = None
        self.subroutine_table.arg_count = 0
        self.subroutine_table.var_count = 0

    def define(self, name, type_, kind):
        if kind == 'static':
            self.table[name] = {'type': type_, 'kind': 'static', 'idx': self.static_count}
            self.static_count += 1
        elif kind == 'field':
            self.table[name] = {'type': type_, 'kind': 'field', 'idx': self.field_count}
            self.field_count += 1
        elif kind == 'arg':
            self.subroutine_table.table[name] = {'type': type_, 'kind': 'arg', 'idx': self.subroutine_table.arg_count}
            self.subroutine_table.arg_count += 1
        elif kind == 'var':
            self.subroutine_table.table[name] = {'type': type_, 'kind': 'var', 'idx': self.subroutine_table.var_count}
            self.subroutine_table.var_count += 1
        else:
            print('Symbol table define error')
            exit()

    def VarCount(self, kind):
        if kind == 'STATIC':
            return self.static_count
        elif kind == 'FIELD':
            return self.field_count
        elif kind == 'ARG':
            return self.subroutine_table.arg_count
        elif kind == 'VAR':
            return self.subroutine_table.var_count
        else:
            print('Symbol table VarCount error')
            exit()

    def KindOf(self, name):
        if self.table.get(name):
            return self.table.get(name).get('kind')
        elif self.subroutine_table.table.get(name):
            return self.subroutine_table.table.get(name).get('kind')
        else:
            print('Symbol table KindOf error')
            exit()
    
    def TypeOf(self, name):
        if self.table.get(name):
            return self.table.get(name).get('type')
        elif self.subroutine_table.table.get(name):
            return self.subroutine_table.table.get(name).get('type')
        else:
            print('Symbol table TypeOf error')
            exit()

    def IndexOf(self, name):
        if self.table.get(name):
            return self.table.get(name).get('idx')
        elif self.subroutine_table.table.get(name):
            return self.subroutine_table.table.get(name).get('idx')
        else:
            print('Symbol table IndexOf error')
            exit()

if __name__ == '__main__':
    s_table = SymbolTable()
    print(s_table.subroutine_table.arg_count)