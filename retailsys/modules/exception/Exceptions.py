class SmsExceptions(Exception):
    def __init__(self, gmail):
        self.msg = 'Ошибка с получением sms'


class NeedOperateUI(Exception):
    def __init__(self):
        self.msg = f'Произошла ошибка'


class InvalidMail(SmsExceptions):
    def __init__(self, gmail, numb):
        self.msg = f'Неправильные данные для аккаунта: {gmail}'


class NotAllowedMail(SmsExceptions):
    def __init__(self, gmail, numb, url):
        self.url = 'https://support.google.com/mail/accounts/answer/78754'
        self.msg = f'Нет разрешений использовать этот аккаунт: {gmail}' + '\n' + self.url


class SmsLoadError(SmsExceptions):
    def __init__(self, gmail, numb):
        self.msg = f'Не удалось получить сообщения для аккаунта: {gmail}'


class DataLoadError(Exception):
    def __init__(self, desr):
        print('this variable is undefined: ' + desr)


class FinderTooTime(Exception):
    def __init__(self, numb, time):
        self.msg = f'Превышено время ожидания для поиска элемента <{time}'

# <div _ngcontent-xrp-c4="" class="invalid-feedback"><!----><span _ngcontent-xrp-c4="">המספר שהוזן אינו תואם</span></div>


