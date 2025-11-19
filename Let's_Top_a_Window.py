import tkinter as tk
def open_new_window():
    win = tk.Toplevel()
    win.title("New Window")
    win.geometry("200x100")
    tk.Label(win, text="Hello!").pack(pady=20)
root = tk.Tk()
root.title("Main Window")
root.geometry("200x100")
tk.Button(root, text="Open", command=open_new_window).pack(pady=20)
root.mainloop()                                                           