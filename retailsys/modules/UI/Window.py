from modules.UI.TypesAction import *
from modules.UI.Settings import *
from config import *

# ✅🟢 ▶️ ⚙️ ❌✅  🔴🟢
height_main = 700
width_main = 1515

width_block = 375
width_ots = 5
height_ots_lines = 20

height_line = 20
height_line_ots = 2


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

            self.change_status(status)

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
            match status[0], len(status):
                case 'run', 1:
                    self.__button.configure(fg = 'red', text = '0', command = None)
                case 'in_stack', 2:
                    self.__button.configure(fg = 'red', text = str(status[1]))
                case _, _:
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

    def create_worker_config(self):
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


class Window(Tk):
    def __init__(self):
        super().__init__(screenName = 'retailsys', className = 'retailsys')

    def make_root(self):
        self.geometry('1515x700+300+200')
        self.resizable(width = False, height = False)

        canvas_main = Canvas(self, background = "grey90", width = width_main, height = height_main)
        canvas_main.place(x = 0, y = 0)

        btn_setting = Button(self, text = '⚙', fg = 'grey', background = "white", command = CanvasMainSettings)
        btn_setting.place(x = 0, y = 0, width = 20, height = 20)

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
