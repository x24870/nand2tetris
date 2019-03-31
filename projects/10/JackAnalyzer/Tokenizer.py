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
            if cur_char == '"':
                self.cur_token, str_len = self._process_str_const(self.stream_idx)
                self.stream_idx += str_len + 2
                break

            #Current string is keyword or variable
            if cur_char not in _symbol and cur_char != ' ':
                self.cur_token += cur_char
                #check if this string is end
                next_char = self.code_stream[self.stream_idx + 1]
                if next_char in _symbol or next_char == ' ' or next_char == '"':
                    self.stream_idx += 1
                    break
                else:
                    self.stream_idx += 1
                    continue
            #Current string is symbol or space
            else:
                if cur_char != ' ':
                    self.cur_token = cur_char
                self.stream_idx += 1
                break
        else:
            return False
        return True
                
    def _process_str_const(self, idx):
        cur_idx = idx + 1 #skip first double quote
        str_const = ''
        self.str_flag = True
        while self.code_stream[cur_idx] != '"':
            str_const += self.code_stream[cur_idx]
            cur_idx += 1
        str_len = cur_idx - idx - 1
        return str_const, str_len

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
            self.str_flag = False
            return 'stringConstant'
        elif token in _keyword:
            return 'keyword'
        elif token in _symbol:
            return 'symbol'
        elif token.isdecimal():
            return 'integerConstant'
        else:
            return 'identifier'
