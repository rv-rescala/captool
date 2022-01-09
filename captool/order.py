from lark import Lark, Transformer
from catswalk.scraping.webdriver import CWWebDriver
from catswalk.scraping.types.type_webdriver import *

def execute(request: CWWebDriver, grammar_path: str, order_path: str, url:str, output_path:str, filename:str) -> str:
    class Main(Transformer):
        def __init__(self):
            self._functions = {}
        
        def open_call(self, token):
            if request:
                request.get(url=url)
            print(f"open: {url}")

        def move_class_call(self, token):
            # request.move_to_element_by_class_name(class_name="Components__EpisodeListContainer-sc-4hyt7h-7 ejFlQx")
            print(token)

        def capture_by_screen(self, token):
            # request.print_screen_by_window("/Users/rv/Desktop", "hoge.png")
            print(token)
        
        def symbol(self, token):
            return token[0].value

        def string(self, token):
            return token[0][1:-1]

    rule = open(grammar_path).read()
    parser = Lark(rule, parser='lalr', transformer=Main())
    program = open(order_path).read()
    parser.parse(program)