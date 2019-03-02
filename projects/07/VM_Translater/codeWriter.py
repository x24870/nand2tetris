from vmParser import Parser

RAM_ADDR_DEFINE = {
    'local': '300',
    'argument': '400',
    'this': '3000',
    'that': '3010',
}

class codeWriter():
    def __init__(self):
        self.vm_code = []
        self.if_count = 0

    def gen_hack_code(self, lines):
        for line in lines:
            line = line.split()#type list
            if len(line) == 1:
                #arithmetic instruction
                self._arithmetic_code(line[0])
            else:
                #memory instruction
                self._mem_seg_code(line)

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            for line in self.vm_code:
                f.write(line + '\n')

    def _arithmetic_code(self, line):
        self.vm_code.append('//' + line)
        if line == 'add':
            self.vm_code.append('@0')
            self.vm_code.append('A=M-1')
            self.vm_code.append('D=M')
            self.vm_code.append('A=A-1')
            self.vm_code.append('M=M+D')
            self.vm_code.append('@0')
            self.vm_code.append('M=M-1')
        elif line == 'sub':
            self.vm_code.append('@0')
            self.vm_code.append('A=M-1')
            self.vm_code.append('D=M')
            self.vm_code.append('A=A-1')
            self.vm_code.append('M=M-D')
            self.vm_code.append('@0')
            self.vm_code.append('M=M-1')
        elif line == 'neg':
            self.vm_code.append('@0')
            self.vm_code.append('A=M-1')
            self.vm_code.append('M=-M')
        elif line in ['eq', 'gt', 'lt']:
            #x = x - y
            self.vm_code.append('@0')
            self.vm_code.append('A=M-1')
            self.vm_code.append('D=M')
            self.vm_code.append('A=A-1')
            self.vm_code.append('D=M-D')
            #if x == 0 jump to (IF) else jump to (ELSE)
            #then both of these two result will jump to (ENDIF)
            self.vm_code.append('@IF' + str(self.if_count))
            if line == 'eq':
                self.vm_code.append('D;JEQ')
            elif line == 'gt':
                self.vm_code.append('D;JGT')
            elif line == 'lt':
                self.vm_code.append('D;JLT')
            self.vm_code.append('@ELSE' + str(self.if_count))
            self.vm_code.append('0;JMP')
            #IF
            self.vm_code.append('(IF' + str(self.if_count) + ')')
            self.vm_code.append('@0')
            self.vm_code.append('A=M-1')#pop 2 times
            self.vm_code.append('A=A-1')
            self.vm_code.append('M=-1')
            self.vm_code.append('@ENDIF' + str(self.if_count))
            self.vm_code.append('0;JMP')
            #ELSE
            self.vm_code.append('(ELSE' + str(self.if_count) + ')')
            self.vm_code.append('@0')
            self.vm_code.append('A=M-1')#pop 2 times
            self.vm_code.append('A=A-1')
            self.vm_code.append('M=0')
            self.vm_code.append('@ENDIF' + str(self.if_count))
            self.vm_code.append('0;JMP')
            #ENDIF SP--
            self.vm_code.append('(ENDIF' + str(self.if_count) + ')')
            self.vm_code.append('@0')
            self.vm_code.append('M=M-1')
            self.if_count += 1
        elif line == 'and':
            self.vm_code.append('@0')
            self.vm_code.append('A=M-1')
            self.vm_code.append('D=M')
            self.vm_code.append('A=A-1')
            self.vm_code.append('M=D&M')
            self.vm_code.append('@0')
            self.vm_code.append('M=M-1')
        elif line == 'or':
            self.vm_code.append('@0')
            self.vm_code.append('A=M-1')
            self.vm_code.append('D=M')
            self.vm_code.append('A=A-1')
            self.vm_code.append('M=D|M')
            self.vm_code.append('@0')
            self.vm_code.append('M=M-1')
        elif line == 'not':
            self.vm_code.append('@0')
            self.vm_code.append('A=M-1')
            self.vm_code.append('M=!M')

    def _mem_seg_code(self, line):
        self.vm_code.append('//' + ' '.join(line))
        if line[1] in ['local', 'argument', 'this', 'that']:
            self._seg_lcl_arg_this_that(line[0], RAM_ADDR_DEFINE[line[1]], line[2])
        elif line[1] == 'constant':
            self._seg_constant(line[2])
        elif line[1] == 'static':
            self._seg_static(line[0], line[2])
        elif line[1] == 'pointer':
            pass
        elif line[1] == 'temp':
            self._seg_temp(line[0], line[2])
        #print(self.vm_code)

    def _seg_lcl_arg_this_that(self, action, mem_seg, index):
        if action == 'push':
            #addr = mem_seg + index
            if index == '0':
                self.vm_code.append('@' + mem_seg)
                self.vm_code.append('A=M')
            else:
                self.vm_code.append('@' + index)
                self.vm_code.append('D=A')
                self.vm_code.append('@' + mem_seg)
                self.vm_code.append('D=D+M')
                self.vm_code.append('A=D')
            self.vm_code.append('D=M')#*SP
            #*SP = *addr
            self.vm_code.append('@0')
            self.vm_code.append('A=M')
            self.vm_code.append('M=D')
            #SP++
            self.vm_code.append('@0')
            self.vm_code.append('M=M+1')
        elif action == 'pop':
            #addr = mem_seg + index
            if index == '0':
                self.vm_code.append('@' + mem_seg)
                self.vm_code.append('D=A')
            else:
                self.vm_code.append('@' + index)
                self.vm_code.append('D=A')
                self.vm_code.append('@' + mem_seg)
                self.vm_code.append('D=D+M')
            #Store addr in R13 temperary(R13, R14, R15 are reserved for generate asm code)
            self.vm_code.append('@R13')
            self.vm_code.append('M=D')
            #SP--
            self.vm_code.append('@0')
            self.vm_code.append('M=M-1')
            self.vm_code.append('A=M')#SP
            self.vm_code.append('D=M')#*SP
            #*addr = *SP
            self.vm_code.append('@R13')
            self.vm_code.append('A=M')#addr
            self.vm_code.append('M=D')
            
    def _seg_constant(self, constant):
        #constant only allow push
        #addr = constant
        self.vm_code.append('@' + constant)
        self.vm_code.append('D=A')
        #*SP = addr
        self.vm_code.append('@0')
        self.vm_code.append('A=M')
        self.vm_code.append('M=D')
        #SP++
        self.vm_code.append('@0')
        self.vm_code.append('M=M+1')

    def _seg_static(self, action, index):
        #Regardint to pop action, I didn't follow the advise in lecture
        #Because I think my way is more elegant
        TEMP_STATIC_ADDR = 16
        if action == 'push':
            #addr = static + index
            self.vm_code.append('@' + str(TEMP_STATIC_ADDR + int(index)))
            self.vm_code.append('D=M')
            #*SP = *addr
            self.vm_code.append('@0')
            self.vm_code.append('A=M')
            self.vm_code.append('M=D')
            #SP++
            self.vm_code.append('@0')
            self.vm_code.append('M=M+1')
        elif action == 'pop':
            #SP--
            self.vm_code.append('@0')
            self.vm_code.append('M=M-1')
            self.vm_code.append('A=M')
            self.vm_code.append('D=M')#*SP
            #*addr = *SP
            self.vm_code.append('@' + str(TEMP_STATIC_ADDR + int(index)))
            self.vm_code.append('M=D')

    def _seg_pointer(self, action, index):
        if action == 'push':
            #*SP = this/that
            self.vm_code.append('@this') if index == '0' else self.vm_code.append('@that')
            self.vm_code.append('D=A')
            self.vm_code.append('@0')
            self.vm_code.append('M=D')
            #SP++
            self.vm_code.append('@0')
            self.vm_code.append('M=M+1')
        elif action == 'pop':
            #SP--
            self.vm_code.append('@0')
            self.vm_code.append('M=M-1')
            self.vm_code.append('A=M')
            self.vm_code.append('D=M')#*SP
            #this/that = *SP
            self.vm_code.append('@this') if index == '0' else self.vm_code.append('@that')
            self.vm_code.append('M=D')

    def _seg_temp(self, action, index):
        #Regardint to pop action, I didn't follow the advise in lecture
        #Because I think my way is more elegant
        TEMP_TEMP_ADDR = 5
        if action == 'push':
            #addr = static + index
            self.vm_code.append('@' + str(TEMP_TEMP_ADDR + int(index)))
            self.vm_code.append('D=M')
            #*SP = *addr
            self.vm_code.append('@0')
            self.vm_code.append('A=M')
            self.vm_code.append('M=D')
            #SP++
            self.vm_code.append('@0')
            self.vm_code.append('M=M+1')
        elif action == 'pop':
            #SP--
            self.vm_code.append('@0')
            self.vm_code.append('M=M-1')
            self.vm_code.append('A=M')
            self.vm_code.append('D=M')#*SP
            #*addr = *SP
            self.vm_code.append('@' + str(TEMP_TEMP_ADDR + int(index)))
            self.vm_code.append('M=D')

if __name__ == "__main__":
    filename = '../StackArithmetic/StackTest/StackTest.vm'
    parser_ = Parser()
    parser_.read_file(filename)
    parser_.parse_vm_code()
    parser_.close_file()

    codeWriter = codeWriter()
    codeWriter.gen_hack_code(parser_.lines)
    codeWriter.write_to_file(filename.split('.vm')[0] + '.asm')