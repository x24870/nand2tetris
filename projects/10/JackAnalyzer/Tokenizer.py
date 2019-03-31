import xml.etree.ElementTree as ET

_keyword = [
    'class',
    'constructor',
    'function',
    'method',
    'field',
    'static',
    'var',
    'int',
    'char',
    'boolean',
    'void',
    'true',
    'false',
    'null',
    'this',
    'let',
    'do',
    'if',
    'else',
    'while',
    'return',
]

_symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

_tokenType = [
    'KEYWORD',
    'SYMBOL',
    'IDENTITIER',
    'INT_CONST',
    'STRING_CONST',
]

class Tokenizer():
    def __init__(self, code_stream):
        self.code_stream = code_stream
        self.cur_token = ''
        self.stream_idx = 0
        self.str_flag = False
        self.root = ET.Element('tokens')
        self.ETree = ET.ElementTree(self.root)

    def process_code(self):
        while self.hasMoreTokens():
            self.advance()
        return self.ETree

    def hasMoreTokens(self):
        self.cur_token = ''
        while self.stream_idx < len(self.code_stream):
            cur_char = self.code_stream[self.stream_idx]
            #Current string is in the double quote
            if self.str_flag:
                if cur_char != '"':
                    self.cur_token += cur_char
                    self.stream_idx += 1
                    continue
                else:
                    self.stream_idx -= 1
                    break

            #Current string is keyword or variable
            if cur_char not in _symbol and cur_char != ' ':
                self.cur_token += cur_char
                self.stream_idx += 1
                continue
            #Current string is symbol or space
            else:
                if cur_char == '"':
                    #if this double quote is start of string, str_flat = True
                    #else str_flat = False
                    self.str_flag = not self.str_flag
                    
                if cur_char != ' ':
                    #if current char is symbol and previous char is not space
                    #deal with current token first
                    if self.cur_token:
                        break
                    else:
                        self.cur_token = cur_char

                self.stream_idx += 1
                break
        else:
            return False
        return True
                
    def advance(self):
        if not self.cur_token:
            return
        #add current token as a new element at root of xml tree
        tokenType = self.tokenType(self.cur_token)
        newElement = ET.Element(tokenType)
        newElement.text = self.cur_token
        self.root.append(newElement)

    def tokenType(self, token):
        if self.str_flag:
            return 'stringConstant'
        elif token in _keyword:
            return 'keyword'
        elif token in _symbol:
            return 'symbol'
        elif token.isdecimal():
            return 'integerConstant'
        else:
            return 'identifier'
