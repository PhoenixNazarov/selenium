class WebDriverArchive:
    def __init__(self, Error, Save, Status, Stack, number_name):
        self.numb = 0
        self.Error = Error
        self.Save = Save
        self.Status = Status
        self.Stack = Stack
        self.number_name = number_name


class WebDriverLogics:
    def __init__(self, UI_control, ):
        self.UI_control = UI_control


class Memory:
    def __init__(self):
        self.copy_miss_functions = ["choose_plans", "button_card", "marking_options", "mark_last_params"]
        self.COPY = 'COPY'# UNCOPY

        self.only_first = 'check_on_reg'
        self.TYPE_USER = 'first'

        self.disallow_rules = [
            lambda name: name in self.copy_miss_functions and self.COPY == "COPY",
            lambda name: name == self.only_first and self.TYPE_USER != "first",
        ]

    def check_allow(self, name):
        if any([i(name) for i in self.disallow_rules]):
            print('disallow', [i(name) for i in self.disallow_rules])
            return 0
        return 1

    def need_write(self, name, res):
        if name == 'check_on_reg':
            self.TYPE_USER = res
        elif name == 'end_action':
            self.COPY = res
