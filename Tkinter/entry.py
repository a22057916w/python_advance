import tkinter as tk

window = tk.Tk()
window.title("User Input")
window.geometry("1600x900")

# Using grid() to hook to window instead of pack()
tk.Label(window, text="First Name").grid(row=0)
tk.Label(window, text="Last Name").grid(row=1)

# Entry is used for user input
entryFirstName = tk.Entry(window).grid(row=0, column=1)
entryLastName = tk.Entry(window).grid(row=1, column=1)

window.mainloop()
