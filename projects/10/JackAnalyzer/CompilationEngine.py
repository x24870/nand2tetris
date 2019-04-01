import xml.etree.ElementTree as ET

class CompilationEngine():
    def __init__(self, Etree):
        if type(Etree) != ET.ElementTree:
            raise TypeError('Please construct with an ElementTree object')
        self.srcTree = Etree
        self.desTree = ET.ElementTree(ET.Element('class'))

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

    def CompileStatements(self):
        pass

    def CompileLet(self):
        pass

    def CompileIf(self):
        pass

    def CompileWhile(self):
        pass

    def CompileDo(self):
        pass

    def CompileReturn(self):
        pass

if __name__ == '__main__':
    tree = ET.ElementTree()
    engine = CompilationEngine(tree)