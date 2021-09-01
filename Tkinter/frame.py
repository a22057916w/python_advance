import tkinter as tk

window = tk.Tk()
window.title("Frame with Buttons")
window.geometry("1600x900")

# --------- Frame ----------
frameTop = tk.Frame(window, bg="white")         # frame is pack to window
frameTop.pack()

frameBottom = tk.Frame(window, bg="white")
frameBottom.pack(side = "bottom")

# ---------- Button ------------
btnRed = tk.Button(frameTop, text="Red", fg="red", bg="white")          # botton is pack to frameTop
btnRed.pack(side = "left")

btnGreen = tk.Button(frameTop, text="Green", fg="green", bg="white")
btnGreen.pack(side = "left")

btnBrown = tk.Button(frameTop, text="Brown", fg="brown", bg="white")
btnBrown.pack(side = "left")

btnBlue = tk.Button(frameBottom, text="Blue", fg="blue", bg="white")    # botton is pack to frameBottom
btnBlue.pack(side = "left")

# Notice that: botton is pack to frame, and frame is hook to window

window.mainloop()
