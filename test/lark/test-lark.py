from lark import Lark, Transformer
# https://developers.10antz.co.jp/archives/2007

class Main(Transformer):
    def __init__(self):
        self._functions = {}
    
    def open_call(self, token):
        print(token)

    def click_call(self, token):
        print(token)

    def move_call(self, token):
        print(token)
    
    def symbol(self, token):
        return token[0].value

    def string(self, token):
        return token[0][1:-1]

rule = open('grammar.lark').read()
parser = Lark(rule, parser='lalr', transformer=Main())
program = open('program.txt').read()
parser.parse(program)