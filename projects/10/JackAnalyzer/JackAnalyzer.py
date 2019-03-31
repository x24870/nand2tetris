import os

import xml.etree.ElementTree as ET

from Tokenizer import Tokenizer
from xml.dom import minidom

class JackAnalyzer():
    def __init__(self):
        pass
        
    def read_file_or_dir(self, path):
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith('.jack'):
                    self._process_file(os.path.join(path, filename))

        elif os.path.isfile(path):
            filename = os.path.basename(path)
            if not filename.endswith('.jack'):
                print('{} is not a jack file'.format(filename))
                exit()
            self._process_file(path)
        else:
            print("'{}' is not a valid path".format(path))
            
    def _process_file(self, path):
        code_stream = ''
        with open(path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if not line.startswith('/') and line:
                    code_stream += line
            tknzr = Tokenizer(code_stream)
            Etree = tknzr.process_code() #retrun a ElementTree
            
            current_dir = os.path.dirname(path)
            filename = os.path.basename(path).split('.jack')[0] + 'T2.xml'
            self._write_to_file(os.path.join(current_dir, filename), Etree)

    def _write_to_file(self, path, Etree):
        #Etree.write(path, short_empty_elements=False, pretty_print=True)
        xmlstr = minidom.parseString(ET.tostring(Etree.getroot())).toprettyxml(indent='')
        #remove xml version
        first_nl = xmlstr.find('\n')
        xmlstr = xmlstr[first_nl+1:]

        with open(path, 'w') as f:
            f.write(xmlstr)

if __name__ == '__main__':
    jackAnlyzr = JackAnalyzer()
    jackAnlyzr.read_file_or_dir(os.path.join( 'ArrayTest', 'Main.jack'))