import tkinter as tk
from tkinter.ttk import Button, Label, Entry, Frame, Style, Progressbar
from tkinter import filedialog
from tkinter import messagebox

from functools import partial
from compile import Compiler
import threading



class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.destination_entry = None
        self.source_entry = None
        self.progressbar = None
        self.wm_title("Orcad PCB Library Compiler")
        self.geometry("500x250")
        self.configure(bg="#e9e4ed")
        self.resizable(False, False)
        self.center_the_screen()
        try:
            self.iconbitmap("D:\P2020\PYTHON\PCBLIB_COMPILER\images\icon.ico")
        except:
            pass

    def center_the_screen(self):
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.winfo_screenheight() / 2 - window_height / 2)
        self.geometry("+{}+{}".format(position_right, position_down))
        print("Width", window_width, "Height", window_height)

        self.add_main_frame()

        self.add_bottom_frame()

    def close_window(self):
        self.quit()

    def compile_files(self):
        source_folder = self.source_entry.get()
        destination_folder = self.destination_entry.get()
        print(source_folder, destination_folder)
        if str(source_folder).__eq__("") or str(destination_folder).__eq__(""):
            messagebox.showerror(title="Compiling Error", message="Source and destination folders should not be empty!")
        else:
            self.progressbar["mode"] = "indeterminate"
            self.progressbar.start(20)
            def run():
                compiler = Compiler(source_folder=source_folder, destination_folder=destination_folder)
                compiler.compile()
                self.progressbar.stop()
                self.progressbar["mode"]="determinate"
                self.progressbar["value"] =100
                messagebox.showinfo(title="Completed", message="Libraries compiled successfully to one folder!")
            threading.Thread(target=run, daemon=True).start()

    def open_folder_dialog(self, entry, text):
        directory = filedialog.askdirectory()
        entry.delete(0, tk.END)
        entry.insert(0, directory)

    def add_main_frame(self):
        main_frame = Frame(self, borderwidth=1)
        main_frame.pack(fill=tk.BOTH, expand=True)

        source_label = Label(main_frame, text="Libraries parent folder ", anchor="e", justify=tk.LEFT)
        self.source_entry = Entry(main_frame, width=65)
        source_button = Button(main_frame, width=10, text="...")
        source_button.bind("<Button-1>", lambda event: self.open_folder_dialog(self.source_entry, "Destination"))

        destination_label = Label(main_frame, text="Compiled destination folder ")
        self.destination_entry = Entry(main_frame, width=65)
        destination_button = Button(main_frame, width=10, text="...")
        destination_button.bind("<Button-1>", lambda event: self.open_folder_dialog(self.destination_entry,
                                                                                    "Select destination folder"))
        progress_label = Label(main_frame, text="Compilation progress", anchor="e", justify=tk.LEFT)
        self.progressbar = Progressbar(main_frame, orient=tk.HORIZONTAL,value="0", mode="indeterminate", length=400)
        self.progressbar["mode"] = "determinate"

        source_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W, columnspan=2)
        self.source_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=9)
        source_button.grid(row=1, column=10, padx=5, pady=5)

        destination_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W, columnspan=2)
        self.destination_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=9)
        destination_button.grid(row=3, column=10, padx=5, pady=5)

        progress_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W, columnspan=2)
        self.progressbar.grid(row=5, column=0, padx=5, pady=5,sticky=tk.W, columnspan =2)

    def add_bottom_frame(self):
        bottom_frame = Frame(self, borderwidth=1)
        style = Style()
        # style.theme_use("default")
        bottom_frame.style = style
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, expand=True)

        close_button = Button(bottom_frame, text="Close", command=self.close_window)

        close_button.pack(side=tk.RIGHT, padx=5, pady=0)
        compile_button = Button(bottom_frame, text="Compile", command=self.compile_files)
        compile_button.pack(side=tk.RIGHT)


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
