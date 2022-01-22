class BaseHtmlException(Exception):
    def __init__(self, web_driver, line):
        self.web_driver = web_driver
        self.line = line
