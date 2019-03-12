import os

class Parser():
    def __init__(self):
        self.lines = []

    def read(self, dir):
        if os.path.isdir(dir):
            for f in os.listdir(dir):
                if f.endswith('.vm'):
                    self._read_file(os.path.join(dir, f))
        elif os.path.isfile(dir):
            self._read_file(dir)
        else:
            print('Error: invalid directory: {}'.format(dir))

    def _read_file(self, filename):
        try:
            f = open(filename, 'r')
            self._parse_vm_code(f)
        except:
            print("Read file error: '{}'".format(filename))
        finally:
            f.close()
        return

    def _parse_vm_code(self, f):
        for line in f.readlines():
            line = line.split('\n')[0]
            if not line.startswith('//') and line:
                self.lines.append(line)


if __name__ == "__main__":
    parser_ = Parser()

    #parse single file
    dir = os.path.join('..', 'ProgramFlow', 'BasicLoop', 'BasicLoop.vm')
    parser_.read(dir)

    #parse directory
    dir = os.path.join('..', 'FunctionCalls', 'FibonacciElement')
    parser_.read(dir)