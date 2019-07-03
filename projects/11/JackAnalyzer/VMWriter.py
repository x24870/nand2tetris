import os

class VMWriter():
    def __init__(self, output_file):
        self.fp = open(output_file, 'w')

    def close(self):
        self.fp.close()

    def writePusn(self, segment, index):
        pass

    def writePop(self, segment, index):
        pass

    def writeArithmetic(self, command):
        pass

    def writeLabel(self, label):
        pass

    def writeGoto(self, label):
        pass

    def writeIf(self, label):
        pass

    def writeCall(self, name, nArgs):
        pass

    def writeFunction(self, name, nLocals):
        return 'function {} {}'.format(name, nLocals)

    def writeReturn(self):
        pass

    def gen_vm_code(self, classNmae, tree):
        for e in tree.iter():
            print(e.text)

if __name__ == '__main__':
    vmWriter = VMWriter('./text.txt')
    vmWriter.close()

