from tkinter import messagebox
from awesometkinter.bidirender import add_bidi_support
from tkinter import *

from config import *
from modules.data.JsonSettings import SettingsJson, SettingsMain


class CanvasMainSettings(Tk):
    def __init__(self):
        super().__init__()
        self.Settings = SettingsMain()
        self.variables = {}

        keys = self.Settings.get_keys()
        self.variables = dict(zip(keys, [''] * len(keys)))
        data = self.Settings.get_data()

        self.resizable(width = False, height = False)

        def validate(action, index, value_if_allowed,
                     prior_value, text, validation_type, trigger_type, widget_name):
            if len(value_if_allowed) == 0:
                return True
            if value_if_allowed:
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False

        vcmd = (self.register(validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        messages_paths = [StringVar(self), StringVar(self), StringVar(self),
                          StringVar(self), StringVar(self), StringVar(self)]
        name = ['Main Sheet', 'Sort Sheet', 'Plans Sheet', "Web Driver", 'Settings Account', 'Log']
        self.variables['PATH_MAIN_SHEET'] = messages_paths[0]
        self.variables['PATH_SORT_SHEET'] = messages_paths[1]
        self.variables['PATH_PLANS_SHEET'] = messages_paths[2]
        self.variables['PATH_WEBDRIVER'] = messages_paths[3]
        self.variables['SETTINGS_ACCOUNT_PATH'] = messages_paths[4]
        self.variables['LOG_PATH'] = messages_paths[5]

        name_time = ['Delay perc', 'Max time wait']
        messages_paths_time = [StringVar(self), StringVar(self), StringVar(self)]
        self.variables['TIME_DELAY_PERC'] = messages_paths_time[0]
        self.variables['MAX_TIME_WAIT'] = messages_paths_time[1]
        for i in self.variables:
            if self.variables[i] != '':
                self.variables[i].set(data[i])

        type_sleep = StringVar(self)
        type_sleep.set(data['TYPE_SLEEP'])
        self.variables['TYPE_SLEEP'] = type_sleep
        logging = IntVar(self)
        logging.set(int(data['LOGGING']))
        self.variables['LOGGING'] = logging

        canvas2 = Canvas(self, background = "grey90", width = 350, height = 400)
        canvas2.pack(side = "bottom", fill = "both", expand = True)
        up = 30
        label = Label(canvas2, text = 'Paths', background = "grey90")
        label.place(x = 100, y = 5, width = 120)
        for i in range(6):
            label = Label(canvas2, text = name[i], background = "grey90")
            label.place(x = 5, y = 5 + 25 * (i + 1), width = 120)
            message_entry = Entry(canvas2, textvariable = messages_paths[i])
            message_entry.place(x = 130, y = 5 + 25 * (i + 1), width = 200)
            up += 25
            # message_entry.insert(0, data[data_keys[i]])
        label = Label(canvas2, text = 'Time', background = "grey90")
        label.place(x = 100, y = up, width = 120)

        for i in range(2):
            label = Label(canvas2, text = name_time[i], background = "grey90")
            label.place(x = 5, y = up + 25, width = 120)
            message_entry = Entry(canvas2, textvariable = messages_paths_time[i], validate = 'all',
                                  validatecommand = vcmd)
            message_entry.place(x = 130, y = up + 25, width = 200)
            up += 25
        up += 25
        label = Label(canvas2, text = 'Type Sleep', background = "grey90")
        label.place(x = 5, y = up, width = 120)
        opt = OptionMenu(canvas2, type_sleep, *('fast', 'last'))
        opt.place(x = 130, y = up, width = 200)
        up += 35

        label = Label(canvas2, text = 'Other', background = "grey90")
        label.place(x = 100, y = up, width = 120)
        up += 25

        label = Label(canvas2, text = 'Logging', background = "grey90")
        label.place(x = 5, y = up, width = 120)
        r1 = Checkbutton(canvas2, variable = logging, onvalue = '1', offvalue = '0', background = "grey90")
        r1.place(x = 130, y = up)

        btn_settings = Button(canvas2, text = 'Save', background = "grey90",
                              command = lambda: self.save())
        btn_settings.place(x = 120, y = up + 50, width = 60, height = 20)

    def save(self):
        paths = []
        data = {}

        # is valid values
        for i in self.variables:
            if self.variables[i].get() == '':
                messagebox.showerror("Ошибка", 'Не должно быть пустых строк\n' + i)
                return
            if 'PATH' in i or "DIR" in i:
                if self.variables[i].get() in paths:
                    messagebox.showerror("Ошибка", 'Не должно быть одинаковых путей\n' + i)
                    return
                else:
                    paths.append(self.variables[i].get())
            data.update({i: self.variables[i].get()})

        self.Settings.save(data)
        self.destroy()


class CanvasWorkerSettings:
    def __init__(self, btn_settings, numb):
        self.Settings = SettingsJson(numb)
        self.root_settings = None
        self.messages = []
        btn_settings['command'] = self.open_window

    def save(self):
        data = {
            'gmail': self.messages[0].get(),
            'password': self.messages[1].get(),
            'user_name': self.messages[2].get(),
            'auto_login': int(self.messages[3].get())
        }
        self.messages = []
        self.Settings.save(data)
        self.root_settings.destroy()

    def open_window(self):
        self.root_settings = Tk()
        self.messages = []
        self.root_settings.resizable(width = False, height = False)

        canvas2 = Canvas(self.root_settings, background = "grey90", width = 300, height = 120)
        canvas2.pack(side = "bottom", fill = "both", expand = True)

        rad_variable = IntVar(self.root_settings)
        self.messages = [StringVar(self.root_settings), StringVar(self.root_settings), StringVar(self.root_settings),
                         rad_variable]

        data = self.Settings.get_data()
        if data['auto_login'] == 1:
            rad_variable.set(1)

        data_keys = ["gmail", "password", "user_name"]
        name = ['mail', 'password', 'id']
        for i in range(3):
            label = Label(canvas2, text = name[i], background = "grey90")
            label.place(x = 5, y = 5 + 25 * i, width = 70)
            message_entry = Entry(canvas2, textvariable = self.messages[i])
            message_entry.place(x = 80, y = 5 + 25 * i, width = 200)
            message_entry.insert(0, data[data_keys[i]])

        label = Label(canvas2, text = 'auto-login', background = "grey90")
        label.place(x = 5, y = 80, width = 70)
        r1 = Checkbutton(canvas2, variable = rad_variable, onvalue = '1', offvalue = '0', background = "grey90")
        r1.place(x = 80, y = 80)

        btn_settings = Button(canvas2, text = 'Save', background = "grey90",
                              command = lambda: self.save())
        btn_settings.place(x = 120, y = 100, width = 60, height = 20)


class CanvasLineSettings(Tk):
    def __init__(self, line):
        name = f'change_line_{line.index}'
        super().__init__(screenName = name, className = name)
        self.resizable(width = False, height = False)

        message2 = StringVar(self)

        canvas = Canvas(self, background = "grey90", width = 500, height = 60 + 40 * line.COUNT_LINES)
        canvas.pack(side = "bottom", fill = "both", expand = True)

        # NAME
        message1 = StringVar(self)
        message_entry1 = Entry(canvas, textvariable = message1)
        add_bidi_support(message_entry1)
        message_entry1.place(x = 5, y = 5, width = 100)
        message_entry1.insert(0, line.NAME)

        # SURNAME
        message2 = StringVar(self)
        message_entry2 = Entry(canvas, textvariable = message2)
        add_bidi_support(message_entry2)
        message_entry2.place(x = 110, y = 5, width = 100)
        message_entry2.insert(0, line.SURNAME)

        ii = 0
        other_messages = [[], []]
        for ii in range(line.COUNT_LINES):
            mes = StringVar(self)
            message_entry = Entry(canvas, textvariable = mes)
            add_bidi_support(message_entry)
            message_entry.place(x = 5, y = 30 + 40 * ii, width = 205)
            message_entry.insert(0, line.PLANS[ii]['number'])

            var = StringVar(self)
            var.set(line.PLANS[ii]['name'])
            opt = OptionMenu(canvas, var, *[i[0] for i in line.plans])
            opt.place(x = 210, y = 30 + 40 * ii, width = 205)

            other_messages[0].append(mes)
            other_messages[1].append(var)

        def save():
            self.destroy()
            line.change_data("NAME", message1.get())
            line.change_data("SURNAME", message2.get())
            line.change_data("PLANS_name", [i.get() for i in other_messages[0]])
            line.change_data("PLANS_number", [i.get() for i in other_messages[1]])

        message_button = Button(canvas, text = "Save", command = save)
        message_button.place(x = 210, y = 30 + 40 * (ii + 1))

        self.mainloop()