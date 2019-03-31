import os, sys, subprocess
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
            block_comment = False
            for line in f.readlines():
                line, block_comment = self._remove_comment_and_space(line, block_comment)

                if line:
                    code_stream += line
            tknzr = Tokenizer(code_stream)
            Etree = tknzr.process_code() #retrun a ElementTree
            
            current_dir = os.path.dirname(path)
            filename = os.path.basename(path).split('.jack')[0] + 'T2.xml'
            self._write_to_file(os.path.join(current_dir, filename), Etree)

    def _remove_comment_and_space(self, line, block_comment):
        if block_comment:
            idx = line.find('*/')
            if idx == -1:
                return '', True
            return line[idx+2:-1], False

        line = line.strip()

        idx_start = line.find('/*')
        if idx_start != -1:
            #check if */ is in same line
            idx_end = line.find('*/')
            if idx_end != -1:
                line = line[:idx_start] + line[idx_end+2:]
            else:
                #not find */ in small line
                line = line[:idx_start]
                block_comment = True

        idx = line.find('//')
        if idx != -1:
            line = line[:idx]

        return line, block_comment

    def _write_to_file(self, path, Etree):
        #Etree.write(path, short_empty_elements=False, pretty_print=True)
        xmlstr = minidom.parseString(ET.tostring(Etree.getroot())).toprettyxml(indent='')
        #remove xml version
        first_nl = xmlstr.find('\n')
        xmlstr = xmlstr[first_nl+1:]

        with open(path, 'w') as f:
            f.write(xmlstr)

if __name__ == '__main__':
    path = sys.argv[1]
    jackAnlyzr = JackAnalyzer()
    jackAnlyzr.read_file_or_dir(path)

    #NOTE: pleas execute this script in nand2tetris/project/10/
    compare_bat_path = os.path.join('..', '..', 'tools', 'TextComparer.bat')
    if os.path.isfile(sys.argv[1]):
        comp_src = sys.argv[1].split('.jack')[0] + 'T.xml'
        comp_des = sys.argv[1].split('.jack')[0] + 'T2.xml'
        print("\n*** Comparing '{}', '{}' ...".format(comp_src, comp_des))
        subprocess.call([compare_bat_path, comp_src, comp_des])
    elif os.path.isdir(sys.argv[1]):
        for f in os.listdir(sys.argv[1]):
            if f.endswith('.jack'):
                comp_src = os.path.join(sys.argv[1], f.split('.jack')[0] + 'T.xml')
                comp_des = os.path.join(sys.argv[1], f.split('.jack')[0] + 'T2.xml')
                print("\n*** Comparing '{}', '{}' ...".format(comp_src, comp_des))
                subprocess.call([compare_bat_path, comp_src, comp_des])
