from sly import Lexer, Parser

class CalcLexer(Lexer):
    literals = {'{', '}'}
    tokens = {NAME, COMPLEX, PLUS, TIMES, ASSIGN, MINUS, DIVIDE}
    ignore = ' \t\n'

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    COMPLEX = r'\([0-9_];[0-9_]\)*'

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS),
        )

    def __init__(self):
        self.names = { }

    @_('NAME ASSIGN complex')
    def statement(self, p):
        self.names[p.NAME] = p.complex

    @_('complex')
    def statement(self, p):
        return(p.complex)

    @_('complex PLUS complex')
    def complex(self, p):
        return ("("+str(int(p.complex0[1])+int(p.complex1[1]))+";"+str(int(p.complex0[3])+int(p.complex1[3]))+")")


    @_('complex MINUS complex')
    def complex(self, p):
        return ("("+str(int(p.complex0[1])-int(p.complex1[1]))+";"+str(int(p.complex0[3])-int(p.complex1[3]))+")")


    @_('complex TIMES complex')
    def complex(self, p):
        return ("("+str(int(p.complex0[1])*int(p.complex1[1])-int(p.complex0[3])*int(p.complex1[3]))+";"+str(int(p.complex0[3])*int(p.complex1[1])+int(p.complex0[1])*int(p.complex1[3]))+")")

    @_('complex DIVIDE complex')
    def complex(self, p):
        return ("("+str((int(p.complex1[1])*int(p.complex0[1])+int(p.complex1[3])*int(p.complex0[3]))/(int(p.complex0[1])*int(p.complex0[1])+int(p.complex0[3])*int(p.complex0[3])))
        +";"+str((int(p.complex1[3])*int(p.complex0[1])-int(p.complex1[1])*int(p.complex0[3]))/(int(p.complex0[1])*int(p.complex0[1])+int(p.complex0[3])*int(p.complex0[3])))+")")

    @_('MINUS complex %prec UMINUS')
    def complex(self, p):
        return -p.complex

    @_('COMPLEX')
    def complex(self, p):
        return str(p.COMPLEX)

    @_('NAME')
    def complex(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print(f'Undefined name {p.NAME!r}')
            return 0



if __name__ == "__main__":
    lexer = CalcLexer()
    parser = CalcParser()
   
    text = ""
    with open('mini4.txt') as f:
        for line in  f.readlines():
            text += line
    result = parser.parse(lexer.tokenize(text))
    with open("minta2.html","w") as file:
        file.write("<html><body>" + str(result) + "</body></html>")