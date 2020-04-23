import tkinter as tk


class Converter:
    def __init__(self, parent):
        self.root = parent
        print("hello world")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Temperature converter")
    main = Converter(root)
    root.mainloop()
