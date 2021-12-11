from tkinter import messagebox
from tkinter import *

from config import *
from modules.TypesAction import Error, Save, Status, Stack
from modules.Data import SettingsJson, SettingsMain

# ✅🟢 ▶️ ⚙️ ❌✅  🔴🟢

height_main = 700
width_main = 1515

width_block = 375
width_ots = 5
height_ots_lines = 20

height_line = 20
height_line_ots = 2


class CanvasMainSettings:
    def __init__(self, btn_setting):
        self.root = None
        # super().__init__(screenName = 'retailsys1', className = 'Settings')
        self.Settings = SettingsMain()
        self.variables = {}
        btn_setting['command'] = self.open_window

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
        self.root.destroy()

    def open_window(self):
        keys = self.Settings.get_keys()
        self.variables = dict(zip(keys, [''] * len(keys)))
        data = self.Settings.get_data()

        self.root = Tk()
        self.root.resizable(width = False, height = False)

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

        vcmd = (self.root.register(validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        messages_paths = [StringVar(self.root), StringVar(self.root), StringVar(self.root),
                          StringVar(self.root), StringVar(self.root)]
        name = ['Main Sheet', 'Sort Sheet', 'Plans Sheet', 'Settings Account', 'Log']
        self.variables['DIR_MAIN_SHEET'] = messages_paths[0]
        self.variables['DIR_SORT_SHEET'] = messages_paths[1]
        self.variables['DIR_PLANS_SHEET'] = messages_paths[2]
        self.variables['SETTINGS_ACCOUNT_PATH'] = messages_paths[3]
        self.variables['LOG_PATH'] = messages_paths[4]
        # messages_paths[0].set('123123123')
        name_time = ['Delay perc', 'Max time wait']
        messages_paths_time = [StringVar(self.root), StringVar(self.root), StringVar(self.root)]
        self.variables['TIME_DELAY_PERC'] = messages_paths_time[0]
        self.variables['MAX_TIME_WAIT'] = messages_paths_time[1]
        for i in self.variables:
            if self.variables[i] != '':
                self.variables[i].set(data[i])

        type_sleep = StringVar(self.root)
        type_sleep.set(data['TYPE_SLEEP'])
        self.variables['TYPE_SLEEP'] = type_sleep
        logging = IntVar(self.root)
        logging.set(int(data['LOGGING']))
        self.variables['LOGGING'] = logging

        canvas2 = Canvas(self.root, background = "grey90", width = 350, height = 360)
        canvas2.pack(side = "bottom", fill = "both", expand = True)
        up = 30
        label = Label(canvas2, text = 'Paths', background = "grey90")
        label.place(x = 100, y = 5, width = 120)
        for i in range(5):
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


class CanvasLineSettings:
    def __init__(self, line):
        self.line = line
        self.root1 = None
        self.message1 = None
        self.message2 = None
        self.other_messages = [[]] * 3

        self.open_window()

    def save(self):
        self.root1.destroy()
        brt = self.line.count_lines
        for i in range(brt):
            self.MainSheet.set_value("E", self.line.index + i, self.message1.get())
            self.MainSheet.set_value("Z", self.line.index + i, self.message2.get())
            self.MainSheet.set_value("G", self.line.index + i, self.other_messages[0][i].get())
            self.MainSheet.set_value("V", self.line.index + i, self.other_messages[1][i].get())
            self.MainSheet.set_value("AU", self.line.index + i, self.other_messages[2][i].get())
        self.MainSheet.save()

    def open_window(self):
        self.root1 = Tk()
        self.root1.resizable(width = False, height = False)

        canvas2 = Canvas(self.root1, background = "grey90", width = 500, height = 60 + 40 * self.line.COUNT_LINES)
        canvas2.pack(side = "bottom", fill = "both", expand = True)

        self.message1 = StringVar(self.root1)
        self.message2 = StringVar(self.root1)

        message_entry1 = Entry(canvas2, textvariable = self.message1)
        message_entry1.place(x = 5, y = 5, width = 100)
        message_entry1.insert(0, self.line.NAME)
        message_entry2 = Entry(canvas2, textvariable = self.message2)
        message_entry2.place(x = 110, y = 5, width = 100)
        message_entry2.insert(0, self.line.SURNAME)

        lis_v = []
        counter = 1
        while self.MainSheet.get_value('A', counter):
            lis_v.append(self.MainSheet.get_value('A', counter))
            counter += 1

        ii = 0
        for ii in range(self.line.count_lines):
            nums = str(self.line.NUMBERS[ii])
            tar = str(self.line.tarifs[ii])
            check_b = self.MainSheet.get_value('AU', self.line.index + ii)

            mes = StringVar(self.root1)
            message_entry = Entry(canvas2, textvariable = mes)
            message_entry.place(x = 5, y = 30 + 40 * ii, width = 205)
            message_entry.insert(0, nums)

            var = StringVar(self.root1)
            var.set(tar)
            opt = OptionMenu(canvas2, var, *lis_v)
            opt.place(x = 210, y = 30 + 40 * ii, width = 205)

            rad_variable = IntVar(self.root1)
            if check_b == 1:
                rad_variable.set(1)
            r1 = Checkbutton(canvas2, text = '1', variable = rad_variable, onvalue = '1', offvalue = '0')
            r1.place(x = 420, y = 30 + 40 * ii, width = 30)

            self.other_messages[0].append(message_entry)
            self.other_messages[1].append(var)
            self.other_messages[2].append(rad_variable)

        message_button = Button(canvas2, text = "Save",
                                command = lambda: self.save())
        message_button.place(x = 210, y = 30 + 40 * (ii + 1))
        self.root1.mainloop()


class CanvasUI:
    def __init__(self, canvas, numb):
        self.canvas = canvas
        self.numb = numb

        # link with Worker
        self.Error = self.__place_error()
        self.Save = self.__place_save()
        self.Status = self.__place_status()
        self.Settings = self.__place_settings()
        self.destroy = []

    def get_worker_config(self):
        return self.Error, self.Save, self.Status, self.Status, self.numb

    def place_line(self, line, count):
        new_canv = Frame(self.canvas, background = "grey90")
        new_canv.place(x = 0, y = (height_line + height_line_ots) * count + 85, width = width_block,
                       height = height_line)
        self.destroy.append(new_canv)

        lab = Label(new_canv, text = str(count), background = "grey90")
        lab.place(x = 0, y = 0, width = 20)

        btn4 = Button(new_canv, text = str(line.COUNT_LINES))
        btn4.place(x = 20, y = 0, width = 20)

        lab = Label(new_canv, text = line.NAME, background = "grey90")
        lab.place(x = 40, y = 0, width = 40)

        lab = Label(new_canv, text = line.SURNAME, width = 1, background = "white")
        lab.place(x = 80, y = 0, width = 50)

        lab = Label(new_canv, text = line.PASSPORT, width = 1, background = "grey90")
        lab.place(x = 130, y = 0, width = 60)

        lab = Label(new_canv, text = line.CITY, width = 1, background = "white")
        lab.place(x = 190, y = 0, width = 85)

        lab = Label(new_canv, text = line.STREET, width = 1, background = "grey90")
        lab.place(x = 275, y = 0, width = 80)

        button_start = Button(new_canv, text = '▶', fg = 'green')
        button_start.place(x = 355, y = 0, width = 20)
        return button_start

    def remove_lines(self):
        for i in self.destroy:
            i.destroy()

    def __place_error(self):
        label_status_error = Label(self.canvas, text = '🔴', background = "white", fg = 'white')
        label_status_error.place(x = 0, y = 25, width = 20)
        btn_error_next = Button(self.canvas, text = 'next▶', fg = 'green', background = "white", state = DISABLED)
        btn_error_next.place(x = 20, y = 25, width = 60)
        btn_error_repeat = Button(self.canvas, text = 'repeat♻️', fg = '#C5AA00', background = "white",
                                  state = DISABLED)
        btn_error_repeat.place(x = 80, y = 25, width = 60)
        btn_error_cancel = Button(self.canvas, text = 'cancel❌', fg = 'red', background = "white", state = DISABLED)
        btn_error_cancel.place(x = 140, y = 25, width = 60)
        return Error([label_status_error, btn_error_next, btn_error_repeat, btn_error_cancel], self.numb)

    def __place_save(self):
        label_status_end = Label(self.canvas, text = '🔴', background = "white", fg = 'white')
        label_status_end.place(x = 0, y = 50, width = 20)
        btn_end_save = Button(self.canvas, text = 'save', fg = 'green', background = "white", state = DISABLED)
        btn_end_save.place(x = 20, y = 50, width = 60)
        btn_end_next = Button(self.canvas, text = 'next', fg = '#C5AA00', background = "white", state = DISABLED)
        btn_end_next.place(x = 80, y = 50, width = 60)
        return Save([label_status_end, btn_end_save, btn_end_next])

    def __place_status(self):
        status_label = Label(self.canvas, text = 'start', background = "white")
        status_label.place(x = 0, y = 0, width = width_block)
        return Status(status_label, self.numb)

    def __place_settings(self):
        btn_settings = Button(self.canvas, text = '⚙', fg = 'grey', background = "white")
        btn_settings.place(x = 355, y = 25, width = 20, height = 20)
        return CanvasWorkerSettings(btn_settings, self.numb)


class UI(Tk):
    def __init__(self):
        super().__init__(screenName = 'retailsys', className = 'retailsys')

    def make_root(self):
        self.geometry('1515x700+300+200')
        self.resizable(width = False, height = False)

        canvas_main = Canvas(self, background = "grey90", width = width_main, height = height_main)
        canvas_main.place(x = 0, y = 0)

        btn_setting = Button(self, text = '⚙', fg = 'grey', background = "white")
        btn_setting.place(x = 0, y = 0, width = 20, height = 20)
        CanvasMainSettings(btn_setting)

        canvas = []
        for i in range(COUNT_GROUPS):
            main_canv = Frame(canvas_main, background = "white", width = width_block, height = height_main)
            main_canv.place(x = (width_block + width_ots) * i)
            lab = Label(main_canv, text = ' - '.join(SORTED_KEYS[i]), background = "grey90")
            lab.place(x = 0, y = 0, width = 375)

            cur_canvas = Frame(main_canv, background = "white", width = width_block, height = height_main)
            cur_canvas.place(x = 0, y = height_ots_lines)
            canvas.append(CanvasUI(cur_canvas, i))

        return canvas

    def show_UI(self):
        self.mainloop()
