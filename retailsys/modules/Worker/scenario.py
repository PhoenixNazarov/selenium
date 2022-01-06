


class Scenario:
    def __init__(self):
        if open_link(): return

        TYPE_USER = 'undefined'
        for i in range(line.COUNT_LINES):
            PLAN_NAME, NAME_CARD, PLAN_TYPE, ND_OPTION, NUMBER = line.PLANS[i].values()

            if choose_plans(): return
            if enter_card(): return

            TYPE_USER = check_on_reg()
            if TYPE_USER: return

            if marking_options(): return
            if enter_number(): return
            if mark_last_params(): return
            if end_action(): return

        if enter_email(): return
        if enter_mailing_data(): return
        if enter_address(): return
        if enter_more_data(): return
        if enter_more_data2(): return
        if enter_card(): return