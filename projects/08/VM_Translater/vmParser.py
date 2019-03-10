class Parser():
    def __init__(self):
        self.f = None
        self.lines = []

    def read_file(self, filename):
        try:
            self.f = open(filename, 'r')
        except:
            print("Can't open '{}'".format(filename))
        return

    def close_file(self):
        self.f.close()

    def parse_vm_code(self):
        for line in self.f.readlines():
            line = line.split('\n')[0]
            if not line.startswith('//') and line:
                self.lines.append(line)

def test():
    print('asdasd')

if __name__ == "__main__":
    parser = Parser()
    parser.read_file('../MemoryAccess/BasicTest/BasicTest.vm')
    parser.parse_vm_code()
    parser.close_file()