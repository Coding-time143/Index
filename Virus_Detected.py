import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import time


SAMPLE_FILES = [
    "C:/Users/Student/Documents/report.docx",
    "C:/Users/Student/Downloads/setup.exe",
    "C:/Users/Student/Pictures/vacation.jpg",
    "C:/Program Files/App/app.exe",
    "C:/Users/Student/Music/song.mp3",
    "D:/Games/game.exe",
    "C:/Temp/tempfile.tmp",
    "C:/Users/Student/Documents/notes.txt",
    "C:/Users/Student/Downloads/invoice.pdf",
    "E:/Shared/installer.msi"
]


INFECTION_CHANCE = 0.25


class VirusScannerSim:
    def __init__(self, root):
        self.root = root
        self.root.title("Virus Scanner — Educational Simulation")
        self.root.geometry("760x420")
        self.root.resizable(False, False)


        self.files_to_scan = SAMPLE_FILES.copy()
        self.scanned = []
        self.infected = []
        self.quarantine = []
        self.log = []
        self.scanning = False
        self.current_index = 0


        self._build_ui()


    def _build_ui(self):
        frame_left = ttk.Frame(self.root, padding=12)
        frame_left.pack(side="left", fill="y")


        ttk.Label(frame_left, text="Files to Scan:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.listbox_files = tk.Listbox(frame_left, width=55, height=15)
        self._refresh_file_listbox()
        self.listbox_files.pack(pady=(4, 12))


        btn_frame = ttk.Frame(frame_left)
        btn_frame.pack(fill="x", pady=(0, 12))


        self.btn_start = ttk.Button(btn_frame, text="Start Scan", command=self.start_scan)
        self.btn_start.pack(side="left", padx=6)
        self.btn_stop = ttk.Button(btn_frame, text="Stop Scan", command=self.stop_scan, state="disabled")
        self.btn_stop.pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Add File...", command=self.add_file).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="View Logs", command=self.view_logs).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="View Quarantine", command=self.view_quarantine).pack(side="left", padx=6)


        frame_right = ttk.Frame(self.root, padding=12)
        frame_right.pack(side="right", fill="both", expand=True)


        ttk.Label(frame_right, text="Scan Progress", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.progress = ttk.Progressbar(frame_right, orient="horizontal", length=360, mode="determinate")
        self.progress.pack(pady=(6, 8))
        self.status_var = tk.StringVar(value="Idle — ready to scan")
        ttk.Label(frame_right, textvariable=self.status_var).pack(anchor="w", pady=(0, 8))


        ttk.Label(frame_right, text="Recent Activity:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.txt_activity = tk.Text(frame_right, width=44, height=14, state="disabled", wrap="word")
        self.txt_activity.pack()


        ttk.Label(self.root, text="Tip: This is a simulation — file operations are NOT real.", foreground="gray").pack(side="bottom", pady=6)


    def _refresh_file_listbox(self):
        self.listbox_files.delete(0, tk.END)
        for f in self.files_to_scan:
            self.listbox_files.insert(tk.END, f)


    def add_file(self):
        new = simpledialog.askstring("Add file", "Enter a file path to add to scan list:", parent=self.root)
        if new:
            self.files_to_scan.append(new.strip())
            self._refresh_file_listbox()
            self._log(f"Added file: {new}")


    def start_scan(self):
        if self.scanning:
            return
        if not self.files_to_scan:
            messagebox.showinfo("No files", "There are no files to scan.")
            return


        if not messagebox.askokcancel("Start Scan", "Start scanning selected files?"):
            return


        self.scanning = True
        self.current_index = 0
        self.scanned.clear()
        self.infected.clear()
        self.progress["maximum"] = len(self.files_to_scan)
        self.progress["value"] = 0
        self._set_ui_state(scanning=True)
        self._log("Scan started.")
        self._scan_next_file()


    def stop_scan(self):
        if not self.scanning:
            return
        if messagebox.askyesno("Stop Scan", "Are you sure you want to stop the scan?"):
            self.scanning = False
            self._set_ui_state(scanning=False)
            self._log("Scan stopped by user.")
            self.status_var.set("Scan stopped.")


    def _set_ui_state(self, scanning):
        if scanning:
            self.btn_start.config(state="disabled")
            self.btn_stop.config(state="normal")
        else:
            self.btn_start.config(state="normal")
            self.btn_stop.config(state="disabled")


    def _scan_next_file(self):
        if not self.scanning:
            return


        if self.current_index >= len(self.files_to_scan):
            self.scanning = False
            self._set_ui_state(scanning=False)
            self.status_var.set("Scan complete.")
            self._log("Scan completed.")
            summary = f"Scan finished. {len(self.infected)} infected file(s) found."
            messagebox.showinfo("Scan Complete", summary)
            return


        filename = self.files_to_scan[self.current_index]
        self.status_var.set(f"Scanning: {filename}")
        self._append_activity(f"Scanning: {filename}")
        infected_here = random.random() < INFECTION_CHANCE


        self.root.after(700, lambda: self._scan_result(filename, infected_here))


    def _scan_result(self, filename, infected_here):
        self.scanned.append(filename)
        self.current_index += 1
        self.progress["value"] = len(self.scanned)


        if infected_here:
            self.infected.append(filename)
            self._log(f"Infected: {filename}")
            resp = messagebox.askyesno(
                "Threat Detected",
                f"Potential threat found:\n\n{filename}\n\nWould you like to quarantine this file?"
            )
            if resp:
                self._quarantine_file(filename)
            else:
                delete_resp = messagebox.askyesno(
                    "Delete file",
                    "Do you want to delete the file instead of quarantining it?\n(Deleting in the simulation removes it from the list.)"
                )
                if delete_resp:
                    self._delete_file(filename)
                else:
                    self._log(f"User ignored threat for: {filename}")
                    self._append_activity(f"Ignored threat: {filename}")
        else:
            self._log(f"Clean: {filename}")
            self._append_activity(f"Clean: {filename}")


        self.root.after(300, self._scan_next_file)


    def _quarantine_file(self, filename):
        if filename not in self.quarantine:
            self.quarantine.append(filename)
        if filename in self.files_to_scan:
            self.files_to_scan.remove(filename)
        self._refresh_file_listbox()
        self._log(f"Quarantined: {filename}")
        self._append_activity(f"Quarantined: {filename}")
        messagebox.showinfo("Quarantined", f"The file has been moved to quarantine:\n\n{filename}")


    def _delete_file(self, filename):
        if filename in self.files_to_scan:
            self.files_to_scan.remove(filename)
        if filename in self.quarantine:
            self.quarantine.remove(filename)
        self._refresh_file_listbox()
        self._log(f"Deleted: {filename}")
        self._append_activity(f"Deleted: {filename}")
        messagebox.showinfo("Deleted", f"The file was deleted (simulation):\n\n{filename}")


    def view_logs(self):
        if not self.log:
            messagebox.showinfo("Logs", "No logs available yet.")
            return
        text = "\n".join(self.log[-50:])
        top = tk.Toplevel(self.root)
        top.title("Scanner Logs")
        top.geometry("640x360")
        txt = tk.Text(top, wrap="word")
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", text)
        txt.config(state="disabled")
        ttk.Button(top, text="Close", command=top.destroy).pack(pady=6)


    def view_quarantine(self):
        if not self.quarantine:
            messagebox.showinfo("Quarantine", "No files are in quarantine.")
            return
        top = tk.Toplevel(self.root)
        top.title("Quarantine")
        top.geometry("520x320")
        lb = tk.Listbox(top, width=80, height=12)
        for f in self.quarantine:
            lb.insert(tk.END, f)
        lb.pack(pady=(8, 6))
        btns = ttk.Frame(top)
        btns.pack()
        def restore():
            sel = lb.curselection()
            if not sel:
                messagebox.showinfo("Select", "Select a file to restore.")
                return
            file_to_restore = lb.get(sel[0])
            if messagebox.askyesno("Restore", f"Restore {file_to_restore} to scan list?"):
                self.quarantine.remove(file_to_restore)
                self.files_to_scan.append(file_to_restore)
                self._refresh_file_listbox()
                lb.delete(sel[0])
                self._log(f"Restored from quarantine: {file_to_restore}")
        def remove_file():
            sel = lb.curselection()
            if not sel:
                messagebox.showinfo("Select", "Select a file to permanently delete.")
                return
            file_to_remove = lb.get(sel[0])
            if messagebox.askyesno("Permanently Delete", f"Permanently delete {file_to_remove}?"):
                self.quarantine.remove(file_to_remove)
                lb.delete(sel[0])
                self._log(f"Permanently deleted from quarantine: {file_to_remove}")


        ttk.Button(btns, text="Restore", command=restore).pack(side="left", padx=6)
        ttk.Button(btns, text="Permanently Delete", command=remove_file).pack(side="left", padx=6)
        ttk.Button(btns, text="Close", command=top.destroy).pack(side="left", padx=6)


    def _log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.log.append(entry)


    def _append_activity(self, message):
        self.txt_activity.config(state="normal")
        self.txt_activity.insert("end", message + "\n")
        self.txt_activity.see("end")
        self.txt_activity.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = VirusScannerSim(root)
    root.mainloop()
