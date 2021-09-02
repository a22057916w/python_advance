import tkinter as tk

window = tk.Tk()
window.title("Listbox")
#window.geometry("1600x900")

lb = tk.Listbox(window)
lb.pack()

lb.insert(1, "Mercedes")
lb.insert(2, "RED BULL")
lb.insert(3, "Ferrari")
lb.insert(4, "The rest of best")

window.mainloop()
