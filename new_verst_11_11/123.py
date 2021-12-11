from config import *
# t_m_c = 1.5

t_m_c = 5


class Worker:
    def __init__(self, stack, name_numb, change_state_save, change_state_error, reload_button_start, type_error,
                 type_save):
        self.web_driver = None
        self.stack = stack
        self.name_numb = name_numb

        # func
        self.change_state_error = change_state_error
        self.change_state_save = change_state_save
        self.reload_button_start = reload_button_start

        self.type_error = type_error
        self.type_save = type_save

        self.status_label = None

    def start(self):
        time.sleep(random.randint(100,299)/100)
        with open('settings.txt', 'r') as file:
            passw = json.loads(file.read())[self.name_numb]

        def get_mes():
            import imaplib
            mail = imaplib.IMAP4_SSL('imap.gmail.com')

            mail.login(passw['gmail'], passw['password'])
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

        self.status_label.config(text = 'Запуск хром')
        options = webdriver.ChromeOptions()
        self.web_driver = webdriver.Chrome(chrome_options = options, executable_path = "webDriver/chromedriver.exe")

        name = str(self.name_numb)

        self.web_driver.execute_script("window.open('http://" + name + ".com', '_blank');")
        time.sleep(1)
        self.web_driver.switch_to_window(self.web_driver.window_handles[0])
        self.status_label.config(text = 'Переход на сайт')
        self.web_driver.get('https://retailsys.hotnet.net.il/Login')
        time.sleep(t_m_c * 2)

        if passw['auto_login'] == 0:
            return

        # LOGGING
        SMS_LAST = get_mes()
        self.web_driver.find_elements_by_tag_name('input')[0].send_keys(passw['user_name'])
        self.web_driver.find_elements_by_tag_name('input')[1].click()
        time.sleep(t_m_c * 2)

        # SMS_ENTER
        self.status_label.config(text = 'Ввод смс')
        while 1:
            SMS = get_mes()
            if SMS != SMS_LAST: break
            time.sleep(1)
        self.web_driver.find_elements_by_tag_name('input')[0].send_keys(SMS)
        self.web_driver.find_elements_by_tag_name('input')[1].click()

    def polling(self):
        self.start()

        while 1:
            if len(self.stack) == 0:
                time.sleep(1)
                self.status_label.config(text = 'Ожидание старта линии')
            else:
                line = self.stack.pop()
                self.reload_button_start()
                self.enter_line(line)

    def enter_line(self, line):
        print('start_enter')

        def have_error():
            self.type_error[0] = 0
            self.change_state_error(1)

            while self.type_error[0] == 0:
                time.sleep(1)

            self.change_state_error(0)

            if self.type_error[0] == 1:
                print('next')
                return 'next'  # next
            elif self.type_error[0] == -2:
                print('rep')
                return 'rep'  # repeat
            else:
                print('cans')
                return 'cans'

        NAME_CARDS = line.NAME_CARDS
        PLAN_TYPES = line.PLAN_TYPES
        NEED_OPTIONS = line.NEED_OPTIONS
        NUMBERS = line.NUMBERS

        PASSPORT = line.PASSPORT
        NUMBER_USER = line.NUMBER_USER
        NAME = line.NAME
        SURNAME = line.SURNAME
        CITY = line.CITY
        HOUSE_NUMBER, APART_NUMBER, STREET = line.HOUSE_NUMBER, line.APART_NUMBER, line.STREET
        POBox = line.POBox
        CARD = line.CARD
        SROK = line.SROK
        TYPE_PAY = line.TYPE_PAY

        self.status_label.config(text = 'Переход на старницу тарифов')
        self.web_driver.get('https://retailsys.hotnet.net.il/HotMobile/HMPurchase')
        time.sleep(t_m_c * 2)

        for i in range(len(NAME_CARDS)):
            NAME_CARD, PLAN_TYPE, NUMB, ND_OPTION = NAME_CARDS[i], PLAN_TYPES[i], NUMBERS[i], NEED_OPTIONS[i]

            # CHECK ON COPY
            COPY = 0
            if i != 0:
                if PLAN_TYPES[i-1] == PLAN_TYPE:
                    COPY = 1
                    option = 'דמי חיבור SIM ללא עלות'
                    options = self.web_driver.find_elements_by_class_name('desing-radios')
                    for u in options:
                        if u.find_element_by_xpath('..').text in option:
                            u.click()
                            time.sleep(0.01)

            # CHOOSE PLANS
            while 1:
                if COPY:break
                self.status_label.config(text = 'Выбор тарифа')
                time.sleep(t_m_c * 0.5)
                try:
                    plans_type = self.web_driver.find_elements_by_class_name('plan-type')
                    plans_type[PLAN_TYPE].find_element_by_xpath('..').click()
                    break
                except:
                    it = have_error()
                    if it == 'next':
                        break
                    elif it == 'cans':
                        return

                    # CARD

            # CARD
            while 1:
                if COPY:break
                self.status_label.config(text = 'Кнопка карты')
                time.sleep(t_m_c * 0.5)
                try:
                    all_cards = self.web_driver.find_elements_by_class_name('card-title')
                    for ci in all_cards:
                        if ci.text == NAME_CARD:
                            but = ci.find_element_by_xpath('..').find_element_by_xpath('..')
                            but.find_element_by_class_name('btn').click()
                    break
                except:
                    it = have_error()
                    if it == 'next':
                        break
                    elif it == 'cans':
                        return

                    # CHECK ON REG

            # CHECK ON REG
            while 1:
                if COPY: break
                self.status_label.config(text = 'Проверка на регистрацию')
                time.sleep(t_m_c * 2)
                try:
                    if i == 0:
                        # LEFT_BUTTON
                        dialog = self.web_driver.find_element_by_tag_name('client-eligibility')
                        h2 = dialog.find_elements_by_tag_name('h2')[1].click()

                        # CHECK ALREADY REG
                        dialog = self.web_driver.find_element_by_tag_name('client-eligibility')
                        dialog.find_element_by_tag_name('input').send_keys(PASSPORT)
                        dialog.find_elements_by_tag_name('button')[0].click()
                        time.sleep(t_m_c * 2)

                        k = 0
                        # error
                        try:
                            if self.web_driver.find_element_by_class_name('invalid-feedback').text != '':
                                type_user = 'error'
                        except:
                            pass

                        # already
                        try:
                            if len(self.web_driver.find_elements_by_name('clientPhoneNumber')) == 1:
                                # clientPhoneNumber
                                type_user = 'already'
                        except:
                            pass

                        # button
                        try:
                            if 'ללקוח זה נמצאה הזמנה פעילה, האם ברצונך להמשיך?' in self.web_driver.find_element_by_tag_name(
                                    'client-eligibility').text:
                                type_user = 'button'
                        except:
                            pass

                        # new
                        try:
                            if len(self.web_driver.find_elements_by_name('clientId')) != 1 and k == 0:
                                type_user = 'new'
                        except:
                            pass
                        print(type_user)
                        if type_user == 'error': 1 / 0
                        if type_user == 'already':
                            self.web_driver.find_element_by_name('clientPhoneNumber').send_keys(NUMBER_USER)
                            self.web_driver.find_element_by_name('clientLastFourDigits').send_keys(CARD[-4:])
                            dialogs = self.web_driver.find_element_by_tag_name('client-eligibility')
                            dialogs.find_elements_by_tag_name('button')[0].click()
                        if type_user == 'button':
                            dialogs = self.web_driver.find_element_by_tag_name('client-eligibility')
                            dialogs.find_elements_by_tag_name('button')[0].click()
                            self.web_driver.find_element_by_name('clientPhoneNumber').send_keys(NUMBER_USER)
                            self.web_driver.find_element_by_name('clientLastFourDigits').send_keys(CARD[-4:])
                            dialogs = self.web_driver.find_element_by_tag_name('client-eligibility')
                            dialogs.find_elements_by_tag_name('button')[0].click()
                            type_user = 'already'
                    break
                except:
                    it = have_error()
                    if it == 'next':
                        break
                    elif it == 'cans':
                        return

                    # ===========OPTIONS PAGE

            # ===========OPTIONS PAGE
            # 1first_table,2second options
            while 1:
                if COPY:break
                self.status_label.config(text = 'Отмечение параметров')
                time.sleep(t_m_c * 2)
                try:
                    options = self.web_driver.find_elements_by_class_name('desing-radios')
                    for u in options:
                        if u.find_element_by_xpath('..').text in ND_OPTION:
                            u.click()
                            time.sleep(0.01)


                    break
                except:
                    it = have_error()
                    if it == 'next':
                        break
                    elif it == 'cans':
                        return

                    # 3third_table number

            # 3third_table number
            while 1:
                self.status_label.config(text = 'Ввод номера')
                time.sleep(t_m_c * 0.5)
                try:
                    table = self.web_driver.find_element_by_tag_name('portability-comp')
                    labels = table.find_elements_by_tag_name('label')
                    if type_user == 'new' and NUMB != 'חדש':
                        try:
                            labels[1].click()
                            table.find_element_by_name('phone').send_keys(NUMB)
                            table.find_element_by_tag_name('button').click()
                            time.sleep(t_m_c * 2)
                            table = self.web_driver.find_element_by_tag_name('portability-comp')
                            table.find_elements_by_name('verifyNeeded')[1].find_element_by_xpath('..').click()
                            time.sleep(t_m_c * 1)
                        except:
                            pass
                        # enter users data
                        table.find_element_by_name('firstName').send_keys(NAME)
                        table.find_element_by_name('lastName').send_keys(SURNAME)
                        table.find_element_by_name('userId').send_keys(PASSPORT)
                        table.find_element_by_name('lastCompany').find_elements_by_tag_name('option')[0].click()
                        table.find_element_by_name('agreement').click()
                    else:
                        labels[0].click()
                    break
                except:
                    it = have_error()
                    if it == 'next':
                        break
                    elif it == 'cans':
                        return

                    # 5fifth_table tab enter

            # 5fifth_table tab enter
            while 1:
                if COPY:break
                self.status_label.config(text = 'Отмечение последних параметров')
                time.sleep(t_m_c * 0.5)
                try:
                    table = self.web_driver.find_element_by_tag_name('regulations-comp')
                    rows = table.find_elements_by_class_name("form-group")[1:]
                    for ci in range(len(rows)):
                        if ci == 0:
                            id = 0
                        elif ci == 8:
                            id = 0
                        else:
                            id = 1


                        rows[ci].find_elements_by_tag_name('label')[id].click()
                        time.sleep(0.01)
                    break
                except:
                    it = have_error()
                    if it == 'next':
                        break
                    elif it == 'cans':
                        return

                    # ACTION

            # ACTION
            while 1:
                self.status_label.config(text = 'Выбор: добавить/копировать пакет|ввод перс.данных')
                time.sleep(t_m_c * 0.5)
                try:
                    table = self.web_driver.find_element_by_tag_name('purchase-summary')

                    if i + 1 == len(NAME_CARDS):
                        table.find_element_by_class_name('continue').click()
                    else:
                        buttons = table.find_elements_by_tag_name('button')
                        for b in buttons:
                            # CHECK IN COPY
                            if PLAN_TYPE == PLAN_TYPES[i + 1]:
                                if b.text == 'שכפל מנוי':
                                    b.click()
                                    time.sleep(t_m_c * 0.3)
                                    break
                            else:
                                if b.text == 'הוסף מנוי נוסף':
                                    b.click()
                                    break
                    break
                except:
                    it = have_error()
                    if it == 'next':
                        break
                    elif it == 'cans':
                        return

                    # AFTER PACKETS

        # AFTER PACKETS
        while 1:
            self.status_label.config(text = 'Ввод mail')
            time.sleep(t_m_c * 2)
            try:
                table = self.web_driver.find_element_by_tag_name('interactive-forms')

                lbs = table.find_elements_by_tag_name('label')
                for uu in lbs:
                    if 'ללא שליחת טפסים מקדימים' in uu.text:
                        uu.click()
                        break

                self.web_driver.find_element_by_class_name('continue').click()

                break
            except:
                it = have_error()
                if it == 'next':
                    break
                elif it == 'cans':
                    return

        # MAILING DATA
        while 1:
            self.status_label.config(text = 'Ввод перс. данных')
            time.sleep(t_m_c * 2)
            try:
                table = self.web_driver.find_element_by_tag_name('app-personaldetails')
                if table.find_element_by_name('Phone').get_attribute('value') == '':
                    table.find_element_by_name('Phone').send_keys(NUMBER_USER)

                divs = table.find_elements_by_tag_name('div')
                for uu in divs:
                    if 'דואר ישראל' == uu.text:
                        print('ok')
                        uu.find_elements_by_tag_name('label')[0].click()
                        break

                if type_user == 'already': break

                table.find_element_by_name('FirstName').send_keys(NAME)
                table.find_element_by_name('LastName').send_keys(SURNAME)
                break
            except:
                it = have_error()
                if it == 'next':
                    break
                elif it == 'cans':
                    return

                # CITY,ADDR

        # CITY,ADDR
        while 1:
            self.status_label.config(text = 'Ввод адреса')
            time.sleep(t_m_c * 0.5)
            try:
                table = self.web_driver.find_element_by_tag_name('app-personaldetails')
                for ii in range(2):
                    if ii == 0:
                        tag = 'City'
                        parametr = CITY
                    else:
                        tag = 'Street'
                        parametr = STREET

                    if table.find_elements_by_name(tag)[1].get_attribute('value') != '': continue

                    inputs = table.find_elements_by_name(tag)
                    options_home, input = inputs[0], inputs[1]

                    for i in range(len(parametr)):
                        input.send_keys(parametr[i])
                        time.sleep(t_m_c * 0.5)

                        # try:
                        options = options_home.find_elements_by_tag_name('li')
                        if len(options) > 0:
                            count_options = len(options)

                            if count_options == 1:
                                options[0].click()
                                break

                            elif i + 1 == len(parametr):
                                options[0].click()
                                break
                    time.sleep(t_m_c * 1)
                break
            except:
                it = have_error()
                if it == 'next':
                    break
                elif it == 'cans':
                    return

        # PERS DATA
        while 1:
            self.status_label.config(text = 'Ввод данных, продолжить')
            time.sleep(t_m_c * 0.5)
            try:
                if table.find_element_by_name('HouseNumber').get_attribute('value') == '':
                    table.find_element_by_name('HouseNumber').send_keys(HOUSE_NUMBER)

                if table.find_element_by_name('ApartmentNumber').get_attribute('value') == '':
                    table.find_element_by_name('ApartmentNumber').send_keys(APART_NUMBER)

                if table.find_element_by_name('POBox').get_attribute('value') == '':
                    table.find_element_by_name('POBox').send_keys(POBox)
                self.web_driver.find_element_by_class_name('continue').click()
                break
            except:
                it = have_error()
                if it == 'next':
                    break
                elif it == 'cans':
                    return

                # DROP CITY,ADDR

        # DROP CITY,ADDR
        while 1:
            self.status_label.config(text = 'Ввод данных2')
            time.sleep(t_m_c * 2)
            try:
                table = self.web_driver.find_element_by_tag_name('retail-deliverytype')
                for ii in range(2):
                    if ii == 0:
                        tag = 'City'
                        parametr = CITY
                    else:
                        tag = 'Street'
                        parametr = STREET

                    if table.find_elements_by_name(tag)[1].get_attribute('value') != '': continue

                    inputs = table.find_elements_by_name(tag)
                    options_home, input = inputs[0], inputs[1]
                    if input.get_attribute('value') != '': continue

                    for i in range(len(parametr)):
                        input.send_keys(parametr[i])
                        time.sleep(t_m_c * 1.5)

                        # try:
                        options = options_home.find_elements_by_tag_name('li')
                        if len(options) > 0:
                            count_options = len(options)

                            if count_options == 1:
                                options[0].click()
                                break

                            elif i + 1 == len(parametr):
                                options[0].click()
                                break
                        # except:pass
                    time.sleep(t_m_c * 3)
                element = table.find_element_by_name('houseNumber')
                if element.get_attribute('value') == '': element.send_keys(HOUSE_NUMBER)
                element = table.find_element_by_name('apartmentNumber')
                if element.get_attribute('value') == '': element.send_keys(APART_NUMBER)
                time.sleep(t_m_c * 2)

                self.web_driver.find_element_by_class_name('continue').click()
                break
            except:
                it = have_error()
                if it == 'next':
                    break
                elif it == 'cans':
                    return

                # CARD

        # CARD
        while 1:
            self.status_label.config(text = 'Ввод карты')
            time.sleep(t_m_c * 1)
            try:
                if type_user == 'already':
                    table = self.web_driver.find_element_by_tag_name('payemnt-comp')
                    table.find_element_by_tag_name('label').click()
                    break

                if TYPE_PAY == 'card':
                    table = self.web_driver.find_element_by_tag_name('payemnt-comp')
                    table.find_element_by_name('creditCardNumber').send_keys(CARD)
                    table.find_element_by_name('creditCardHolderId').send_keys(PASSPORT)

                else:
                    table.find_element_by_name('bankOrderClientId').send_keys(CARD)
                    table.find_element_by_name('bankOrderFirstName').send_keys(CARD)
                    table.find_element_by_name('bankOrderLastName').send_keys(CARD)

                options = self.web_driver.find_elements_by_class_name('desing-radios')
                for u in options:
                    u.click()
                break
            except:
                it = have_error()
                if it == 'next':
                    break
                elif it == 'cans':
                    return

        # FINISH
        self.status_label.config(text = 'Конец')
        self.change_state_save(1)

        self.type_save[0] = 0
        while self.type_save[0] == 0:
            time.sleep(1)

        if self.type_save[0] == -1: return

        # SAVE
        while 1:
            self.status_label.config(text = 'Сохранение данных')
            time.sleep(t_m_c * 1)
            try:
                self.web_driver.find_element_by_class_name('continue').click()
                time.sleep(t_m_c * 1)
                boxes = self.web_driver.find_elements_by_class_name('box')

                wb = load_workbook(r'123.xlsx')
                for i in wb:
                    sheet = wb[str(i)[12:-2]]

                if len(boxes) == 1:
                    box = boxes[0]
                    last_er = box.find_element_by_tag_name('h3').text

                    sheet["AM" + str(line.index)].value = last_er
                    # labels[lab_index].config(text = last_er)

                else:
                    kod1 = self.web_driver.find_element_by_xpath(
                        '/html/body/app-root/master-page/div/div[2]/div[1]/app-purchase/form/div/thank-you/div/div/div[2]/div[3]/div[1]').text
                    kod2 = self.web_driver.find_element_by_xpath(
                        '/html/body/app-root/master-page/div/div[2]/div[1]/app-purchase/form/div/thank-you/div/div/div[2]/div[1]/div/div[3]').text

                    sheet["AM" + str(line.index)].value = kod1 + ' ' + kod2
                    # labels[indexxx].config(text = kod1 + ' ' + kod2)
            except:
                it = have_error()
                if it == 'next':
                    break
                elif it == 'cans':
                    return


class Lines_base:
    def __init__(self, canvas, name_numb):
        self.name_numb = name_numb
        self.canvas = canvas
        self.lines = []
        self.stack = []
        self.type_error = [0]
        self.type_save = [0]
        self.status_label = None

        self.worker = Worker(self.stack, name_numb, self.change_state_save, self.change_state_error,
                             self.reload_button_start,
                             self.type_error, self.type_save)

        # labels
        self.label_status_error = None
        self.btn_error_next = None
        self.btn_error_repeat = None
        self.btn_error_cancel = None

        self.label_status_end = None
        self.btn_end_save = None
        self.btn_end_next = None

    def place_lines(self, list_lines):
        def change_error(stat):
            self.type_error[0] = stat
            self.change_state_error(0)

        def change_save(stat):
            self.type_save[0] = stat
            self.change_state_save(0)

        self.status_label = Label(self.canvas, text = 'start', background = "white")
        self.status_label.place(x = 0, y = 0, width = width_block)
        self.worker.status_label = self.status_label

        self.label_status_error = Label(self.canvas, text = '🔴', background = "white", fg = 'white')
        self.label_status_error.place(x = 0, y = 25, width = 20)

        self.btn_error_next = Button(self.canvas, text = 'next▶', fg = 'green', background = "white", state = DISABLED,
                                     command = lambda: change_error(1))
        self.btn_error_next.place(x = 20, y = 25, width = 60)
        self.btn_error_repeat = Button(self.canvas, text = 'repeat♻️', fg = '#C5AA00', background = "white",
                                       state = DISABLED, command = lambda: change_error(-2))
        self.btn_error_repeat.place(x = 80, y = 25, width = 60)
        self.btn_error_cancel = Button(self.canvas, text = 'cancel❌', fg = 'red', background = "white",
                                       state = DISABLED, command = lambda: change_error(-1))
        self.btn_error_cancel.place(x = 140, y = 25, width = 60)

        self.label_status_end = Label(self.canvas, text = '🔴', background = "white", fg = 'white')
        self.label_status_end.place(x = 0, y = 50, width = 20)

        self.btn_end_save = Button(self.canvas, text = 'save', fg = 'green', background = "white", state = DISABLED,
                                   command = lambda: change_save(1))
        self.btn_end_save.place(x = 20, y = 50, width = 60)
        self.btn_end_next = Button(self.canvas, text = 'next', fg = '#C5AA00', background = "white", state = DISABLED,
                                   command = lambda: change_save(-1))
        self.btn_end_next.place(x = 80, y = 50, width = 60)

        btn_settings = Button(self.canvas, text = '⚙', fg = 'grey', background = "white",
                              command = lambda: self.change_settings())
        btn_settings.place(x = 355, y = 25, width = 20, height = 20)

        count = 0
        for ind in list_lines:
            new_canv = Frame(self.canvas, background = "grey90")
            new_canv.place(x = 0, y = (height_line + height_line_ots) * count + 85, width = width_block,
                           height = height_line)

            cur_line = Line(ind, self.stack, self.reload_button_start, self.name_numb)
            cur_line.place(new_canv, count)
            self.lines.append(cur_line)

            count += 1

        if count != 0:
            threading.Thread(target = self.worker.polling).start()

    def reload_button_start(self):
        for i in self.lines:
            if i.type == 'in_stack':
                if i in self.stack:
                    i.button_start.configure(fg = 'red', text = str(self.stack.index(i) + 1))
                else:
                    i.button_start.configure(fg = 'red', text = '0')
            else:
                i.button_start.configure(fg = 'green', text = '▶')

    def change_settings(self):
        def save():
            with open('settings.txt', 'r') as file:
                paswd = json.loads(file.read())
            paswd[self.name_numb]['password'] = messages2.get()
            paswd[self.name_numb]['gmail'] = messages.get()
            paswd[self.name_numb]['user_name'] = messages3.get()
            paswd[self.name_numb]['auto_login'] = int(rad_variable.get())

            with open('settings.txt', 'w') as file:
                file.write(json.dumps(paswd))
            root1.destroy()

        root1 = Tk()
        root1.resizable(width = False, height = False)

        canvas2 = Canvas(root1, background = "grey90", width = 300, height = 120)
        canvas2.pack(side = "bottom", fill = "both", expand = True)

        messages = StringVar(root1)
        messages2 = StringVar(root1)
        messages3 = StringVar(root1)

        with open('settings.txt', 'r') as file:
            paswd = json.loads(file.read())[self.name_numb]

        label = Label(canvas2, text = 'mail', background = "grey90")
        label.place(x = 5, y = 5, width = 70)
        message_entry1 = Entry(canvas2, textvariable = messages)
        message_entry1.place(x = 80, y = 5, width = 200)
        message_entry1.insert(0, paswd['gmail'])

        label = Label(canvas2, text = 'password', background = "grey90")
        label.place(x = 5, y = 30, width = 70)
        message_entry2 = Entry(canvas2, textvariable = messages2)
        message_entry2.place(x = 80, y = 30, width = 200)
        message_entry2.insert(0, paswd['password'])

        label = Label(canvas2, text = 'id', background = "grey90")
        label.place(x = 5, y = 55, width = 70)
        message_entry2 = Entry(canvas2, textvariable = messages3)
        message_entry2.place(x = 80, y = 55, width = 200)
        message_entry2.insert(0, paswd['user_name'])

        label = Label(canvas2, text = 'auto-login', background = "grey90")
        label.place(x = 5, y = 80, width = 70)
        rad_variable = IntVar(root1)
        if paswd['auto_login'] == 1:
            rad_variable.set(1)
        r1 = Checkbutton(canvas2, variable = rad_variable, onvalue = '1', offvalue = '0', background = "grey90")
        r1.place(x = 80, y = 80)

        btn_settings = Button(canvas2, text = 'Save', background = "grey90",
                              command = lambda: save())
        btn_settings.place(x = 120, y = 100, width = 60, height = 20)

    def destr(self):
        self.canvas.destroy()

    def change_state_error(self, state):
        if state == 1:
            self.label_status_error.configure(fg = 'red')
            self.btn_error_next.configure(state = NORMAL)
            self.btn_error_repeat.configure(state = NORMAL)
            self.btn_error_cancel.configure(state = NORMAL)
        else:
            self.label_status_error.configure(fg = 'white')
            self.btn_error_next.configure(state = DISABLED)
            self.btn_error_repeat.configure(state = DISABLED)
            self.btn_error_cancel.configure(state = DISABLED)

    def change_state_save(self, state):
        if state == 1:
            self.label_status_end.configure(fg = 'green')
            self.btn_end_save.configure(state = NORMAL)
            self.btn_end_next.configure(state = NORMAL)
        else:
            self.label_status_end.configure(fg = 'white')
            self.btn_end_save.configure(state = DISABLED)
            self.btn_end_next.configure(state = DISABLED)


class Line:
    def __init__(self, index, stack, reload_button, name_numb):
        self.type = 'wait'
        self.canvas = None
        self.stack = stack
        self.numb = None
        self.index = index
        self.name_numb = name_numb

        # lines
        self.count_lines = None
        self.tarifs = []
        self.NAME_CARDS = []
        self.PLAN_TYPES = []
        self.NEED_OPTIONS = []
        self.NUMBERS = []

        # data
        self.PASSPORT = None
        self.NAME = None
        self.SURNAME = None
        self.CITY = None
        self.STREET = None
        self.APART_NUMBER = None
        self.HOUSE_NUMBER = None
        self.NUMBER_USER = None
        self.POBox = '000'
        self.TYPE_PAY = None
        self.SROK = None
        self.CARD = None

        # func
        self.reload_button = reload_button

        # canv
        self.button_start = None

        self.load()

    def load(self):
        # lines
        wb = load_workbook(r'123.xlsx')
        for i in wb:
            sheet = wb[str(i)[12:-2]]
        self.count_lines = int(sheet["S" + str(self.index)].value)

        wb_2 = load_workbook(r'plans.xlsx')
        for i in wb_2:
            sheet_plans = wb_2[str(i)[12:-2]]

        for i in range(self.count_lines):
            cur_num = str(sheet["G" + str(self.index + i)].value)
            if len(cur_num) == 9: cur_num = '0' + cur_num
            self.NUMBERS.append(cur_num)

            cur_name = str(sheet["V" + str(self.index + i)].value)

            ind_plan_ch = 1
            while 1:
                if sheet_plans['A' + str(ind_plan_ch)].value == None:
                    break
                    1 / 0
                elif cur_name == sheet_plans['A' + str(ind_plan_ch)].value:
                    cur_plan = sheet_plans['B' + str(ind_plan_ch)].value
                    if self.name_numb in [0,3]:
                        cur_plan_type = sheet_plans['C' + str(ind_plan_ch)].value
                    else:
                        cur_plan_type = sheet_plans['D' + str(ind_plan_ch)].value
                    cur_options = sheet_plans['E' + str(ind_plan_ch)].value.split(',')

                    # unique symbol
                    if str(sheet[f'BD{self.index}'].value) == 'כן':
                        cur_options.append('חודש ראשון ללא עלות')

                    break
                else:
                    ind_plan_ch += 1

            self.NAME_CARDS.append(cur_plan)
            self.PLAN_TYPES.append(cur_plan_type)
            self.NEED_OPTIONS.append(cur_options)
            self.tarifs.append(cur_name)

        # info
        def fix_city(name):
            name_d = name
            for ww in range(1, len(name_d)):
                if name_d[-ww] == ' ':
                    name = name_d[:-ww]
                else:
                    break
            return name

        def fix_street(name):
            addrs = name
            for w in range(len(addrs)):
                try:
                    int(addrs[w])
                    addr_street = (addrs[:w - 1])
                    e = addr_street
                    for ww in range(1, len(e)):
                        if e[-ww] == ' ':
                            addr_street = e[:-ww]
                        else:
                            break
                    break
                except:
                    pass
            addr_numb_hous, addr_numb_kv = re.sub(r'\D', ' ', addrs).split()
            return addr_numb_hous, addr_numb_kv, addr_street

        self.PASSPORT = str(sheet["D" + str(self.index)].value)
        self.NAME = str(sheet["E" + str(self.index)].value)
        self.SURNAME = str(sheet["Z" + str(self.index)].value)
        self.CITY = fix_city(str(sheet["AA" + str(self.index)].value))
        self.NUMBER_USER = str(sheet["AC" + str(self.index)].value)
        self.HOUSE_NUMBER, self.APART_NUMBER, self.STREET = fix_street(str(sheet["AB" + str(self.index)].value))

        if len(self.NUMBER_USER) == 9: self.NUMBER_USER = '0' + self.NUMBER_USER
        if len(self.PASSPORT) == 8: self.PASSPORT = '0' + self.PASSPORT

        self.TYPE_PAY = str(sheet["AF" + str(self.index)].value)
        if 'הוראת קבע' not in self.TYPE_PAY:
            self.TYPE_PAY = 'card'
            self.CARD = str(sheet["AO" + str(self.index)].value)
            self.SROK = str(sheet["AP" + str(self.index)].value).split('/')
            if self.SROK[0] == '0': self.SROK[0] = self.SROK[0][1:]
            if self.SROK[1] == '0': self.SROK[1] = self.SROK[1][1:]
        else:
            self.TYPE_PAY = 'bank'

    def change_line(self):
        def save():
            wb = load_workbook(r'123.xlsx')
            for i in wb:
                sheet = wb[str(i)[12:-2]]
            brt = int(sheet["S" + str(self.index)].value)
            for i in range(brt):
                sheet["E" + str(self.index + i)].value = messages.get()
                sheet["Z" + str(self.index + i)].value = messages2.get()
                sheet["G" + str(self.index + i)].value = numss[i].get()
                sheet["V" + str(self.index + i)].value = kreds[i].get()
                sheet["AU" + str(self.index + i)].value = radiobuts[i].get()
            wb.save('123.xlsx')

        root1 = Tk()
        root1.resizable(width = False, height = False)

        canvas2 = Canvas(root1, background = "grey90", width = 500, height = 60 + 40 * self.count_lines)
        canvas2.pack(side = "bottom", fill = "both", expand = True)

        messages = StringVar(root1)
        messages2 = StringVar(root1)

        message_entry1 = Entry(canvas2, textvariable = messages)
        message_entry1.place(x = 5, y = 5, width = 100)
        message_entry1.insert(0, self.NAME)
        message_entry2 = Entry(canvas2, textvariable = messages2)
        message_entry2.place(x = 110, y = 5, width = 100)
        message_entry2.insert(0, self.SURNAME)

        lis_v = []
        wb_2 = load_workbook(r'plans.xlsx')
        for i in wb_2:
            sheet_plans = wb_2[str(i)[12:-2]]

        ind_plan_ch = 1
        while 1:
            if sheet_plans['A' + str(ind_plan_ch)].value is None:
                break
            else:
                lis_v.append(sheet_plans['A' + str(ind_plan_ch)].value)
                ind_plan_ch += 1

        numss = []
        kreds = []
        radiobuts = []
        for ii in range(int(self.count_lines)):
            nums = str(self.NUMBERS[ii])
            tar = str(self.tarifs[ii])
            wb = load_workbook(r'123.xlsx')
            for i in wb:
                sheet = wb[str(i)[12:-2]]
            check_b = (sheet["AU" + str(self.index + ii)].value)

            mes = StringVar(root1)
            message_entry = Entry(canvas2, textvariable = mes)
            message_entry.place(x = 5, y = 30 + 40 * ii, width = 205)
            message_entry.insert(0, nums)
            numss.append(message_entry)

            var = StringVar(root1)
            var.set(tar)
            opt = OptionMenu(canvas2, var, *lis_v)
            opt.place(x = 210, y = 30 + 40 * ii, width = 205)
            kreds.append(var)

            rad_variable = IntVar(root1)
            if check_b == 1:
                rad_variable.set(1)
            r1 = Checkbutton(canvas2, text = '1', variable = rad_variable, onvalue = '1', offvalue = '0')
            r1.place(x = 420, y = 30 + 40 * ii, width = 30)
            radiobuts.append(rad_variable)

        message_button = Button(canvas2, text = "Save",
                                command = lambda: save())

        message_button.place(x = 210, y = 30 + 40 * (ii + 1))
        root1.mainloop()

    def add_stack(self):
        if self.type == 'wait':
            self.type = 'in_stack'
            self.stack.append(self)
        else:
            if self in self.stack:
                self.stack.pop(self.stack.index(self))
                self.type = 'wait'
        self.reload_button()
        print(self.stack)

    def place(self, canvas, numb):
        self.canvas = canvas
        self.numb = numb

        lab = Label(self.canvas, text = str(self.numb), background = "grey90")
        lab.place(x = 0, y = 0, width = 20)

        btn4 = Button(self.canvas, text = str(self.count_lines), command = lambda: self.change_line())
        btn4.place(x = 20, y = 0, width = 20)

        lab = Label(self.canvas, text = self.NAME, background = "grey90")
        lab.place(x = 40, y = 0, width = 40)

        lab = Label(self.canvas, text = self.SURNAME, width = 1, background = "white")
        lab.place(x = 80, y = 0, width = 50)

        lab = Label(self.canvas, text = self.PASSPORT, width = 1, background = "grey90")
        lab.place(x = 130, y = 0, width = 60)

        lab = Label(self.canvas, text = self.CITY, width = 1, background = "white")
        lab.place(x = 190, y = 0, width = 85)

        lab = Label(self.canvas, text = self.STREET, width = 1, background = "grey90")
        lab.place(x = 275, y = 0, width = 80)

        self.button_start = Button(self.canvas, text = '▶', fg = 'green', command = lambda: self.add_stack())
        self.button_start.place(x = 355, y = 0, width = 20)


try:
    root = Tk()
    root.geometry('1515x700+300+200')
    root.resizable(width = False, height = False)
    # ✅🟢 ▶️ ⚙️ ❌✅  🔴🟢
    height_main = 700
    width_main = 1515

    width_block = 375
    width_ots = 5
    height_ots_lines = 20

    height_line = 20
    height_line_ots = 2

    canvas_main = Canvas(root, background = "grey90", width = width_main, height = height_main)
    canvas_main.place(x = 0, y = 0)

    canv_1 = Frame(canvas_main, background = "white", width = width_block, height = height_main)
    canv_1.place(x = 0)
    canv_2 = Frame(canvas_main, background = "white", width = width_block, height = height_main)
    canv_2.place(x = (width_block + width_ots) * 1)
    canv_3 = Frame(canvas_main, background = "white", width = width_block, height = height_main)
    canv_3.place(x = (width_block + width_ots) * 2)
    canv_4 = Frame(canvas_main, background = "white", width = width_block, height = height_main)
    canv_4.place(x = (width_block + width_ots) * 3)

    sort_keys = [['צוות נוטשים', 'נוטשים'], ['צוות נוטשים', 'WB'], ['צוות WB', 'WB'], ['צוות WB', 'נוטשים']]

    canvs = [canv_1, canv_2, canv_3, canv_4]

    lab = Label(canv_1, text = ' - '.join(sort_keys[0]), background = "grey90")
    lab.place(x = 0, y = 0, width = 375)
    lab = Label(canv_2, text = ' - '.join(sort_keys[1]), background = "grey90")
    lab.place(x = 0, y = 0, width = 375)
    lab = Label(canv_3, text = ' - '.join(sort_keys[2]), background = "grey90")
    lab.place(x = 0, y = 0, width = 375)
    lab = Label(canv_4, text = ' - '.join(sort_keys[3]), background = "grey90")
    lab.place(x = 0, y = 0, width = 375)

    destroys = []

    sort_keys = []
    wb = load_workbook(r'sort.xlsx')
    for g in wb:
        sheet = wb[str(g)[12:-2]]
    for i in [['A','B'], ['C','D'], ['E','F'], ['G','H']]:
        sort = []
        nm = 1
        while 1:
            # print(f'{i[0]}{nm}')
            if sheet[f'{i[0]}{nm}'].value:
                sort.append([sheet[f'{i[0]}{nm}'].value, sheet[f'{i[1]}{nm}'].value])
            else:
                break
            nm += 1
        sort_keys.append(sort)
    def load_wb():
        wb = load_workbook(r'123.xlsx')
        for i in wb:
            sheet = wb[str(i)[12:-2]]

        index_table = 2
        lines = []
        sort_lines = [[], [], [], []]
        while 1:
            if sheet["S" + str(index_table)].value == None: break
            count_lines = int(sheet["S" + str(index_table)].value)
            lines.append({
                'first_key': sheet["P" + str(index_table)].value,
                'second_key': sheet["M" + str(index_table)].value,
                'index': index_table
            })
            index_table += count_lines
        print(sort_keys)
        for i in lines:
            for ii in range(4):
                for keys in sort_keys[ii]:
                    if i['first_key'] == keys[0] and i['second_key'] == keys[1]:
                        sort_lines[ii].append(i['index'])

        for i in range(4):
            _canv = canvs[i]
            lines = sort_lines[i]

            cur_canvas = Frame(_canv, background = "white", width = width_block, height = height_main)
            cur_canvas.place(x = 0, y = height_ots_lines)

            cur_lines = Lines_base(cur_canvas, i)
            cur_lines.place_lines(lines)

            destroys.append(cur_lines)


    load_wb()

    import os


    def check_new():
        time.sleep(5)
        a = os.path.getmtime(r'123.xlsx')
        while 1:
            try:
                if a == os.path.getmtime(r'123.xlsx'): continue
            except:
                continue
            a = os.path.getmtime(r'123.xlsx')

            for i in destroys:
                i.destr()
            try:
                load_wb()
            except:
                pass
except Exception as e:
    print('Ошибка2:\n', traceback.format_exc())
    input()

threading.Thread(target = check_new).start()

root.mainloop()

