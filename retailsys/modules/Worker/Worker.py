from selenium.webdriver.common.by import By
from modules.exception.Handlers import *
from modules.data import ErrorsSheetBase, ErrorsSheetCollect, MainSheet
from modules.Worker.MyWebDriver import WebDriver
from modules.Worker.Authorization import authorization
from modules.Objects import Memory
from modules.data.Log import Log

# not important
from modules.Lines.Line import Line


def check_page_on_error(web_driver, current_line, solve=None):
    element = web_driver.have_element(By.CLASS_NAME, "invalid-feedback")
    if element:
        ErrorsSheetCollect.write_error(web_driver.find_element(By.CLASS_NAME, "invalid-feedback").text, current_line.PASSPORT)


class Worker(Log):
    def __init__(self, Error, Save, Status, Stack, numb):
        super().__init__(numb)
        self.web_driver = None
        self.Error = Error
        self.Save = Save
        self.Status = Status
        self.Stack = Stack
        self.numb = numb

        self.current_line = None

    @worker_exceptions
    def polling(self):
        self.web_driver = WebDriver()
        authorization(self.web_driver, self.Status, self.numb)

        self.Status.set_status("polling")
        while 1:
            self.current_line = None
            line = self.Stack.wait_line()
            self.current_line = line
            self.plan(line)
            self.Stack.end_line(line)

    def UI_control(self, function):
        error_api = self.Error
        status_api = self.Status

        def wrapper(func):
            status_api.set_status(func.__name__)
            while 1:
                try:
                    ret = function(func)
                    if ret and type(ret) == bool:
                        return False
                    return ret
                except Exception as e:
                    print('error', e)
                    check_page_on_error(self.web_driver, self.current_line, solve=False)
                    # try_fix_error(self.web_driver, self.current_line, func.__name__)

                    # self.write_log('line_error', self.numb)
                    error_api.change_position('error', 1)
                    command = error_api.wait_change_position()
                    if command == 'next':
                        break
                    elif command == 'cancel':
                        raise BreakScenario()
                    elif command == 'repeat':
                        continue
            # next
            return False

        return wrapper

    def find_error(self, function):
        def wrapper(func):
            check_page_on_error(self.web_driver, self.current_line, solve=False)

            res = function(func)

            check_page_on_error(self.web_driver, self.current_line, solve=False)
            return res

        return wrapper

    @staticmethod
    def smart_memory(function):
        mem = Memory()

        def wrapper(func):
            # when need break
            name = func.__name__
            if not mem.check_allow(name):
                return

            res = function(func)
            mem.need_write(func.__name__, res)

            return res

        return wrapper

    @plans_exception
    def plan(self, line: Line):
        @self.UI_control
        @self.find_error
        # @self.smart_memory
        def pull(function):
            function()

        wd = self.web_driver
        COPY = True

        def open_link():
            wd.get('https://retailsys.hotnet.net.il/HotMobile/HMPurchase')

        # CHOOSE PLANS
        def choose_plans():
            if not COPY: return
            plans_type = wd.find_elements(By.CLASS_NAME, 'plan-type', time_sleep =  0.5)
            plans_type[PLAN_TYPE].find_element(By.XPATH, '..').click()

        # CARD
        def button_card():
            if not COPY: return
            all_cards = wd.find_elements(By.CLASS_NAME, 'card-title', time_sleep =  0.5)
            for ci in all_cards:
                if ci.text == NAME_CARD:
                    but = ci.find_element(By.XPATH, '..').find_element(By.XPATH, '..')
                    but.find_element(By.CLASS_NAME, 'btn').click()

        # CHECK ON REG
        def check_on_reg():
            if not COPY: return
            global TYPE_USER

            def writer_number():
                for number in set([line.NUMBER_USER] + [i['number'] for i in line.PLANS]):
                    wd.find_element(By.NAME, 'clientPhoneNumber').clear()
                    wd.find_element(By.NAME, 'clientLastFourDigits').clear()
                    wd.find_element(By.NAME, 'clientPhoneNumber').send_keys(number)
                    wd.find_element(By.NAME, 'clientLastFourDigits').send_keys(line.CARD[-4:])
                    dialogs = wd.find_element(By.TAG_NAME, 'client-eligibility')
                    dialogs.find_elements(By.TAG_NAME, 'button')[0].click()
                    wd.nothing(time_sleep = 0.4, important = True)
                    if not wd.have_element(By.TAG_NAME, "client-eligibility"):
                        return
                raise Exception

            # LEFT_BUTTON
            dialog = wd.find_element(By.TAG_NAME, 'client-eligibility', time_sleep = 2)
            dialog.find_elements(By.TAG_NAME, 'h2')[1].click()

            # CHECK ALREADY REG
            dialog = wd.find_element(By.TAG_NAME, 'client-eligibility')
            dialog.find_element(By.TAG_NAME, 'input').send_keys(line.PASSPORT)
            dialog.find_element(By.TAG_NAME, 'button').click()
            wd.nothing(time_sleep = 0.5, important = True)

            TYPE_USER = 'undefined'
            # already
            if wd.have_element(By.NAME, 'clientPhoneNumber'):
                if wd.have_element(By.NAME, "clientPhoneNumber") and wd.have_element(By.NAME, "clientLastFourDigits"):
                    writer_number()
                    TYPE_USER = 'already'

            # button
            if wd.have_element(By.TAG_NAME, 'client-eligibility'):
                if 'ללקוח זה נמצאה הזמנה פעילה, האם ברצונך להמשיך?' in wd.find_element(By.TAG_NAME,
                                                                                   'client-eligibility').text:
                    dialogs = wd.find_element(By.TAG_NAME, 'client-eligibility')
                    dialogs.find_elements(By.TAG_NAME, 'button')[0].click()
                    writer_number()
                    TYPE_USER = 'already'

            # new
            if wd.have_element(By.NAME, 'clientId'):
                if len(wd.find_elements(By.NAME, 'clientId')) != 1:
                    TYPE_USER = 'new'

            return TYPE_USER

        # ===========OPTIONS PAGE

        # 1first_table,2second options
        def marking_options():
            if not COPY: return
            options = wd.find_elements(By.CLASS_NAME, 'desing-radios', time_sleep =  2)
            for u in options:
                if u.find_element(By.XPATH, '..').text in ND_OPTION:
                    u.click()
                    wd.noting(0.01, important = True)

        # 3third_table number
        def enter_number():
            table = wd.find_element(By.TAG_NAME, 'portability-comp', time_sleep =  0.5)
            labels = table.find_elements(By.TAG_NAME, 'label')
            if TYPE_USER == 'new' and NUMBER != 'חדש':
                try:
                    labels[1].click()
                    table.find_element(By.NAME, 'phone').send_keys(NUMBER)
                    table.find_element(By.TAG_NAME, 'button').click()
                    table = wd.find_element(By.TAG_NAME, 'portability-comp', time_sleep =  2)
                    table.find_elements(By.NAME, 'verifyNeeded')[1].find_element(By.XPATH, '..').click()
                except:
                    pass
                # enter users data
                table.find_element(By.NAME, 'firstName', time_sleep =  2).send_keys(NUMBER)
                table.find_element(By.NAME, 'lastName').send_keys(line.SURNAME)
                table.find_element(By.NAME, 'userId').send_keys(line.PASSPORT)
                table.find_element(By.NAME, 'lastCompany').find_elements(By.TAG_NAME, 'option')[0].click()
                table.find_element(By.NAME, 'agreement').click()
            else:
                labels[0].click()

        # 5fifth_table tab enter
        def mark_last_params():
            table = wd.find_element(By.TAG_NAME, 'regulations-comp', time_sleep =  0.5)
            rows = table.find_elements(By.CLASS_NAME, "form-group")[1:]
            for ci in range(len(rows)):
                if ci == 0:
                    _id = 0
                elif ci == 8:
                    _id = 0
                else:
                    _id = 1

                rows[ci].find_elements(By.TAG_NAME, 'label')[_id].click()
                wd.noting(time_sleep =  0.01, important = True)

        # ACTION
        def end_action():
            global COPY
            table = wd.find_element(By.TAG_NAME, 'purchase-summary', time_sleep =  0.5)

            if i + 1 == line.COUNT_LINES:
                table.find_element(By.CLASS_NAME, 'continue').click()
            else:
                buttons = table.find_elements(By.TAG_NAME, 'button')
                if PLAN_TYPE == line.PLANS[i + 1]['plan_type']:
                    need_button = 'שכפל מנוי'
                    COPY = True
                else:
                    need_button = 'הוסף מנוי נוסף'
                    COPY = False
                for b in buttons:
                    if b.text == need_button:
                        b.click()
                        wd.noting(time_sleep =  0.3, important = True)

                # CHECK ON COPY MOVE
                if PLAN_TYPE == line.PLANS[i + 1]['plan_type']:
                    option = 'דמי חיבור SIM ללא עלות'
                    options = wd.find_elements(By.CLASS_NAME, 'desing-radios')
                    for u in options:
                        if option in u.find_element(By.XPATH, '..').text:
                            u.click()
                            wd.noting(time_sleep =  0.01, important = True)
                    return "COPY"
                return "UNCOPY"

        # AFTER PACKETS
        def enter_email():
            table = wd.find_element(By.TAG_NAME, 'interactive-forms', time_sleep =  2)
            lbs = table.find_elements(By.TAG_NAME, 'label')
            for uu in lbs:
                if 'ללא שליחת טפסים מקדימים' in uu.text:
                    uu.click()
                    break
            wd.find_element(By.CLASS_NAME, 'continue').click()

        # MAILING DATA
        def enter_mailing_data():
            table = wd.find_element(By.TAG_NAME, 'app-personaldetails', time_sleep =  2)
            if table.find_element(By.NAME, 'Phone').get_attribute('value') == '':
                table.find_element(By.NAME, 'Phone').send_keys(line.NUMBER_USER)

            divs = table.find_elements(By.TAG_NAME, 'div')
            for uu in divs:
                if 'דואר ישראל' == uu.text:
                    print('ok')
                    uu.find_elements(By.TAG_NAME, 'label')[0].click()
                    break

            # todo
            if TYPE_USER == 'already': return

            table.find_element(By.NAME, 'FirstName').send_keys(line.NAME)
            table.find_element(By.NAME, 'LastName').send_keys(line.SURNAME)

        # CITY, ADDRESS
        def enter_address():
            table = wd.find_element(By.TAG_NAME, 'app-personaldetails', time_sleep =  0.5)
            for ii in range(2):
                if ii == 0:
                    tag = 'City'
                    parametr = line.CITY
                else:
                    tag = 'Street'
                    parametr = line.STREET

                # # todo
                # if table.find_elements(By.NAME, tag)[1].get_attribute('value') != '': continue

                inputs = table.find_elements(By.NAME, tag)
                options_home, input = inputs[0], inputs[1]

                for i in range(len(parametr)):
                    input.send_keys(parametr[i])
                    wd.noting(time_sleep =  0.5, important = True)

                    options = options_home.find_elements(By.TAG_NAME, 'li')
                    if len(options) > 0:
                        count_options = len(options)

                        if count_options == 1:
                            options[0].click()
                            break

                        elif i + 1 == len(parametr):
                            options[0].click()
                            break
                    wd.noting(time_sleep =  1, true = False)

        # PERS DATA
        def enter_more_data():
            table = wd.find_element(By.TAG_NAME, 'app-personaldetails', time_sleep =  0.5)
            if table.find_element(By.NAME, 'HouseNumber').get_attribute('value') == '':
                table.find_element(By.NAME, 'HouseNumber').send_keys(line.HOUSE_NUMBER)

            if table.find_element(By.NAME, 'ApartmentNumber').get_attribute('value') == '':
                table.find_element(By.NAME, 'ApartmentNumber').send_keys(line.APART_NUMBER)

            if table.find_element(By.NAME, 'POBox').get_attribute('value') == '':
                table.find_element(By.NAME, 'POBox').send_keys(line.POBox)
            wd.find_element(By.CLASS_NAME, 'continue').click()

        # DROP CITY,ADDR
        def enter_more_data2():
            table = wd.find_element(By.TAG_NAME, 'retail-deliverytype', time_sleep =  2)
            for ii in range(2):
                if ii == 0:
                    tag = 'City'
                    parameter = line.CITY
                else:
                    tag = 'Street'
                    parameter = line.STREET

                if table.find_elements(By.NAME, tag)[1].get_attribute('value') != '': continue

                inputs = table.find_elements(By.NAME, tag)
                options_home, input = inputs[0], inputs[1]

                # # todo
                # if input.get_attribute('value') != '': continue

                for i in range(len(parameter)):
                    input.send_keys(parameter[i])
                    wd.noting(time_sleep =  1.5, important = True)

                    # try:
                    options = options_home.find_elements(By.TAG_NAME, 'li')
                    if len(options) > 0:
                        count_options = len(options)

                        if count_options == 1:
                            options[0].click()
                            break

                        elif i + 1 == len(parameter):
                            options[0].click()
                            break
                    # except:pass
                wd.noting(time_sleep =  1.5, important = False)
            element = table.find_element(By.NAME, 'houseNumber')
            if element.get_attribute('value') == '': element.send_keys(line.HOUSE_NUMBER)
            element = table.find_element(By.NAME, 'apartmentNumber')
            if element.get_attribute('value') == '': element.send_keys(line.APART_NUMBER)
            wd.find_element(By.CLASS_NAME, 'continue', time_sleep =  2).click()

        # CARD
        def enter_card():
            table = wd.find_element(By.TAG_NAME, 'payemnt-comp', time_sleep =  1)
            if TYPE_USER == 'already':
                table = wd.find_element(By.TAG_NAME, 'payemnt-comp')
                table.find_element(By.TAG_NAME, 'label').click()

            if line.TYPE_PAY == 'card':
                table.find_element(By.NAME, 'creditCardNumber').send_keys(line.CARD)
                table.find_element(By.NAME, 'creditCardHolderId').send_keys(line.PASSPORT)

            else:
                table.find_element(By.NAME, 'bankOrderClientId').send_keys(line.CARD)
                table.find_element(By.NAME, 'bankOrderFirstName').send_keys(line.CARD)
                table.find_element(By.NAME, 'bankOrderLastName').send_keys(line.CARD)

            options = wd.find_elements(By.CLASS_NAME, 'desing-radios')
            for u in options:
                u.click()

        # SAVE
        def save():
            wd.find_element(By.CLASS_NAME, 'continue', time_sleep =  1).click()
            boxes = wd.find_elements(By.CLASS_NAME, 'box', time_sleep =  1)

            if len(boxes) == 1:
                box = boxes[0]
                last_er = box.find_element(By.TAG_NAME, 'h3').text

                MainSheet.set_value('AM', line.index, last_er)
                # labels[lab_index].config(text = last_er)

            else:
                kod1 = wd.find_element(By.XPATH,
                                                    '/html/body/app-root/master-page/div/div[2]/div[1]/app-purchase/form/div/thank-you/div/div/div[2]/div[3]/div[1]').text
                kod2 = wd.find_element(By.XPATH,
                                                    '/html/body/app-root/master-page/div/div[2]/div[1]/app-purchase/form/div/thank-you/div/div/div[2]/div[1]/div/div[3]').text

                MainSheet.set_value('AM', line.index, kod1 + ' ' + kod2)
                # labels[indexxx].config(text = kod1 + ' ' + kod2)

        # ========== SCENARIO ==========
        pull(open_link)

        WriteLines = [
            choose_plans,
            button_card,
            check_on_reg,
            marking_options,
            enter_number,
            mark_last_params,
            end_action
        ]

        PersonalData = [
            enter_email,
            enter_mailing_data,
            enter_address,
            enter_more_data,
            enter_more_data2,
            enter_card
        ]

        # lines
        for i in range(line.COUNT_LINES):
            PLAN_NAME, NAME_CARD, PLAN_TYPE, ND_OPTION, NUMBER = line.PLANS[i].values()
            [pull(func) for func in WriteLines]

        # after lines
        [pull(func) for func in PersonalData]

        self.Status.set_status("end")
        self.Save.change_position(1, "finish")

        command = self.Save.wait_command()
        if command:
            save()
