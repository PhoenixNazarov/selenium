from config import *
from modules.exception.Handlers import read_json_error


class Log:
    __path = LOG_PATH
    __base = []
    __check = 0
    __numb = -1

    def __init__(self, numb):
        self.__numb = numb

    def write_log(self, _type, description, numb=-1):
        if self.__numb != -1:
            numb = self.__numb
        if not LOGGING: return
        self.__read()
        self.__base.append({
            'type': _type,
            'description': description,
            'numb': numb,
            'time': round(time.time())
        })
        self.__save()

    @read_json_error(LOG_PATH)
    def __read(self):
        with open(self.__path, 'r') as file:
            self.__base = json.loads(file.read())

    def __save(self):
        with open(self.__path, 'w') as file:
            file.write(json.dumps(self.__base))