import os

class VMWriter():
    def __init__(self, output_file):
        self.fp = open(output_file, 'w')

    def close(self):
        self.fp.close()

    def writePush(self, segment, index):
        self.fp.write('push {} {}'.format(segment, index))

    def writePop(self, segment, index):
        pass

    def writeArithmetic(self, command):
        if command == '+':
            self.fp.write('add\n')
        elif command == '-':
            self.fp.write('sub\n')
        elif command == '*':
            self.fp.write('call Math.multiply 2\n')


    def writeLabel(self, label):
        pass

    def writeGoto(self, label):
        pass

    def writeIf(self, label):
        pass

    def writeCall(self, name, nArgs):
        self.fp.write('call {} {}'.format(name, nArgs))

    def writeFunction(self, name, nLocals):
        self.fp.write('function {} {}\n'.format(name, nLocals))

    def writeReturn(self):
        pass



if __name__ == '__main__':
    vmWriter = VMWriter('./text.txt')
    vmWriter.close()

