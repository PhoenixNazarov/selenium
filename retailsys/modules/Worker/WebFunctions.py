from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

wd: WebDriver
ts = None
PLAN_TYPE = None
NAME_CARD = None
line = None

def open_link():
    wd.get('https://retailsys.hotnet.net.il/HotMobile/HMPurchase')
    ts(2, can_skip = True)


def open_link():
    wd.get('https://retailsys.hotnet.net.il/HotMobile/HMPurchase')
    ts(2, can_skip = True)


# CHOOSE PLANS
def choose_plans():
    plans_type = ts(0.5, lambda: wd.find_elements(By.CLASS_NAME, 'plan-type'))
    plans_type[PLAN_TYPE].find_element(By.XPATH, '..').click()


# CARD
def button_card():
    all_cards = ts(0.5, lambda: wd.find_elements(By.CLASS_NAME, 'card-title'))
    for ci in all_cards:
        if ci.text == NAME_CARD:
            but = ci.find_element(By.XPATH, '..').find_element(By.XPATH, '..')
            but.find_element(By.CLASS_NAME, 'btn').click()


# CHECK ON REG
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
        if have_elements("invalid-feedback"):
            raise

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
def marking_options():
    options = ts(2, lambda: wd.find_elements(By.CLASS_NAME, 'desing-radios'))
    for u in options:
        if u.find_element(By.XPATH, '..').text in ND_OPTION:
            u.click()
            ts(0.01, can_skip = True)


# 3third_table number
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
def enter_email():
    table = ts(2, lambda: wd.find_element(By.TAG_NAME, 'interactive-forms'))
    lbs = table.find_elements(By.TAG_NAME, 'label')
    for uu in lbs:
        if 'ללא שליחת טפסים מקדימים' in uu.text:
            uu.click()
            break
    wd.find_element(By.CLASS_NAME, 'continue').click()


# MAILING DATA
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


# CITY, ADDRESS
def enter_address():
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
def save():
    ts(1, lambda: wd.find_element(By.CLASS_NAME, 'continue')).click()
    boxes = ts(1, lambda: wd.find_elements(By.CLASS_NAME, 'box'))

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
