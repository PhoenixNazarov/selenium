from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium
import threading

from config import *
from modules.Exceptions import SmsLoadError
from modules.Line import Line
from modules.Data import SettingsJson, Log


def get_mes(password):
    import imaplib
    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    mail.login(password['gmail'], password['password'])
    mail.list()
    mail.select("inbox")

    result, data = mail.search(None, "ALL")
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]
    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]

    import email
    email_message = email.message_from_string(raw_email.decode('utf-8'))

    code = ''
    for part in email_message.walk():
        # each part is a either non-multipart, or another multipart message
        # that contains further parts... Message is organized like a tree
        if part.get_content_type() == 'text/plain':
            code = (part.get_payload(None, True))  # prints the raw text

    # code = get_first_text_block(email_message)
    code = (code.decode(errors = 'ignore')).split()
    d_code = 0
    for i in code:
        if i.isdigit():
            if len(i) == 5:
                d_code = int(i)

    return d_code


class Worker(Log):
    def __init__(self, Error, Save, Status, Stack, numb, MainSheet):
        super().__init__(numb)
        self.web_driver = None
        self.Error = Error
        self.Save = Save
        self.Status = Status
        self.Stack = Stack
        self.numb = numb
        self.Settings = SettingsJson(numb)
        self.MainSheet = MainSheet

        self.type_sleep = TYPE_SLEEP

    def start(self):
        self.Status.set_status('start')

        password = self.Settings.get_data()

        try:
            SMS_LAST = get_mes(password)
        except Exception as e:
            raise SmsLoadError(password['mail'], self.numb)

        options = webdriver.ChromeOptions()
        self.web_driver = webdriver.Chrome(chrome_options = options, executable_path = "webDriver/chromedriver.exe")

        name = str(self.numb)
        self.web_driver.execute_script("window.open('http://" + name + ".com', '_blank');")
        self.time_sleep(1)
        self.web_driver.switch_to.window(self.web_driver.window_handles[0])
        self.web_driver.get('https://retailsys.hotnet.net.il/Login')
        self.time_sleep(2)

        if password['auto_login'] == 0:
            return

        # LOGGING
        SMS_LAST = get_mes(password)
        self.web_driver.find_elements(By.TAG_NAME, 'input')[0].send_keys(password['user_name'])
        self.web_driver.find_elements(By.TAG_NAME, 'input')[1].click()
        self.time_sleep(2)

        #
        self.Status.set_status('enter_sms')
        while 1:
            SMS = get_mes(password)
            if SMS != SMS_LAST: break
            self.time_sleep(1)
        self.web_driver.find_elements(By.TAG_NAME, 'input')[0].send_keys(SMS)
        self.web_driver.find_elements(By.TAG_NAME, 'input')[1].click()

    def polling(self):
        def thread():
            self.start()

            while 1:
                line = self.Stack.wait_line()
                self.plan(line)
                self.Stack.end_line(line)

        threading.Thread(target = thread).start()

    def error_checker(self, function):
        error_api = self.Error
        status_api = self.Status

        def wrapper(*args, **kwargs):
            status_api.set_status(function.__name__)
            while 1:
                try:
                    ret = function(*args, **kwargs)
                    if ret and type(ret) == bool:
                        return False
                    return ret
                except Exception as e:
                    self.write_log('line_error', e, self.numb)
                    error_api.change_position(e, 1)
                    command = error_api.wait_change_position()
                    if command == 'next':
                        break
                    elif command == 'cans':
                        # exit
                        return True
                    elif command == 'repeat':
                        continue
            # next
            return False

        return wrapper

    def time_sleep(self, count, element_finder=None, can_skip=False):
        time_start = time.time()
        if element_finder is None:
            if not can_skip:
                time.sleep(count * TIME_DELAY_PERC)

        if self.type_sleep == 'last':
            time.sleep(count * TIME_DELAY_PERC)
        elif self.type_sleep == 'fast':
            start = time.time()
            while 1:
                if time.time() - start > MAX_TIME_WAIT:
                    self.write_log('line_delay_max_time', json.dumps({
                        "time_delta": round(time.time() - time_start, 5),
                        "line_status": self.Status.get_status(),
                        "TYPE_SLEEP": self.type_sleep,
                        "can_skip": can_skip,
                        "count": count,
                        "element_finder": 0 if element_finder is None else 1
                    }), self.numb)
                    raise Exception
                try:
                    return element_finder()
                except selenium:
                    pass

        self.write_log('line_delay', json.dumps({
            "time_delta": round(time.time() - time_start, 5),
            "line_status": self.Status.get_status(),
            "TYPE_SLEEP": self.type_sleep,
            "can_skip": can_skip,
            "count": count,
            "element_finder": 0 if element_finder is None else 1
        }), self.numb)

    def plan(self, line: Line):
        wd = self.web_driver
        ts = self.time_sleep

        @self.error_checker
        def open_link():
            wd.get('https://retailsys.hotnet.net.il/HotMobile/HMPurchase')
            ts(2, can_skip = True)

        # CHOOSE PLANS
        @self.error_checker
        def choose_plans():
            plans_type = ts(0.5, lambda: wd.find_elements(By.CLASS_NAME, 'plan-type'))
            plans_type[PLAN_TYPE].find_element(By.XPATH, '..').click()

        # CARD
        @self.error_checker
        def button_card():
            all_cards = ts(0.5, lambda: wd.find_elements(By.CLASS_NAME, 'card-title'))
            for ci in all_cards:
                if ci.text == NAME_CARD:
                    but = ci.find_element(By.XPATH, '..').find_element(By.XPATH, '..')
                    but.find_element(By.CLASS_NAME, 'btn').click()

        # CHECK ON REG
        @self.error_checker
        def check_on_reg():
            if i == 0:
                # LEFT_BUTTON
                dialog = ts(2, lambda: wd.find_element(By.TAG_NAME, 'client-eligibility'))
                dialog.find_elements(By.TAG_NAME, 'h2')[1].click()

                # CHECK ALREADY REG
                dialog = wd.find_element(By.TAG_NAME, 'client-eligibility')
                dialog.find_element(By.TAG_NAME, 'input').send_keys(line.PASSPORT)
                dialog.find_elements(By.TAG_NAME, 'button')[0].click()
                ts(2, can_skip = False)

                type_user = 'undefined'
                # error
                try:
                    if wd.find_element(By.CLASS_NAME, 'invalid-feedback').text != '':
                        type_user = 'error'
                except:
                    pass

                # already
                try:
                    if len(wd.find_elements(By.NAME, 'clientPhoneNumber')) == 1:
                        # clientPhoneNumber
                        type_user = 'already'
                except:
                    pass

                # button
                try:
                    if 'ללקוח זה נמצאה הזמנה פעילה, האם ברצונך להמשיך?' in wd.find_element(By.TAG_NAME, 
                            'client-eligibility').text:
                        type_user = 'button'
                except:
                    pass

                # new
                try:
                    if len(wd.find_elements(By.NAME, 'clientId')) != 1:
                        type_user = 'new'
                except:
                    pass

                if type_user == 'error': raise
                if type_user == 'already':
                    wd.find_element(By.NAME, 'clientPhoneNumber').send_keys(line.NUMBER_USER)
                    wd.find_element(By.NAME, 'clientLastFourDigits').send_keys(line.CARD[-4:])
                    dialogs = wd.find_element(By.TAG_NAME, 'client-eligibility')
                    dialogs.find_elements(By.TAG_NAME, 'button')[0].click()
                if type_user == 'button':
                    dialogs = wd.find_element(By.TAG_NAME, 'client-eligibility')
                    dialogs.find_elements(By.TAG_NAME, 'button')[0].click()
                    wd.find_element(By.NAME, 'clientPhoneNumber').send_keys(line.NUMBER_USER)
                    wd.find_element(By.NAME, 'clientLastFourDigits').send_keys(line.CARD[-4:])
                    dialogs = wd.find_element(By.TAG_NAME, 'client-eligibility')
                    dialogs.find_elements(By.TAG_NAME, 'button')[0].click()
                    type_user = 'already'
                return type_user

        # ===========OPTIONS PAGE

        # 1first_table,2second options
        @self.error_checker
        def marking_options():
            options = ts(2, lambda: wd.find_elements(By.CLASS_NAME, 'desing-radios'))
            for u in options:
                if u.find_element(By.XPATH, '..').text in ND_OPTION:
                    u.click()
                    ts(0.01, can_skip = True)

        # 3third_table number
        @self.error_checker
        def enter_number():
            table = ts(0.5, lambda: wd.find_element(By.TAG_NAME, 'portability-comp'))
            labels = table.find_elements(By.TAG_NAME, 'label')
            if TYPE_USER == 'new' and NUMBER != 'חדש':
                try:
                    labels[1].click()
                    table.find_element(By.NAME, 'phone').send_keys(NUMBER)
                    table.find_element(By.TAG_NAME, 'button').click()
                    table = wd.find_element(By.TAG_NAME, 'portability-comp')
                    table = ts(2, lambda: wd.find_element(By.TAG_NAME, 'portability-comp'))
                    table.find_elements(By.NAME, 'verifyNeeded')[1].find_element(By.XPATH, '..').click()
                    ts(2, can_skip = True)
                except:
                    pass
                # enter users data
                table.find_element(By.NAME, 'firstName').send_keys(NUMBER)
                table.find_element(By.NAME, 'lastName').send_keys(line.SURNAME)
                table.find_element(By.NAME, 'userId').send_keys(line.PASSPORT)
                table.find_element(By.NAME, 'lastCompany').find_elements(By.TAG_NAME, 'option')[0].click()
                table.find_element(By.NAME, 'agreement').click()
            else:
                labels[0].click()

        # 5fifth_table tab enter
        @self.error_checker
        def mark_last_params():
            table = ts(0.5, lambda: wd.find_element(By.TAG_NAME, 'regulations-comp'))
            rows = table.find_elements(By.CLASS_NAME, "form-group")[1:]
            for ci in range(len(rows)):
                if ci == 0:
                    id = 0
                elif ci == 8:
                    id = 0
                else:
                    id = 1

                rows[ci].find_elements(By.TAG_NAME, 'label')[id].click()
                ts(0.01, can_skip = True)

        # ACTION
        @self.error_checker
        def end_action():
            table = ts(0.5, lambda: wd.find_element(By.TAG_NAME, 'purchase-summary'))

            if i + 1 == line.COUNT_LINES:
                table.find_element(By.CLASS_NAME, 'continue').click()
            else:
                buttons = table.find_elements(By.TAG_NAME, 'button')
                if PLAN_TYPE == line.PLANS[i + 1].values():
                    need_button = 'שכפל מנוי'
                else:
                    need_button = 'הוסף מנוי נוסף'
                for b in buttons:
                    if b.text == need_button:
                        b.click()
                        ts(0.3, can_skip = True)
                # CHECK ON COPY MOVE
                if PLAN_TYPE == line.PLANS[i + 1].values():
                    option = 'דמי חיבור SIM ללא עלות'
                    options = wd.find_elements(By.CLASS_NAME, 'desing-radios')
                    for u in options:
                        if u.find_element(By.XPATH, '..').text in option:
                            u.click()
                            ts(0.01, can_skip = True)

        # AFTER PACKETS
        @self.error_checker
        def enter_email():
            table = ts(2, lambda: wd.find_element(By.TAG_NAME, 'interactive-forms'))
            lbs = table.find_elements(By.TAG_NAME, 'label')
            for uu in lbs:
                if 'ללא שליחת טפסים מקדימים' in uu.text:
                    uu.click()
                    break
            wd.find_element(By.CLASS_NAME, 'continue').click()

        # MAILING DATA
        @self.error_checker
        def enter_mailing_data():
            table = ts(2, lambda: wd.find_element(By.TAG_NAME, 'app-personaldetails'))
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

        # CITY,ADDR
        @self.error_checker
        def enter_addr():
            table = ts(0.5, lambda: wd.find_element(By.TAG_NAME, 'app-personaldetails'))
            for ii in range(2):
                if ii == 0:
                    tag = 'City'
                    parametr = line.CITY
                else:
                    tag = 'Street'
                    parametr = line.STREET

                # todo
                if table.find_elements(By.NAME, tag)[1].get_attribute('value') != '': continue

                inputs = table.find_elements(By.NAME, tag)
                options_home, input = inputs[0], inputs[1]

                for i in range(len(parametr)):
                    input.send_keys(parametr[i])
                    ts(0.5, can_skip = False)

                    options = options_home.find_elements(By.TAG_NAME, 'li')
                    if len(options) > 0:
                        count_options = len(options)

                        if count_options == 1:
                            options[0].click()
                            break

                        elif i + 1 == len(parametr):
                            options[0].click()
                            break
                    ts(1, can_skip = False)

        # PERS DATA
        @self.error_checker
        def enter_more_data():
            table = ts(0.5, lambda: wd.find_element(By.TAG_NAME, 'app-personaldetails'))
            if table.find_element(By.NAME, 'HouseNumber').get_attribute('value') == '':
                table.find_element(By.NAME, 'HouseNumber').send_keys(line.HOUSE_NUMBER)

            if table.find_element(By.NAME, 'ApartmentNumber').get_attribute('value') == '':
                table.find_element(By.NAME, 'ApartmentNumber').send_keys(line.APART_NUMBER)

            if table.find_element(By.NAME, 'POBox').get_attribute('value') == '':
                table.find_element(By.NAME, 'POBox').send_keys(line.POBox)
            wd.find_element(By.CLASS_NAME, 'continue').click()

        # DROP CITY,ADDR
        @self.error_checker
        def enter_more_data2():
            table = ts(2, lambda: wd.find_element(By.TAG_NAME, 'retail-deliverytype'))
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

                # todo
                if input.get_attribute('value') != '': continue

                for i in range(len(parameter)):
                    input.send_keys(parameter[i])
                    ts(1.5, can_skip = False)

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
                ts(1.5, can_skip = False)
            element = table.find_element(By.NAME, 'houseNumber')
            if element.get_attribute('value') == '': element.send_keys(line.HOUSE_NUMBER)
            element = table.find_element(By.NAME, 'apartmentNumber')
            if element.get_attribute('value') == '': element.send_keys(line.APART_NUMBER)
            ts(2, lambda: wd.find_element(By.CLASS_NAME, 'continue')).click()

        # CARD
        @self.error_checker
        def enter_card():
            table = ts(1, lambda: wd.find_element(By.TAG_NAME, 'payemnt-comp'))
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
        @self.error_checker
        def save():
            ts(1, lambda: wd.find_element(By.CLASS_NAME, 'continue')).click()
            boxes = ts(1, lambda: wd.find_elements(By.CLASS_NAME, 'box'))

            if len(boxes) == 1:
                box = boxes[0]
                last_er = box.find_element(By.TAG_NAME, 'h3').text

                self.MainSheet.set_value('AM', line.index, last_er)
                # labels[lab_index].config(text = last_er)

            else:
                kod1 = self.web_driver.find_element(By.XPATH, 
                    '/html/body/app-root/master-page/div/div[2]/div[1]/app-purchase/form/div/thank-you/div/div/div[2]/div[3]/div[1]').text
                kod2 = self.web_driver.find_element(By.XPATH, 
                    '/html/body/app-root/master-page/div/div[2]/div[1]/app-purchase/form/div/thank-you/div/div/div[2]/div[1]/div/div[3]').text

                self.MainSheet.set_value('AM', line.index, kod1 + ' ' + kod2)
                # labels[indexxx].config(text = kod1 + ' ' + kod2)

        # PLAN
        if open_link():
            return

        TYPE_USER = 'undefined'
        for i in range(len(line.COUNT_LINES)):
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
        if enter_addr(): return
        if enter_more_data(): return
        if enter_more_data2(): return
        if enter_card(): return

        self.Status.set_status("end")
        self.Save.change_position(1, "finish")

        command = self.Save.wait_command()
        if command:
            save()
