from firefly import FireflyBot
from tkinter import *

def run_firefly():
    bot = FireflyBot()
    bot.take_instructions()

def create_window():
    root = Tk()
    button = Button(root, text="Click me", padx=50)
    button.pack()
    root.mainloop()
create_window()



