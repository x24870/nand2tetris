from vmParser import Parser
from codeWriter import CodeWriter

filename = '../MemoryAccess/BasicTest/BasicTest.vm'
parser_ = Parser()
parser_.read_file(filename)
parser_.parse_vm_code()
parser_.close_file()

codeWriter = CodeWriter()
codeWriter.gen_hack_code(parser_.lines)
codeWriter.write_to_file(filename.split('.vm')[0] + '.asm')