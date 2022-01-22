from modules.Lines import load_lines_group
from modules.UI import UI
from modules.Worker import Operator
from modules.Worker.Errors.Classification import check_page_on_error
from modules.Worker.MyWebDriver import WebDriver
from modules.functions import start_thread

from .TestTypesAction import *

canvas = UI.make_root()
line_groups = load_lines_group()
stack = Stack()
stack.load_lines(line_groups[0])
worker = Operator(Error(), Save(), Status(), stack, 0)

line = line_groups[0].get_lines()[0]


def check():
    while 1:
        check_page_on_error(worker.web_driver, line, False)

worker.web_driver = WebDriver()
start_thread(check)


# time.sleep(30)\
while 1:
    time.sleep(20)
