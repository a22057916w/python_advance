import tkinter as tk

window = tk.Tk()
window.title("Scale")
window.geometry("1600x900")

# type(tk.Scale()) return <class 'tkinter.Scale'>
scaleDefault = tk.Scale(window, from_=0, to=1000)
scaleDefault.pack()
scaleHorizon = tk.Scale(window, from_=0, to=2000, orient="horizontal")
scaleHorizon.pack()

window.mainloop()
