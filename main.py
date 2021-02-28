import tkinter as tk
from tkinter.ttk import Button,Label,Entry, Frame, Style
from tkinter import filedialog
from functools import partial
from compile import Compiler
from threading import Thread


class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry()

        self.wm_title("Orcad PCB Library Compiler")
        self.geometry("500x250")
        self.configure(bg="#e9e4ed")
        self.resizable(False, False)
        self.center_the_screen()

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
        def run():
            compiler = Compiler(source_folder=source_folder, destination_folder=destination_folder)
            compiler.compile()
        Thread(target=run(),daemon=False).start()

    def open_folder_dialog(self, entry, text):

        directory = filedialog.askdirectory()
        entry.delete(0, tk.END)
        entry.insert(0, directory)


    def add_main_frame(self):
        main_frame = Frame(self,  borderwidth=1)
        main_frame.pack(fill=tk.BOTH, expand=True)

        source_label = Label(main_frame, text="Library source folder :")
        self.source_entry = Entry(main_frame, width=65)
        source_button = Button(main_frame, width=10,text="...")
        source_button.bind("<Button-1>", lambda event : self.open_folder_dialog(self.source_entry,"Destinatom"))

        destination_label = Label(main_frame, text="Compiled folder :")
        self.destination_entry = Entry(main_frame, width=65)
        destination_button = Button(main_frame, width=10, text="...")
        destination_button.bind("<Button-1>", lambda event: self.open_folder_dialog(self.destination_entry, "Select destination folder"))

        source_label.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
        self.source_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=9)
        source_button.grid(row=1, column=10, padx=5, pady=5)

        destination_label.grid(row=2, column=0, padx=5, pady=5, columnspan=4)
        self.destination_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=9)
        destination_button.grid(row=3, column=10, padx=5, pady=5)


    def add_bottom_frame(self):
        self.bottom_frame = Frame(self, borderwidth=1)
        style = Style()
        #style.theme_use("default")
        self.bottom_frame.style = style
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, expand=True)

        self.close_button = Button(self.bottom_frame, text="Close", command=self.close_window)

        self.close_button.pack(side=tk.RIGHT, padx=5, pady=0)
        self.compile_button = Button(self.bottom_frame, text="Compile", command=self.compile_files)
        self.compile_button.pack(side=tk.RIGHT)


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
