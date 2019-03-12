import os
from vmParser import Parser
from codeWriter import CodeWriter

path = os.path.join('..', 'FunctionCalls', 'FibonacciElement')
#path = os.path.join('..', 'ProgramFlow', 'BasicLoop', 'BasicLoop.vm')
parser_ = Parser()
parser_.read(path)

codeWriter = CodeWriter()
codeWriter.gen_hack_code(parser_.lines)
codeWriter.write_to_file(path)