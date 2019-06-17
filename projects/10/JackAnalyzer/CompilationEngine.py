import os
import xml.etree.ElementTree as ET

from Tokenizer import _keyword, _symbol, _tokenType

_op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

_statements_type = ['let', 'if', 'while', 'do', 'return']

_keyword_constant = ['true', 'false', 'null', 'this']

class CompilationEngine():
    def __init__(self, Etree):
        if type(Etree) != ET.ElementTree:
            raise TypeError('Please construct with an ElementTree object')
        self.srcTree = Etree
        self.e_lst = list(Etree.getroot().iter())
        self.idx = 1 #start from 1 for skip <token>

        self.desRoot = ET.Element('')
        self.desTree = ET.ElementTree(self.desRoot)
        self.cur_root = self.desRoot

    def func_msg(func, *args, **kwargs):
        def wrap(*args, **kwargs):
            print('INTO {}'.format(func.__name__))
            func(*args, **kwargs)
        return wrap

    @func_msg
    def CompileClass(self, parent):
        parent.append(ET.Element('class'))
        root = self._get_last_child(parent)
        self._eat('class', root)
        self._eat('CONST', root)#class name
        self._eat('{', root)
        if self._get_cur_src_element().text in ['static', 'field']:
            self.CompileClassVarDec(root)
        if self._get_cur_src_element().text in ['constructor', 'function', 'method']:
            self.CompileSubroutineDec(root)
        self._eat('}', root)

    @func_msg
    def CompileClassVarDec(self, parent):
        parent.append(ET.Element('classVarDec'))
        root = self._get_last_child(parent)
        self._eat('CONST', root)#type
        self._eat('CONST', root)#varName
        while self._get_next_src_element().text == ',':
            self._eat(',', root)
            self._eat('CONST', root)#varName
        self._eat(';', root)

    @func_msg
    def CompileSubroutineDec(self, parent):
        parent.append(ET.Element('subroutineDec'))
        root = self._get_last_child(parent)
        self._eat('CONST', root)#('constructor' | 'function' | 'method')
        self._eat('CONST', root)#('void" | type)
        self._eat('CONST', root)#subroutineName
        self._eat('(', root)
        self.CompileParameterList(root)
        self._eat(')', root)
        self.CompileSubroutineBody(root)

    @func_msg
    def CompileParameterList(self, parent):
        parent.append(ET.Element('parameterList'))
        root = self._get_last_child(parent)
        while self._get_next_src_element().tag == 'keyword':
            self._eat('CONST', root)#type
            self._eat('CONSt', root)#varName
            if self._get_next_src_element().text == ',':
                self._eat(',', root)

    @func_msg
    def CompileSubroutineBody(self, parent):
        parent.append(ET.Element('subroutineBody'))
        root = self._get_last_child(parent)
        self._eat('{', root)
        while self._get_cur_src_element().text == 'var':
            self.CompileVarDec(root)
        self.CompileStatements(root)
        self._eat('}', root)

    @func_msg
    def CompileVarDec(self, parent):
        parent.append(ET.Element('varDec'))
        root = self._get_last_child(parent)
        self._eat('var', root)
        self._eat('CONST', root)#type
        self._eat('CONST', root)#varName
        while self._get_cur_src_element().text == ',':
            self._eat(',', root)
            self._eat('CONST', root)#varName
        self._eat(';', root)

    @func_msg
    def CompileStatements(self, parent):
        parent.append(ET.Element('statements'))
        root = self._get_last_child(parent)
        while(True):
            stateType = self._get_cur_src_element().text
            if stateType == 'let':
                self.CompileLet(root)
            elif stateType == 'if':
                self.CompileIf(root)
            elif stateType == 'while':
                self.CompileWhile(root)
            elif stateType == 'do':
                self.CompileDo(root)
            elif stateType == 'return':
                self.CompileReturn(root)
            else:
                print("[CompileStatements error] invalid state type: {}, index: {}".format(stateType, self.idx))
                exit()

            if self._get_cur_src_element().text not in _statements_type:
                break

    @func_msg
    def CompileLet(self, parent):
        parent.append(ET.Element('LetStatement'))
        root = self._get_last_child(parent)
        self._eat('let', root)
        self._eat('CONST', root)#varName
        if self._get_cur_src_element().text == '[':
            self._eat('[', root)
            self.CompileExpression(root)
            self._eat(']', root)
        self._eat('=', root)
        self.CompileExpression(root)
        self._eat(';', root)

    @func_msg
    def CompileIf(self, parent):
        parent.append(ET.Element('IfStatement'))
        root = self._get_last_child(parent)
        self._eat('if', root)
        self._eat('(', root)
        self.CompileExpression(root)
        self._eat(')', root)
        self._eat('{', root)
        self.CompileStatements(root)
        self._eat('}', root)

        if self._get_next_src_element().text == 'else':
            self._eat('(', root)
            self.CompileStatements(root)
            self._eat(')', root)

    @func_msg
    def CompileWhile(self, parent):
        parent.append(ET.Element('whileStatement'))
        root = self._get_last_child(parent)
        self._eat('while', root)
        self._eat('(', root)
        self.CompileExpression(root)
        self._eat(')', root)
        self._eat('{', root)
        self.CompileStatements(root)
        self._eat('}', root)


    @func_msg
    def CompileDo(self, parent):
        parent.append(ET.Element('doStatement'))
        root = self._get_last_child(parent)
        self._eat('do', root)

        self._compileSubroutineCall(root)

        self._eat(';', root)

    @func_msg
    def CompileReturn(self, parent):
        parent.append(ET.Element('returnStatement'))
        root = self._get_last_child(parent)
        self._eat('retrun', root)
        if self._get_next_src_element().text != ';':
            self.CompileExpression(root)
        self._eat(';', root)

    @func_msg
    def CompileExpression(self, parent):
        parent.append(ET.Element('expression'))
        root = self._get_last_child(parent)
        self.CompileTerm(root)
        while self._get_cur_src_element().text in _op:
            self._eat(self._get_cur_src_element().text, root)
            self.CompileTerm(root)

    @func_msg
    def CompileTerm(self, parent):
        parent.append(ET.Element('term'))
        root = self._get_last_child(parent)
        e = self._get_cur_src_element()
        if e.tag in ['integerConstant', 'stringConstant']:
            self._eat('CONST', root)
        elif e.text in ['true', 'false', 'null', 'this']:
            self._eat('CONST', root)
        elif e.tag == 'identifier' and self._get_next_src_element().text != '.':
            #varName | varName['expression']
            print("***varName***")
            self._eat('CONST', root)
            if self._get_cur_src_element().text == '[':
                self._eat('[', root)
                self.CompileExpression(root)
                self._eat(']', root)
        elif e.tag == 'identifier':
            self._compileSubroutineCall(root)
        elif e.text == '(':
            self._eat('(', root)
            self.CompileExpression(root)
            self._eat(')', root)
        elif e.text in _op:
            self._eat('CONST', root)#unaryOp
            self.CompileTerm(root)
        else:
            print('CompileTerm Error: not comply compile term rule, index: {}, tag: {}, text'
            .format(self.idx, e.tag, e.text))
            exit()
    
    @func_msg
    def CompileExpressionList(self, parent):
        parent.append(ET.Element('expressionList'))
        root = self._get_last_child(parent)
        self.CompileExpression(root)

        while self._get_next_src_element().text == ',':
            self.CompileExpression(root)

    #This function is not defined in lecture API, but I think implement this function is better solution
    def _compileSubroutineCall(self, parent):
            print("***subroutineCall***")
            self._eat('CONST', parent)#subroutineName
            if self._get_cur_src_element().text == '(':
                self._eat('(', parent)
                self.CompileExpressionList(parent)
                self._eat(')', parent)
            elif self._get_cur_src_element().text == '.':
                print("** DOT **")
                self._eat('.', parent)
                self._eat('CONST', parent)#subroutineName
                self._eat('(', parent)
                self.CompileExpressionList(parent)
                self._eat(')', parent)

    def _eat(self, text, root):
        #check if current element is comply the grammer
        #the append this element to current root
        e = self._get_cur_src_element()
        if text == 'CONST':
            root.append(e)
            self.idx += 1 #advance
        else:
            if e.text != text:
                print('_eat Error at line: {}, expect text: {}, src text: {}'.format(self.idx+1, text, self._get_cur_src_element().text) )
                exit()
            else:
                root.append(e)
                self.idx += 1 #advance
        print("idx: {}, tag: {}, text: {}".format(self.idx, e.tag, e.text))

    def _get_cur_src_element(self):
        return self.e_lst[self.idx]

    def _get_next_src_element(self):
        return self.e_lst[self.idx + 1]

    def _get_last_child(self, e):
        #print("-- " , e.tag, e.text, e.findall('*'))
        return e.findall('*')[-1]

    def _get_parnet(self):
        pass


if __name__ == '__main__':
    path = os.path.join('..', 'ArrayTest')
    srcName = 'MainT2.xml'
    tree = ET.ElementTree(file=os.path.join(path, srcName))
    engine = CompilationEngine(tree)
    engine.CompileClass(engine.desRoot)

    desName = srcName.split('T2.xml')[0] + 'T3.xml'
    engine.desTree.write(os.path.join(path, desName))