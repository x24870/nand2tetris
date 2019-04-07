import os
import xml.etree.ElementTree as ET

from Tokenizer import _keyword, _symbol, _tokenType

_op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

_statements_type = ['let', 'if', 'while', 'do', 'return']

class CompilationEngine():
    def __init__(self, Etree):
        if type(Etree) != ET.ElementTree:
            raise TypeError('Please construct with an ElementTree object')
        self.srcTree = Etree
        self.e_lst = list(Etree.getroot().iter())
        self.idx = 1 #skip <token>

        self.desRoot = ET.Element('')
        self.desTree = ET.ElementTree(self.desRoot)
        self.cur_root = self.desRoot


    def CompileClass(self):
        pass

    def CompileClassVarDec(self):
        pass

    def CompileSubroutineDec(self):
        pass

    def CompileParameterList(self):
        pass

    def CompileSubroutineBody(self):
        pass

    def CompileVarDec(self):
        pass

    def CompileStatements(self, parent):
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
                print("[CompileStatements error] invalid state type: {}".format(stateType))
                exit()

            if stateType = self._get_cur_src_element().text not in _statements_type:
                break

    def CompileLet(self, parent):
        root = self._get_last_child(parent)
        self._eat('let', root)
        self.CompileVarName()
        self._eat('=', root)
        self.CompileExpression(self, root)
        self._eat(';', root)

    def CompileIf(self, parent):
        pass

    def CompileWhile(self, parent):
        #self._add_child(whileStatement)
        parent.append(ET.Element('whileStatement'))
        root = self._get_last_child(parent)
        self._eat('while', root)
        self._eat('(', root)
        self.CompileExpression(root)
        self._eat(')', root)
        self._eat('{', root)
        self.CompileStatements()
        self._eat('}', root)


    def CompileDo(self, parent):
        pass

    def CompileReturn(self, parent):
        pass

    def CompileExpression(self, parent):
        parent.append(ET.Element('expression'))
        root = self._get_last_child(parent)
        self.CompileTerm(root)

        if self._get_next_src_element().tag in _op:
            self._eat(self._get_next_src_element().text, root)
            self.CompileTerm(root)

    def CompileTerm(self, parent):
        parent.append(ET.Element('term'))
        root = self._get_last_child(parent)
        #TODO: deal with term
    
    def CompileExpressionList(self):
        pass

    def CompileVarName(self, parent):
        #TODO: ('['expression']')?
        pass

    def _eat(self, text, root):
        #check if current element is comply the grammer
        #the append this element to current root
        e = self._get_cur_src_element()
        if e.text != text:
            print('Error: At line: {}, expect text: {}'.format(self.idx+1, text))
        else:
            root.append(e)
            self.idx += 1 #advance

    def _get_cur_src_element(self):
        return self.e_lst[self.idx]

    def _get_next_src_element(self):
        return self.e_lst[self.idx + 1]

    def _get_last_child(self, e):
        return e.findall('*')[-1]

    def _get_parnet(self):
        pass


if __name__ == '__main__':
    path = os.path.join('..', 'ArrayTest')
    srcName = 'testT2.xml'
    tree = ET.ElementTree(file=os.path.join(path, srcName))
    engine = CompilationEngine(tree)
    engine.CompileWhile(engine.desRoot)

    desName = srcName.split('T2.xml')[0] + 'T3.xml'
    engine.desTree.write(os.path.join(path, desName))