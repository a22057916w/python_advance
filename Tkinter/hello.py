import tkinter as tk

# 定義一個視窗 名叫 window
window = tk.Tk()

# 設定標題
window.title("whisky")

# 設定像素大小
window.geometry("600x800")

# 設定背景顏色
window.configure(bg = "white")

# 宣告一個標籤
label_1 = tk.Label(window, text="Hello world", bg="yellow", fg="#263238", font=("Arial", 12))

# 設定放置的位置 ( 使用 grid 佈局 )
label_1.grid(column=0, row=0)

# 主視窗迴圈顯示
window.mainloop()
