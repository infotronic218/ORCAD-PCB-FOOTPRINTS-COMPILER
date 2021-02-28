import os
import shutil

class Compiler:
    def __init__(self, source_folder, destination_folder):
        self.source_path = os.path.abspath(source_folder)
        self.destination_path = os.path.abspath(destination_folder)

    def copy_file_to_destination(self, file_path,):
        file = os.path.abspath(file_path)
        shutil.copy(file, self.destination_path)

    def scan_folder(self, folder_parent):
        for path_child in os.scandir(folder_parent):
            if os.path.isfile(path_child):
                self.copy_file_to_destination(path_child)
            else:
                print("DIR", path_child)
                self.scan_folder(path_child)

    def compile(self):
        self.scan_folder(self.source_path)
