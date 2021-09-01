import tkinter as tk

window = tk.Tk()
window.title("countdown")
window.geometry("600x800")

# pack() 先宣告先顯示, 由上而下, 由左自右
btnStop = tk.Button(window, text="stop", width=25, command=window.destroy)
btnStop.pack()

btnDoNothing = tk.Button(window, text="Do Nothing", width=25, command=None)
btnDoNothing.pack()

window.mainloop()
