import tkinter as tk
def convert():
    value = float(entry_value.get())
    unit_from = var_from.get()
    unit_to = var_to.get()
    meters = value
    if unit_from == "Kilometer": meters = value * 1000
    elif unit_from == "Centimeter": meters = value / 100
    elif unit_from == "Millimeter": meters = value / 1000
    elif unit_from == "Mile": meters = value * 1609.34
    elif unit_from == "Yard": meters = value * 0.9144
    elif unit_from == "Foot": meters = value * 0.3048
    elif unit_from == "Inch": meters = value * 0.0254
    if unit_to == "Kilometer": result = meters / 1000
    elif unit_to == "Centimeter": result = meters * 100
    elif unit_to == "Millimeter": result = meters * 1000
    elif unit_to == "Mile": result = meters / 1609.34
    elif unit_to == "Yard": result = meters / 0.9144
    elif unit_to == "Foot": result = meters / 0.3048
    elif unit_to == "Inch": result = meters / 0.0254
    else: result = meters
    label_result.config(text=f"Result: {result:.4f} {unit_to}")
root = tk.Tk()
root.title("Length Converter")
root.geometry("350x300")
tk.Label(root, text="Enter Value").pack()
entry_value = tk.Entry(root)
entry_value.pack()
units = ["Meter","Kilometer","Centimeter","Millimeter","Mile","Yard","Foot","Inch"]
tk.Label(root, text="From Unit").pack()
var_from = tk.StringVar(root)
var_from.set("Meter")
tk.OptionMenu(root, var_from, *units).pack()
tk.Label(root, text="To Unit").pack()
var_to = tk.StringVar(root)
var_to.set("Kilometer")
tk.OptionMenu(root, var_to, *units).pack()
tk.Button(root, text="Convert", command=convert).pack(pady=10)
label_result = tk.Label(root, text="Result:")
label_result.pack()
root.mainloop()