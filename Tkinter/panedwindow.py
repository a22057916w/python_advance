import tkinter as tk

panedWindow = tk.PanedWindow()

# 'PanedWindow' object has no attribute 'title'
# panedWindow.title("PanedWindow")

# "expand" 是設定是否隨視窗放大
panedWindow.pack(fill="both", expand=True)

etLeft = tk.Entry(panedWindow, bd = 5)
panedWindow.add(etLeft)

pw_2 = tk.PanedWindow(panedWindow, orient=tk.VERTICAL)
panedWindow.add(pw_2)

scaleTop = tk.Scale(pw_2, orient=tk.HORIZONTAL)
pw_2.add(scaleTop)

# Notice that: scaleTop is hooked to pw_2; pw_2 and etLeft are hooked to panedWindow

panedWindow.mainloop()
