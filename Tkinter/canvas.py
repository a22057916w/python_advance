import tkinter as tk

window = tk.Tk()
window.title("Canvas - create lines")
window.geometry("1600x900")

canvas = tk.Canvas(window, width=600, height=600, bg="white")
canvas.pack()


canvas.create_line(20, 20, 580, 20)                     # (x1, y1, x2, y2)
canvas.create_line(20, 100, 580, 100, dash=(20, 5))     # dash(實線長度, 虛線長度)
canvas.create_line(20, 200, 580, 200, width=5)          # set width
canvas.create_line(20, 300, 580, 300, fill="red")       # set color

window.mainloop()
