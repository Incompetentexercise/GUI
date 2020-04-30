import tkinter as tk
import tkinter.ttk as ttk

fonts = {
    "heading": ("Arial", "14", "bold"),
    "body": ('Arial', '10'),
    "button": ('Arial', '12', 'bold')
}
colors = {
    'green': '#30DD30',
    'grey': '#AAAAAA'
}
help_text = "First select a temperature to convert from by clicking one of the unit buttons on the far left.\n\n" \
            "Then input a temperature into the enabled text box.\n\n" \
            "Take care not to enter a temperature below absolute zero.\n\n" \
            "After this, press the convert button to see the converted values."
frame_bg = '#FCFCFC'


class Converter:
    def __init__(self, parent):
        self.input = 'c'

        self.root = parent # parent should be an instance of tk.Tk()

        # Divide the window up into three sections to make layout easier
        # far left frame for temperature input
        self.input_frame = tk.Frame(
            self.root,
            bg=frame_bg,
            padx=15, pady=15,
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
            bg=frame_bg,
            padx=30, pady=30
        )
        self.output_frame.grid(row=30, column=10)

        #input title
        self.input_title = tk.Label(
            self.input_frame,
            text="Input",
            font=fonts['heading'],
            bg=frame_bg,
            padx=5
        )
        self.input_title.grid(
            row=5, column=10,
            columnspan=2
        )

        # input setup
        self.celsius_button = tk.Button(
            self.input_frame,
            text="C\u00B0",
            bg=colors['green'],
            font=fonts['heading'],
            relief='groove'
        )
        self.celsius_button.grid(row=10, column=10)

        self.fahrenheit_button = tk.Button(
            self.input_frame,
            text="F\u00B0",
            bg=colors['grey'],
            font=fonts['heading'],
            relief='groove'
        )
        self.fahrenheit_button.grid(row=20, column=10)

        self.help_button = tk.Button(
            self.center_frame,
            text="Help",
            font=fonts['button'],
            relief="groove",
            padx=10, pady=10
        )
        self.help_button.grid(row=40, column=10)

    def open_help(self):
        self.help_button.config(state=tk.DISABLED)
        help_window = Help(self)


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
