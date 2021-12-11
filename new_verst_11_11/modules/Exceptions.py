from modules.Data import Log


class SmsLoadError(Exception, Log):
    def __init__(self, gmail, numb):
        self.write_log('exceptions', 'SmsLoadError', numb)
        self.gmail = gmail
