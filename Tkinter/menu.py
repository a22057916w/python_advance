import tkinter as tk

window = tk.Tk()
window.title("MenuBar")
window.geometry("1600x900")

menuBar = tk.Menu(window)
window.config(menu = menuBar)

menuFile = tk.Menu(menuBar)
menuHelp = tk.Menu(menuBar)

menuBar.add_cascade(label="File", menu=menuFile)
menuBar.add_cascade(label="Help", menu=menuHelp)

menuFile.add_command(label="New")
menuFile.add_command(label="Open...")
menuFile.add_separator()
menuFile.add_command(label="Exit", command=window.quit)

menuHelp.add_command(label="about")

# Notice that: menuBar is hooked to window, menuFile and menuHelp are hooked to menuBar

window.mainloop()
