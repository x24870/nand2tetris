import preDefine

class hackAssembler():
    def __init__(self):
        self.asm_content = []
        self.machine_code = []
        self.filename = ''

    def first_pass():
    #Convert the .asm file to symbol-less assembler language
        pass

    def second_pass(self):
    #Convert the symbol-less assmebler language to machine code
        for line in self.asm_content:
            if line[0] == '@':
                instruction = self.convert_A_instruction(line)
                self.machine_code.append(instruction)
            else:
                instruction = self.convert_C_instruction(line)
                self.machine_code.append(instruction)

    def convert_A_instruction(self, instruction):
        address = instruction.split('@')[1]
        address = str(bin(int(address)))
        address = address.split('b')[1]
        fill_zero = 16 - len(address)#include first bit
        instruction = '0' * fill_zero + address
        return instruction


    def convert_C_instruction(self, instruction):
        #print(instruction)
        dest_and_comp = instruction.split('=')
        if len(dest_and_comp) < 2:
            comp_and_jump = instruction.split(';')
            #print(comp_and_jump)
            comp = preDefine.comp[comp_and_jump[0]]
            jump = preDefine.jump[comp_and_jump[1]]
            #print('{}, {}'.format(comp, jump))
            instruction = '111' + comp + '000' + jump
        else:
            #print(dest_and_comp)
            dest = preDefine.dest[dest_and_comp[0]]
            comp = preDefine.comp[dest_and_comp[1]]
            #print('{}, {}'.format(dest, comp))
            instruction = '111' + comp + dest + '000'
        #print('-----------------------------')
        return instruction

    def read_asm_file(self, filename):
        self.filename = filename
        try:
            f = open(filename, 'r')
            self.asm_content = f.readlines()
        except:
            print("Can't open '{}'".format(filename))
            return

        f.close()

        self.remove_comment_and_white()

    def remove_comment_and_white(self):
        new_asm = []
        for line in self.asm_content:
            line = line.split('\n')[0];
            line = line.split('//')[0];
            line = line.strip()
            if line:
                new_asm.append(line)
                #print(repr(line))
        self.asm_content = new_asm

    def output_machine_code(self):
        filename = self.filename.split('.asm')[0] + '.hack'
        with open(filename, 'w') as f:
            for line in self.machine_code:
                f.write(line+'\n')

if __name__ == "__main__":
    asm = hackAssembler()
    asm.read_asm_file('max/MaxL.asm')
    asm.second_pass()
    asm.output_machine_code()