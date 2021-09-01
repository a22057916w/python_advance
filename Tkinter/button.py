import tkinter as tk

window = tk.Tk()
window.title("countdown")
window.geometry("600x800")

# pack() 先宣告先顯示, 由上而下, 由左自右
btStop = tk.Button(window, text="stop", width=25, command=window.destroy)
btStop.pack()

btDoNothing = tk.Button(window, text="Do Nothing", width=25, command=None)
btDoNothing.pack()

window.mainloop()
