from WebFunctions import *
from Handler import *


class Scenario:
    def __init__(self, line, handlers):
        open_link()

        TYPE_USER = 'undefined'
        for i in range(line.COUNT_LINES):
            PLAN_NAME, NAME_CARD, PLAN_TYPE, ND_OPTION, NUMBER = line.PLANS[i].values()

            choose_plans()
            enter_card()

            TYPE_USER = check_on_reg()
            if TYPE_USER: return

            marking_options()
            enter_number()
            mark_last_params()
            end_action()

        enter_email()
        enter_mailing_data()
        enter_address()
        enter_more_data()
        enter_more_data2()
        enter_card()

    @handlers.UI_control
    def pull(self, function):
