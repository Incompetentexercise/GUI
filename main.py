import tkinter as tk

fonts = {
    "heading": ("Arial", "16", "bold")
}


class Converter:
    def __init__(self, parent):
        self.root = parent # parent should be an instance of tk.Tk()
        # Divide the window up into three sections to make layout easier
        self.input_frame = tk.Frame(self.root)
        self.input_frame.grid(row=10, column=10)
        self.center_frame = tk.Frame(self.root, padx=10, pady=10)
        self.center_frame.grid(row=10, column=20)
        self.output_frame = tk.Frame(self.root)
        self.output_frame.grid(row=10, column=30)

        self.help_button = tk.Button(
            self.center_frame,
            text="help",
            padx=10, pady=10,
            command=self.open_help
        )
        self.help_button.grid(row=40, column=10)

    def open_help(self):
        self.help_button.config(state=tk.DISABLED)
        help_window = Help(self)


class Help:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(master=self.parent.root)
        self.root.protocol('WM_DELETE_WINDOW', self.close)

    def close(self):
        self.parent.help_button.config(state=tk.NORMAL)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Temperature converter")
    root.geometry("600x350")
    main = Converter(root)
    root.mainloop()
