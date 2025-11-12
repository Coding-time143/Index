import tkinter as tk
from datetime import datetime
def calculate_age():
    try:
        day = int(entry_day.get())
        month = int(entry_month.get())
        year = int(entry_year.get())
        dob = datetime(year, month, day)
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        result_label.config(text=f"Your Age: {age} years")
    except:
        result_label.config(text="Invalid Date")
root = tk.Tk()
root.title("Age Calculator")
root.geometry("300x250")
tk.Label(root, text="Enter Date of Birth").pack(pady=10)
tk.Label(root, text="Day").pack()
entry_day = tk.Entry(root)
entry_day.pack()
tk.Label(root, text="Month").pack()
entry_month = tk.Entry(root)
entry_month.pack()
tk.Label(root, text="Year").pack()
entry_year = tk.Entry(root)
entry_year.pack()
btn = tk.Button(root, text="Calculate Age", command=calculate_age)
btn.pack(pady=15)
result_label = tk.Label(root, text="")
result_label.pack()
root.mainloop()

