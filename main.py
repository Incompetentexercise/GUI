import tkinter as tk
import tkinter.ttk as ttk

fonts = {
    "heading": ("Arial", "14", "bold"),
    "body": ('Arial', '10'),
    "button": ('Arial', '12', 'bold'),
    'list': ('Arial', '10')
}
colors = {
    'green': '#30DD30',
    'grey': '#AAAAAA',
    'frame bg': '#FCFCFC'
}
help_text = "Type in the temperature you want to convert from into the input box, and select it's unit.\n\n" \
            "The converted value will show in the output box.\n\n" \
            "Take care not to enter a temperature below absolute zero.\n\n" \
            "You can press the history button to view past conversions"
decimal_places = 2


class Converter:
    def __init__(self, parent):
        self.unit = None
        self.input_temp = None
        self.C_out = 0
        self.F_out = 0
        self.K_out = 0
        self.float_input = 0
        self.output_string = ""
        self.history_window = 0
        self.help_window = 0
        self.input_valid = None

        self.root = parent # parent should be an instance of tk.Tk()

        # Divide the window up into three sections to make layout easier
        # far left frame for temperature input
        self.input_frame = tk.Frame(
            self.root,
            bg=colors['frame bg'],
            padx=10, pady=10,
            borderwidth=1,
            relief='sunken'
        )
        self.input_frame.grid(row=10, column=10)
        #middle frame for misc stuff
        self.center_frame = tk.Frame(
            self.root,
            padx=10, pady=10
        )
        self.center_frame.grid(row=20, column=10)
        # right frame for temperature output
        self.output_frame = tk.Frame(
            self.root,
            bg=colors['frame bg'],
            padx=10, pady=10,
            borderwidth=1,
            relief='sunken'
        )
        self.output_frame.grid(row=30, column=10)

        #       INPUT SETUP       ~

        self.input_title = tk.Label(
            self.input_frame,
            text="Input",
            font=fonts['heading'],
            bg=colors['frame bg'],
            padx=5
        )
        self.input_title.grid(
            row=5, column=10,
            columnspan=11
        )

        self.input_temp = tk.StringVar()
        self.input_temp.trace_add("write", self.do_conversion)
        self.temp_entry = tk.Entry(
            self.input_frame,
            textvariable=self.input_temp
        )
        self.temp_entry.grid(row=30, column=10)

        self.input_unit = tk.StringVar(None, 'c')
        self.input_unit.trace_add("write", self.do_conversion)

        self.C_radio = tk.Radiobutton(
            self.input_frame,
            text="C\u00B0",
            variable=self.input_unit,
            value='c',
            background=colors['frame bg']
        )
        self.C_radio.grid(row=20, column=20)
        self.F_radio = tk.Radiobutton(
            self.input_frame,
            text="F\u00B0",
            variable=self.input_unit,
            value='f',
            background=colors['frame bg']
        )
        self.F_radio.grid(row=30, column=20)
        self.K_radio = tk.Radiobutton(
            self.input_frame,
            text="K\u00B0",
            variable=self.input_unit,
            value='k',
            background=colors['frame bg']
        )
        self.K_radio.grid(row=40, column=20)

        #      MIDDLE SETUP      ~

        self.error_message = tk.StringVar()
        self.error_label = tk.Label(
            self.center_frame,
            textvariable=self.error_message,
            font=fonts['body'],
            fg='#CC2020'
        )
        self.error_label.grid(row=10, column=10, columnspan=11)

        self.instruction_label = tk.Label(
            self.center_frame,
            text="Input a temperature and it’s unit above, the converted value will be shown below.",
            font=fonts['body'],
            wraplength=180,
            justify=tk.CENTER
        )
        self.instruction_label.grid(row=20, column=10, columnspan=11, pady=3)

        self.history_button = tk.Button(
            self.center_frame,
            command=self.open_history,
            text="History",
            font=fonts['button'],
            relief='groove',
            padx=10, pady=5
        )
        self.history_button.grid(row=40, column=10, padx=10)

        self.help_button = tk.Button(
            self.center_frame,
            command=self.open_help,
            text="Help",
            font=fonts['button'],
            relief="groove",
            padx=10, pady=5
        )
        self.help_button.grid(row=40, column=20, padx=10)

        #      OUTPUT SETUP      ~

        self.output_label = tk.Label(
            self.output_frame,
            text='Output',
            font=fonts['heading'],
            bg=colors['frame bg']
        )
        self.output_label.grid(row=5, column=10, columnspan=11)

        self.C_out_label = tk.Label(
            self.output_frame,
            text="C\u00B0",
            bg=colors['frame bg']
        )
        self.C_out_label.grid(row=10, column=10)

        self.F_out_label = tk.Label(
            self.output_frame,
            text="F\u00B0",
            bg=colors['frame bg']
        )
        self.F_out_label.grid(row=20, column=10)

        self.K_out_label = tk.Label(
            self.output_frame,
            text="K\u00B0",
            bg=colors['frame bg']
        )
        self.K_out_label.grid(row=30, column=10)

        self.C_out_entry = tk.Entry(
            self.output_frame,
        )
        self.C_out_entry.grid(row=10, column=20)

        self.F_out_entry = tk.Entry(
            self.output_frame,
        )
        self.F_out_entry.grid(row=20, column=20)

        self.K_out_entry = tk.Entry(
            self.output_frame,
        )
        self.K_out_entry.grid(row=30, column=20)

        self.save_button = tk.Button(
            self.output_frame,
            text='save',
            font=fonts['button'],
            relief="groove",
            padx=10, pady=2,
            command=self.save_conversion
        )
        self.save_button.grid(row=40, column=10, columnspan=11)

        self.do_conversion()

    def open_help(self):
        self.help_button.config(state=tk.DISABLED)
        self.help_window = Help(self)

    def open_history(self):
        self.history_button.config(state=tk.DISABLED)
        self.history_window = History(self)

    def save_conversion(self):
        self.output_string = "{inp}{in_unit}   --->   {C}C    {F}F    {K}K".format(
            inp=str(self.float_input), in_unit=self.unit.upper(),
            C=str(self.C_out), F=str(self.F_out), K=str(self.K_out),
        )
        print(self.output_string)
        with open("history.txt", 'a') as file:
            file.write(self.output_string+"\n")

        if self.history_window:
            self.history_window.refresh_list()

    # convert the inputted value to other units and set the output boxes
    # also does checks to ensure validity
    def do_conversion(self, *args):
        # get an ascii version of the unit from the linked tkinter variable
        self.unit = self.input_unit.get()

        try:
            # try to get the temperature input from the input box and convert to float
            self.float_input = float(self.input_temp.get())
            self.error_message.set('') # float conversion successful, clear errors message

            # do conversions and checks for below absolute zero
            if self.unit == 'c':
                if self.float_input < -273.15:
                    self.error_message.set('Input below absolute zero')
                    self.C_out, self.F_out, self.K_out = '>:(', '>:(', '>:('
                    self.input_valid = False
                else:
                    self.C_out = self.float_input
                    self.F_out = (self.float_input * 9 / 5) + 32
                    self.K_out = self.float_input + 273.15
                    self.input_valid = True

            elif self.unit == 'f':
                if self.float_input < -460:
                    self.error_message.set('Input below absolute zero')
                    self.C_out, self.F_out, self.K_out = ';-(', ';-(', ';-('
                    self.input_valid = False
                else:
                    self.C_out = (self.float_input - 32) * 5/9
                    self.F_out = self.float_input
                    self.K_out = ((self.float_input - 32) * 5/9) + 273.15
                    self.input_valid = True

            elif self.unit == 'k':
                if self.float_input < 0:
                    self.error_message.set('Input below absolute zero')
                    self.C_out, self.F_out, self.K_out = '(ノಠ益ಠ)ノ彡┻━┻', 'ヽ(`Д´)ﾉ︵ ┻━┻', '(╯°□°）╯︵ ┻━┻'
                    self.input_valid = False
                else:
                    self.C_out = self.float_input - 273.15
                    self.F_out = ((self.float_input - 273.15) * 9/5) + 32
                    self.K_out = self.float_input
                    self.input_valid = True

        except ValueError: # float conversion failed
            self.input_valid = False
            # if there is a value in the text box
            if self.input_temp.get() != '':
                # input is present but invalid
                self.error_message.set('Invalid input')
                self.C_out, self.F_out, self.K_out = ':(', ':(', ':('

            else:
                # there is no input
                self.error_message.set('')
                self.C_out, self.F_out, self.K_out = 0, 0, 0

        try:
            # try to round the temperature values to avoid horrible recurring decimals
            self.C_out = round(self.C_out, decimal_places)
            self.F_out = round(self.F_out, decimal_places)
            self.K_out = round(self.K_out, decimal_places)
        except TypeError:
            # for when there is text in the output boxes so rounding doesnt work
            pass

        # set the output boxes to the values in the output variables
        self.C_out_entry.delete(0, 'end') # clear the output box
        self.C_out_entry.insert(0, str(self.C_out)) # insert output value

        self.F_out_entry.delete(0, 'end')
        self.F_out_entry.insert(0, str(self.F_out))

        self.K_out_entry.delete(0, 'end')
        self.K_out_entry.insert(0, str(self.K_out))

        if self.input_valid:
            self.save_button.configure(state=tk.NORMAL)
        else:
            self.save_button.configure(state=tk.DISABLED)


class Help:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(master=self.parent.root)
        self.root.title("Conversion Help")
        self.root.geometry("350x200")
        # bind the window close button to the close function in this class
        # important for enabling the help button
        self.root.protocol('WM_DELETE_WINDOW', self.close)

        self.main_label = tk.Label(
            self.root,
            text=help_text,
            font=fonts["body"],
            padx=10, pady=10,
            wraplength=320,
            justify=tk.LEFT
            )
        self.main_label.grid(row=10, column=10)

    def close(self):
        self.parent.help_button.config(state=tk.NORMAL)
        self.root.destroy()
        self.parent.help_window = 0


class History:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(master=self.parent.root)
        self.root.title("Conversion History")
        # self.root.geometry("290x250")
        # bind the window close button to the close function in this class
        # important for enabling the history button
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.history = [] # holds the history items read from file

        # frame to hold the list of history items and a scrollbar for the list
        self.history_frame = tk.Frame(self.root)
        self.history_frame.grid(row=10, column=10)

        # list of all the previous calculations in history file
        self.history_list = tk.Listbox(
            self.history_frame,
            width=40,
            height=15,
            font=fonts['list']
        )
        self.history_list.pack(side="left", fill="y")

        # scrollbar for when there are a lot of items in history
        self.list_scroll = tk.Scrollbar(self.history_frame,
                                        orient='vertical',
                                        command=self.history_list.yview
                                        )
        self.list_scroll.pack(side='right', fill='y')

        # link history list to scrollbar
        self.history_list.config(yscrollcommand=self.list_scroll.set)

        self.refresh_list()

    def refresh_list(self):
        self.history_list.delete(0, tk.END)

        # read history file and put contents into history list
        with open('history.txt', 'r') as file:
            for line in file:
                self.history.append(line)
        # add all read items to the listbox
        for item in self.history:
            self.history_list.insert(0, item)

    def close(self):
        self.parent.history_button.config(state=tk.NORMAL)
        self.root.destroy()
        # self.parent.history_window = 0


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Temperature converter")
    # root.geometry("600x350")
    main_frame = tk.Frame(
        root,
        pady=20, padx=20
    )
    main_frame.pack()
    main = Converter(main_frame)
    root.mainloop()
