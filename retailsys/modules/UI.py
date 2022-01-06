from tkinter import messagebox
from awesometkinter.bidirender import add_bidi_support
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


class CanvasUI:
    class LineButtonUI(Frame):
        def __init__(self, canvas, offset, separators, line, command=None, status=None):
            self.separators = separators
            self.offset = offset
            Frame.__init__(self, canvas)
            self.place(x = 0,
                       y = (height_line + height_line_ots) * self.offset[0] + 85,
                       width = width_block,
                       height = height_line)
            self.offset[0] += 1

            if line is None:
                self.__separator(command)
                return

            Label(self, text = str(line.index), background = "grey90").place(x = 0, y = 0, width = 20)

            btn_settings = Button(self, text = str(line.COUNT_LINES), command = closure(CanvasLineSettings, line))
            btn_settings.place(x = 20, y = 0, width = 20)

            Label(self, text = line.NAME, background = "grey90").place(x = 40, y = 0, width = 40)
            Label(self, text = line.SURNAME, background = "white").place(x = 80, y = 0, width = 50)
            Label(self, text = line.PASSPORT, background = "grey90").place(x = 130, y = 0, width = 60)
            Label(self, text = line.CITY, background = "white").place(x = 190, y = 0, width = 85)
            Label(self, text = line.STREET, background = "grey90").place(x = 275, y = 0, width = 80)

            self.__button = Button(self, text = '▶', fg = 'green', command = command)
            self.__button.place(x = 355, y = 0, width = 20)

            self.change_status(*status)

        def __separator(self, text):
            back_color = "grey90"
            match text:
                case "":
                    self.configure(background = "white")
                    return
                case "run":
                    fg = "#275c5b"
                case "stack":
                    fg = '#694510'
                case "wait":
                    fg = '#028200'
                case _:
                    fg = '#696969'

            text = ' ' * 100 + text + ' ' * 100
            result = ''
            for c in text:
                result += c
                if c == ' ':
                    result += '\u0336'

            Label(self, text = result, background = back_color, justify = CENTER, fg = fg).place(x = 0, y = 0,
                                                                                                 width = width_block)

        def change_status(self, status, *args):
            if status == 'run':
                self.__button.configure(fg = 'red', text = '0')
            elif status == 'in_stack':
                self.__button.configure(fg = 'red', text = str(args[0]))
            else:
                self.__button.configure(fg = 'green', text = '▶')

        def destroy(self):
            while len(self.separators) != 0:
                self.separators.pop(0).destroy()
            self.offset[0] = 0
            Frame.destroy(self)

    def __init__(self, canvas, numb):
        self.canvas = canvas
        self.number_name = numb

        # link with Worker
        self.Error = self.__place_error()
        self.Save = self.__place_save()
        self.Status = self.__place_status()
        self.Settings = self.__place_settings()
        self.Stack = Stack(self.place_line)
        self.offset = [0]
        self.separators = []

    def get_worker_config(self):
        return self.Error, self.Save, self.Status, self.Stack, self.number_name

    def place_line(self, line, *args, **kwargs):
        return self.LineButtonUI(self.canvas, self.offset, self.separators, line, *args, **kwargs)

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
        return Error([label_status_error, btn_error_next, btn_error_repeat, btn_error_cancel], self.number_name)

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
        return Status(status_label, self.number_name)

    def __place_settings(self):
        btn_settings = Button(self.canvas, text = '⚙', fg = 'grey', background = "white")
        btn_settings.place(x = 355, y = 25, width = 20, height = 20)
        return CanvasWorkerSettings(btn_settings, self.number_name)


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
