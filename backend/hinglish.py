#-------------------------------------------#
#defined constants 
#-------------------------------------------#

digits = '0123456789'


#-------------------------------------------#
#errors
#-------------------------------------------#

class Error:
    def __init__(self, pos_start,pos_end,error_name,details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def to_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln+1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


#-------------------------------------------#
#position of char
#-------------------------------------------#

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#-------------------------------------------#
#tokens 
#-------------------------------------------#
TOKEN_DICT = {
    '+' : 'PLUS',
    '-' : 'MINUS',
    '*' : 'MUL',
    '/' : 'DIV',
    '(' : 'LBRACKET',
    ')' : 'RBRACKET'
}
INT = 'INT'
FLOAT ='FLOAT'

class Token:
    def __init__(self, type_,value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        else:
            return f'{self.type}'

#----------------------------------------------#
# lexical analyser
#----------------------------------------------#

class Lexer:
    def __init__(self , fn , text):
        self.fn = fn 
        self.text = text
        self.pos = Position(-1,0,-1 ,fn , text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
        else:
            self.current_char = None

    def tokenize(self):
        tokens = list()

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in digits:
                tokens.append(self.tokenize_num())
            elif self.current_char in TOKEN_DICT:
                tokens.append(Token(TOKEN_DICT[self.current_char]))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [] , IllegalCharError(pos_start, self.pos, "'" + char + "'")
        
        return tokens, None

    def tokenize_num(self):
        num_str = ''
        dots = 0

        while self.current_char !=None and self.current_char in digits + '.':
            if self.current_char == '.':
                if dots == 1:
                    break
                else:
                    dots += 1
                    num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        
        if dots == 0:
            return Token(INT , int(num_str))
        else:
            return Token(FLOAT , float(num_str))

#-------------------------------------------#
#execute
#-------------------------------------------#

def execute(fn ,text):
    lex = Lexer(fn , text)
    tokens , error = lex.tokenize()

    return tokens,error