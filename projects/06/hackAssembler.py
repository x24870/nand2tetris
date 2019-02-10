import preDefine

class hackAssembler():
    def __init__(self):
        self.asm_content = []
        self.machine_code = []
        self.filename = ''
        self.symbol_table = preDefine.symbol_table

    def first_pass(self):
    #Add lables to symbol table and remove labels from asm code
        label_num = -1
        label_less_asm = []
        for idx, line in enumerate(self.asm_content):
            #print(idx, line)
            if line.startswith('('):
                label = line.strip('()')
                label_num = label_num + 1
                self.symbol_table[label] = idx - label_num
                #print(label, self.symbol_table[label])
            else:
                label_less_asm.append(line)
        self.asm_content = label_less_asm


    def second_pass(self):
    #Add variables to symbol table and translate vriables and labels to value
        var_val = 16
        var_less_asm = []
        for line in self.asm_content:
            if line.startswith('@'):
                line = line.strip('@')
                if line.isdigit():
                    line = '@' + line
                elif line not in self.symbol_table:
                    self.symbol_table[line] = var_val
                    var_val = var_val + 1
                    line = '@' + str(self.symbol_table[line])
                else:
                    line = '@' + str(self.symbol_table[line])
            var_less_asm.append(line)
        self.asm_content = var_less_asm

    def generate_machine_code(self):
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
    print('''
    Usage: 
    A. Symbol less asm file:
        1. Init an hackAssembler
        2. read_asd_file()
        3. generate_machine_code()
        4. output_machine_code

    B. Asm file with symbol
        1. Init an hackAssembler
        2. read_asd_file()
        3. first_pass()
        4. second_pass()
        5. generate_machine_code()
        6. output_machine_code
    ''')

    
    asm = hackAssembler()
    asm.read_asm_file('pong/PongL.asm')
    asm.generate_machine_code()
    asm.output_machine_code()
    
    asm = hackAssembler()
    asm.read_asm_file('pong/Pong.asm')
    asm.first_pass()
    asm.second_pass()
    asm.generate_machine_code()
    asm.output_machine_code()