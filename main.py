import tkinter as tk
import tkinter.ttk as ttk

fonts = {
    "heading": ("Arial", "14", "bold"),
    "body": ('Arial', '10'),
    "button": ('Arial', '12', 'bold')
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


class Converter:
    def __init__(self, parent):
        self.unit = None
        self.input_temp = None
        self.C_out = 0
        self.F_out = 0
        self.K_out = 0

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
        self.error_label.grid(row=10, column=10)

        self.help_button = tk.Button(
            self.center_frame,
            command=self.open_help,
            text="Help",
            font=fonts['button'],
            relief="groove",
            padx=10, pady=10
        )
        self.help_button.grid(row=40, column=10)

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

    def open_help(self):
        self.help_button.config(state=tk.DISABLED)
        help_window = Help(self)

    def do_conversion(self, *args):
        self.unit = self.input_unit.get()

        try:
            self.float_input = float(self.input_temp.get())
            self.error_message.set('')

            if self.unit == 'c':
                self.C_out = self.float_input
                self.F_out = (self.float_input * 9 / 5) + 32
                self.K_out = self.float_input + 273.15

            elif self.unit == 'f':
                self.C_out = (self.float_input - 32) * 5/9
                self.F_out = self.float_input
                self.K_out = ((self.float_input - 32) * 5/9) + 273.15

            elif self.unit == 'k':
                self.C_out = self.float_input - 273.15
                self.F_out = ((self.float_input - 273.15) * 9/5) + 32
                self.K_out = self.float_input

        except ValueError:
            self.error_message.set('Invalid input')

        self.C_out_entry.delete(0, 'end')
        self.C_out_entry.insert(0, str(self.C_out))

        self.F_out_entry.delete(0, 'end')
        self.F_out_entry.insert(0, str(self.F_out))

        self.K_out_entry.delete(0, 'end')
        self.K_out_entry.insert(0, str(self.K_out))


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
