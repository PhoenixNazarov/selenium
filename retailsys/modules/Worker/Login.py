from selenium.webdriver.common.by import By

from modules.exception.Handlers import mail_exception
import imaplib
import email
import time


@mail_exception
def get_mes(password, numb):
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


def authorization(web_driver):
    Status.set_status('start')

    password = Settings.get_data()

    name = str(numb)
    web_driver.execute_script("window.open('http://" + name + ".com', '_blank');")
    web_driver.switch_to.window(web_driver.window_handles[0])
    web_driver.get('https://retailsys.hotnet.net.il/Login')
    time.sleep(2 * TIME_DELAY_PERC)

    if password['auto_login'] == 0:
        return

    # LOGGING
    SMS_LAST = get_mes(password, numb)
    web_driver.find_elements(By.TAG_NAME, 'input')[0].send_keys(password['user_name'])
    web_driver.find_elements(By.TAG_NAME, 'input')[1].click()
    time.sleep(2)
    Status.set_status('enter_sms')
    while 1:
        SMS = get_mes(password, numb)
        if SMS != SMS_LAST: break
        time.sleep(1)
    web_driver.find_elements(By.TAG_NAME, 'input')[0].send_keys(SMS)
    web_driver.find_elements(By.TAG_NAME, 'input')[1].click()

