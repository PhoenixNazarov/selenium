from modules.Worker.selenium.webdriver.common.by import By
# from .FalseNumbers import ManyNumberException
from modules.data.Sheets import ErrorsSheetCollect

errors = [
    # ManyNumberException
]

errors_base = ErrorsSheetCollect()


def check_page_on_error(web_driver, line, solve):
    # for error in errors:
    #     _error = error(web_driver, line)
    #     res = _error.check()
    #     if res:
    #         if solve:
    #             return _error.solve()
    #         else:
    #             raise _error

    element = web_driver.have_element(By.CLASS_NAME, "invalid-feedback")
    if element:
        errors_base.write_error(web_driver.find_element(By.CLASS_NAME, "invalid-feedback").text, line.PASSPORT)


# def try_fix_error(web_driver, line, func_name):
#     fixer = False
    # if func_name == 'check_on_reg':
    #     fixer = ManyNumberException(web_driver, line)

    # if fixer:
    #     return fixer.solve()
