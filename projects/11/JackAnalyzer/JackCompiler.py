import sys, os, json
import xml.etree.ElementTree as ET
import JackAnalyzer, CompilationEngine, SymbolTable

class JackCompiler():
    def __init__(self):
        pass

    def compile(self, path):
    #prcess the pretty print xml file that generated by CompilationEngine
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(CompilationEngine.PRETTY_PRINT_FILE):
                    print('Convert xml to vm code: {}'.format(os.path.join(path, filename)))
                    self._process_xml_file(os.path.join(path, filename))
        elif os.path.isfile(path):
            path = path.replace('.jack', CompilationEngine.PRETTY_PRINT_FILE)
            if not os.path.isfile(path):
                print('Can not find {}'.format(path))
                exit()
            print('Convert xml to vm code: {}'.format(path))
            self._process_xml_file(path)
        else:
            print("'{}' is not a valid path".format(path))

    def _process_xml_file(self, src):
        src_tree = ET.ElementTree(file=src)
        table = SymbolTable.SymbolTable()

        print('---------global table------------')
        self._build_global_table(src_tree, table)
        print(json.dumps(table.table ,sort_keys=True, indent=4))

        subroutineDecs = src_tree.findall('./subroutineDec')
        className = src_tree.findall('./')[1].text
        for dec in subroutineDecs:
            print('---------local table: {}------------'.format(dec.findall('./')[2].text))
            self._build_local_table(dec, table, className)
            print(json.dumps(table.subroutine_table.table ,sort_keys=True, indent=4))

        #TODO: generate vm code

    def _build_global_table(self, src_tree, table):
        classVarDec = src_tree.findall('./classVarDec')
        for e in classVarDec:
            dec = e.findall('./')
            idx = 2
            while idx < len(dec):
                table.define(dec[idx].text, dec[1].text, dec[0].text)
                idx += 2

    def _build_local_table(self, dec_tree, table, className):
        #Add this to subroutine table
        table.define('this', className,'arg')
        for e in dec_tree:
            #TODO: add parameters to subroutine table
            parameters = e.findall('./parameterList')
            print(parameters)
            if parameters:
                idx = 0
                while idx < len(parameters):
                    table.define(parameters[idx+1].text, parameters[idx].text, 'arg')
                    idx += 3
            #TODO: add variables to subroutine table
            variables = e.findall('./varDec/')
            if variables:
                idx = 0
                while idx < len(parameters):
                    table.define(parameters[idx+1].text, parameters[idx].text, 'arg')
                    idx += 3

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python JackAnalyzer.py PATH')
        exit()

    path = sys.argv[1]
    jackAnlyzr = JackAnalyzer.JackAnalyzer()
    jackAnlyzr.read_file_or_dir(path)

    jackCompiler = JackCompiler()
    jackCompiler.compile(path)