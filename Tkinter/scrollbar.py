import tkinter as tk

window = tk.Tk()
window.title("Scrollbar")
#window.geometry("1600x900")

scrollbar = tk.Scrollbar(window)

# "fill="y"" means scrollbar should stretch to fill any extra space in the y axis
scrollbar.pack(side="right", fill="y")

# type(scrollbar.set) return <class 'method'>, "yscrollcommand" allows the user
# to scroll vertically
lb = tk.Listbox(window, yscrollcommand = scrollbar.set)

for i in range(100):
    lb.insert(i, "This is line number " + str(i))

# "fill="both"" should stretch to fill any extra space in the x and y axis
lb.pack(side="left", fill="both")

# lb.yview is to make the listbox vertically scrollable
scrollbar.config(command=lb.yview)

window.mainloop()
