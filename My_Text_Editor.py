import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def new_file():
    text_area.delete("1.0", tk.END)
    root.title("Untitled - Text Editor")

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files","*.txt"), ("All Files","*.*")]
    )
    if file_path:
        with open(file_path, "r") as f:
            content = f.read()
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, content)
        root.title(file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files","*.txt"), ("All Files","*.*")]
    )
    if file_path:
        try:
            content = text_area.get("1.0", tk.END)
            with open(file_path, "w") as f:
                f.write(content)
            root.title(file_path)
        except:
            messagebox.showerror("Error", "Unable to save file")

root = tk.Tk()
root.title("Text Editor")
root.geometry("700x500")

text_area = tk.Text(root, wrap="word", font=("Arial", 12))
text_area.pack(fill="both", expand=True)

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

root.mainloop()

d
