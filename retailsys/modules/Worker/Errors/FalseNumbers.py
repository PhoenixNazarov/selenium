from modules.Worker.selenium.webdriver.common.by import By
from .Base import BaseHtmlException

inv_text = 'פרטי לקוח שהוזנו לא תואמים אנא עדכן ונסה שנית'


class ManyNumberException(BaseHtmlException):
    def check(self):
        if not self.web_driver.have_element(By.CLASS_NAME, "invalid-feedback"):
            return False

        if self.web_driver.find_element(By.CLASS_NAME, "invalid-feedback").text == inv_text:
            return True

        return False

    def __check_exit(self):
        if self.web_driver.have_element(By.TAG_NAME, "client-eligibility"):
            while 1:
                buttons = self.web_driver.find_element(By.TAG_NAME, "button")
                for i in buttons:
                    if i.text == 'חזרה':
                        i.click()

        else:
            return False

    def solve(self):
        written = [self.line.PLANS[0]['number']]
        for val in self.line.PLANS[1:]:
            if val['number'] in written:
                continue
            dialogs = self.web_driver.find_element(By.TAG_NAME, 'client-eligibility')
            dialogs.find_elements(By.TAG_NAME, 'button')[0].click()
            self.web_driver.find_element(By.NAME, 'clientPhoneNumber').send_keys(val['number'])
            self.web_driver.find_element(By.NAME, 'clientLastFourDigits').send_keys(self.line.CARD[-4:])
            dialogs = self.web_driver.find_element(By.TAG_NAME, 'client-eligibility')
            dialogs.find_elements(By.TAG_NAME, 'button')[0].click()

            if not self.check():
                return True
            written.append(val['number'])

        return False
