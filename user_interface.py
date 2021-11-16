import tkinter as tk
import tkinter.messagebox as mb


class Author:
    def __init__(self, first_name = None, last_name = None):
        self.first_name = first_name
        self.last_name = last_name


class AuthorFrame(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master=window, height=100, width=100, bd=1, relief='groove', text="Author Information")
        self.authors = []
        firstname_label = tk.Label(text="First name", master=self)
        firstname_label.grid(row=0, column=0)
        firstname_entry = tk.Entry(master=self, width=35)
        firstname_entry.grid(row=0, column=1)
        lastname_label = tk.Label(text="Last name", master=self)
        lastname_label.grid(row=0, column=3)
        lastname_entry = tk.Entry(master=self, width=35)
        lastname_entry.grid(row=0, column=4)
        add_button = tk.Button(text="Add", master=self, command=self.add_author)
        add_button.grid(row=1, column=0)
        done_button = tk.Button(text="Done", master=self, command=self.done)
        done_button.grid(row=1, column=1)

    def append_authords(self):
        current_row = 1
        for author in self.authors:
            current_row += 1
            firstname_label = tk.Label(text=author.first_name, master=self)
            firstname_label.grid(row=current_row, column=0)
            lastname_label = tk.Label(text=author.last_name, master=self)
            lastname_label.grid(row=current_row, column=1)

    def add_author(self):
        print("add")
        mb.Message("dsdsd")

    def done(self):
        print('done')


# https://realpython.com/python-gui-tkinter/

def add_author_event():
    print("{}".format(firstname_entry.get()))


def done_author_event():
    print("{}".format(firstname_entry.get()))


if __name__ == '__main__':
    window = tk.Tk()

    self = AuthorFrame(window)
    self.pack()

    window.mainloop()