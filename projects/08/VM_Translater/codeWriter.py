import os
from vmParser import Parser

RAM_ADDR_DEFINE = {
    'local': '1',
    'argument': '2',
    'this': '3',
    'that': '4',
}

class CodeWriter():
    def __init__(self):
        self.vm_code = []
        self.if_count = 0
        self.label_table = {}
        self._asm_ignored_line_count = 0

    def gen_hack_code(self, lines, gen_init_code):
        if gen_init_code:
            self._add_asm_comment('Initialize')
            self._call_code('call Sys.init 0'.split())

        for line in lines:
            line = line.split()#type list
            if line[0] in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
                #arithmetic instruction
                self._arithmetic_code(line[0])
            elif line[0] in ['push', 'pop']:
                #memory instruction
                self._mem_seg_code(line)
            elif line[0] == 'label':
                #label
                self._label_code(line)
            elif 'goto' in line[0]:
                #if-goto/goto
                self._goto_if_goto_code(line)
            elif line[0] == 'function':
                #funtion define
                self._function_code(line)
            elif line[0] == 'call':
                #function call
                self._call_code(line)
            elif line[0] == 'return':
                #return
                self._return_code(line)
            else:
                print('Error: unspecified VM code "{}"'.format(' '.join(line)))

    def write_to_file(self, path):
        if os.path.basename(path).endswith('.vm'):
            filename = os.path.basename(path)
            directory = os.path.dirname(path)
            filename = filename.split('.vm')[0] + '.asm'
        else:
            directory = path
            filename = os.path.basename(path) + '.asm'
        path = os.path.join(directory, filename)
        print('Output: {}'.format(path))

        with open(path, 'w') as f:
            for line in self.vm_code:
                f.write(line + '\n')

    def _add_asm_comment(self, comment):
        self.vm_code.append('//' + comment + '  ' + str(len(self.vm_code) - self._asm_ignored_line_count))
        self._asm_ignored_line_count += 1

    def _arithmetic_code(self, line):
        self._add_asm_comment(line)
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
        self._add_asm_comment(' '.join(line))
        if line[1] in ['local', 'argument', 'this', 'that']:
            self._seg_lcl_arg_this_that(line[0], line[1], line[2])
        elif line[1] == 'constant':
            self._seg_constant(line[2])
        elif line[1] == 'static':
            self._seg_static(line[0], line[2])
        elif line[1] == 'pointer':
            self._seg_pointer(line[0], line[2])
        elif line[1] == 'temp':
            self._seg_temp(line[0], line[2])
        #print(self.vm_code)

    def _seg_lcl_arg_this_that(self, action, mem_seg, index):
        if action == 'push':
            #addr = mem_seg + index
            if index == '0':
                self.vm_code.append('@' + RAM_ADDR_DEFINE.get(mem_seg))
                self.vm_code.append('A=M')
            else:
                self.vm_code.append('@' + index)
                self.vm_code.append('D=A')
                self.vm_code.append('@' + RAM_ADDR_DEFINE.get(mem_seg))
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
                self.vm_code.append('@' + RAM_ADDR_DEFINE.get(mem_seg))
                self.vm_code.append('D=M')
            else:
                self.vm_code.append('@' + index)
                self.vm_code.append('D=A')
                self.vm_code.append('@' + RAM_ADDR_DEFINE.get(mem_seg))
                self.vm_code.append('D=D+M')
            #Store addr in R13 temporarily(R13, R14, R15 are reserved for generate asm code)
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
            if index == '0':
                self.vm_code.append('@' + RAM_ADDR_DEFINE.get('this'))
            else:
                self.vm_code.append('@' + RAM_ADDR_DEFINE.get('that'))
            self.vm_code.append('D=M')
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
            #this/that = *SP
            if index == '0':
                self.vm_code.append('@' + RAM_ADDR_DEFINE.get('this'))
            else:
                self.vm_code.append('@' + RAM_ADDR_DEFINE.get('that'))
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

    def _label_code(self, line):
        self._add_asm_comment(' '.join(line))
        self.vm_code.append('(' + line[1] + ')')
        self._asm_ignored_line_count += 1

    def _goto_if_goto_code(self, line):
        self._add_asm_comment(' '.join(line))
        if 'if' in line[0]:
            #SP--
            self.vm_code.append('@0')
            self.vm_code.append('M=M-1')
            self.vm_code.append('A=M')#SP
            self.vm_code.append('D=M')#*SP
            #if
            self.vm_code.append('@' + line[1])
            self.vm_code.append('D;JNE')
        else:
            self.vm_code.append('@' + line[1])
            self.vm_code.append('0;JMP')

    def _function_code(self, line):
        self._add_asm_comment(' '.join(line))
        #(function.label)
        self.vm_code.append('(' + line[1] + ')')
        self._asm_ignored_line_count += 1
        #Initialize local varialble to 0
        for i in range(int(line[2])):
            self._mem_seg_code('push constant 0'.split())
            self._mem_seg_code(('pop local ' + str(i)).split())

    def _call_code(self, line):
        self._add_asm_comment(' '.join(line))
        #*SP=retAddr SP++
        self._add_asm_comment('*SP=retAddr SP++')
        self.vm_code.append('@0')
        self.vm_code.append('D=M')
        for i in range(int(line[2])): self.vm_code.append('D=D-1')
        self.vm_code.append('A=M')
        self.vm_code.append('M=D')
        self.vm_code.append('@0')
        self.vm_code.append('M=M+1')
        #*SP=savedLCL SP++
        self._add_asm_comment('*SP=savedLCL SP++')
        self.vm_code.append('@1')
        self.vm_code.append('D=M')
        self.vm_code.append('@0')
        self.vm_code.append('A=M')
        self.vm_code.append('M=D')
        self.vm_code.append('@0')
        self.vm_code.append('M=M+1')
        #*SP=savedARG SP++
        self._add_asm_comment('*SP=savedARG SP++')
        self.vm_code.append('@2')
        self.vm_code.append('D=M')
        self.vm_code.append('@0')
        self.vm_code.append('A=M')
        self.vm_code.append('M=D')
        self.vm_code.append('@0')
        self.vm_code.append('M=M+1')
        #*SP=savedTHIS SP++
        self._add_asm_comment('*SP=savedTHIS SP++')
        self.vm_code.append('@3')
        self.vm_code.append('D=M')
        self.vm_code.append('@0')
        self.vm_code.append('A=M')
        self.vm_code.append('M=D')
        self.vm_code.append('@0')
        self.vm_code.append('M=M+1')
        #*SP=savedTHAT SP++
        self._add_asm_comment('*SP=savedTHAT SP++')
        self.vm_code.append('@4')
        self.vm_code.append('D=M')
        self.vm_code.append('@0')
        self.vm_code.append('A=M')
        self.vm_code.append('M=D')
        self.vm_code.append('@0')
        self.vm_code.append('M=M+1')
        #ARG
        self._add_asm_comment('ARG')
        self.vm_code.append('@0')
        self.vm_code.append('D=M')
        for i in range(int(line[2])+5): self.vm_code.append('D=D-1')
        self.vm_code.append('@2')
        self.vm_code.append('M=D')
        #LCL
        self._add_asm_comment('LCL')
        self.vm_code.append('@0')
        self.vm_code.append('D=M')
        self.vm_code.append('@1')
        self.vm_code.append('M=D')
        #jump to function
        self._add_asm_comment('jump to function')
        self.vm_code.append('@' + line[1])
        self.vm_code.append('0;JMP')

    def _return_code(self, line):
        # *** The excution squence in lecture is as following ***
        #   1.endFrame = LCL
        #   2.retAddr = *(endFrame - 5)
        #   3.*ARG = pop()
        #   4.SP = ARG + 1
        #   5.THAT = *(endFrame - 1)
        #   6.THIS = *(endFrame - 2)
        #   7.ARG = *(endFrame - 3)
        #   8.LCL = *(endFrame - 4)
        #   9.goto retAddr

        self._add_asm_comment(' '.join(line))
        
        #endFrame = LCL
        #Store endFrame in R14 temporarily(R13, R14, R15 are reserved for generate asm code)
        self._add_asm_comment('endFrame = LCL')
        self.vm_code.append('@1')
        self.vm_code.append('D=M')
        self.vm_code.append('@14')
        self.vm_code.append('M=D')
        #retAddr = *(endFrame - 5)
        #Store retAddr in R15 temporarily(R13, R14, R15 are reserved for generate asm code)
        self._add_asm_comment('retAddr = *(endFrame - 5)')
        self.vm_code.append('@R14')
        self.vm_code.append('D=M')
        for i in range(5): self.vm_code.append('D=D-1')
        self.vm_code.append('A=D')
        self.vm_code.append('D=M')
        self.vm_code.append('@R15')
        self.vm_code.append('M=D')
        #*ARG = pop()
        self._add_asm_comment('*ARG = pop()')
        self._mem_seg_code('pop argument 0'.split())
        #SP = ARG + 1
        self._add_asm_comment('SP = ARG + 1')
        self.vm_code.append('@2')
        self.vm_code.append('D=M+1')
        self.vm_code.append('@0')
        self.vm_code.append('M=D')
        #THAT = *(endFrame - 1)
        self._add_asm_comment('THAT = *(endFrame - 1)')
        self.vm_code.append('@R14')
        self.vm_code.append('M=M-1')
        self.vm_code.append('A=M')
        self.vm_code.append('D=M')
        self.vm_code.append('@4')
        self.vm_code.append('M=D')
        #THIS = *(endFrame - 2)
        self._add_asm_comment('THIS = *(endFrame - 2)')
        self.vm_code.append('@R14')
        self.vm_code.append('M=M-1')
        self.vm_code.append('A=M')
        self.vm_code.append('D=M')
        self.vm_code.append('@3')
        self.vm_code.append('M=D')
        #ARG = *(endFrame - 3)
        self._add_asm_comment('ARG = *(endFrame - 3)')
        self.vm_code.append('@R14')
        self.vm_code.append('M=M-1')
        self.vm_code.append('A=M')
        self.vm_code.append('D=M')
        self.vm_code.append('@2')
        self.vm_code.append('M=D')
        #LCL = *(endFrame - 4)
        self._add_asm_comment('LCL = *(endFrame - 4)')
        self.vm_code.append('@R14')
        self.vm_code.append('M=M-1')
        self.vm_code.append('A=M')
        self.vm_code.append('D=M')
        self.vm_code.append('@1')
        self.vm_code.append('M=D')
        #goto retAddr
        self._add_asm_comment('goto retAddr')
        self.vm_code.append('@R15')
        self.vm_code.append('0;JMP')

if __name__ == "__main__":
    path = os.path.join('..', 'FunctionCalls', 'FibonacciElement')
    #path = os.path.join('..', 'ProgramFlow', 'BasicLoop', 'BasicLoop.vm')
    parser_ = Parser()
    parser_.read(path)


    codeWriter = CodeWriter()
    codeWriter.gen_hack_code(parser_.lines, parser_.is_dir)
    codeWriter.write_to_file(path)