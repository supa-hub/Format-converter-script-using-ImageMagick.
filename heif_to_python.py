'''
Copyright (C) 2024  Tomi Bilcu

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''


import os
import glob
import shutil
import subprocess
import threading
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()


result_available = threading.Event()

class convert:
    def __init__(self):
        self.pythonfiles_directory = filedialog.askdirectory()
        
        try:
            converted_pictures_path = os.path.join(self.pythonfiles_directory, "converted_pictures")
            y_file = os.makedirs(converted_pictures_path)
        except Exception:
            # if the converted pictures folder cannot be create in the given (or it already exists), then the code will create the folder in the current directory.
            print("folder to store the converted pictures already exists, so the script will not create another one")
            self.pythonfiles_directory = os.getcwd()



        self.picture_list = []
        self.jpg_picture_list = []
        self.pictures_already_converted = []
        self.jpg_already_converted = []

        
        
        for xx in glob.glob("*.heic"):
            self.picture_list.append(xx)

        for zz in glob.glob("*.jpg"):
            self.jpg_already_converted.append(zz)

        for yy in glob.glob(r"converted_pictures\*.jpg", recursive=True):
            for_yyy = "converted_pictures\{}"
            for_yyy = for_yyy.format("")
            yyy = yy.replace(for_yyy,"")
            #print(yyy)
            self.pictures_already_converted.append(yyy)

        self.length_picture_list = len(self.picture_list)/4
        self.st_length_picture_list = int(round(self.length_picture_list,0))
        self.nd_length_picture_list = int(round(self.length_picture_list,0))
        self.rd_length_picture_list = int(round(self.length_picture_list,0))
        self.th_length_picture_list = int(round(self.length_picture_list,0))


        self.whole_count = self.st_length_picture_list + self.nd_length_picture_list + self.rd_length_picture_list + self.th_length_picture_list

        if self.whole_count != len(self.picture_list):
            self.th_length_picture_list = self.th_length_picture_list + (len(self.picture_list)- self.whole_count)




    def convert_picture(self, count_for_multithreading):
        if count_for_multithreading == 0:
            counting_amount = self.st_length_picture_list
        if count_for_multithreading == 1:
            counting_amount = self.nd_length_picture_list
        if count_for_multithreading == 2:
            counting_amount = self.rd_length_picture_list
        if count_for_multithreading == 3:
            counting_amount = self.th_length_picture_list
            
        for xx_convert_count in range(counting_amount):
            new_name = self.picture_list[xx_convert_count + count_for_multithreading*self.st_length_picture_list]
            picture_name = new_name.replace(" ","")
            os.rename(self.picture_list[xx_convert_count + count_for_multithreading*self.st_length_picture_list], picture_name)
            
            self.filename = self.picture_list[xx_convert_count + count_for_multithreading*self.st_length_picture_list]
            self.filename2 = self.filename.split(".")
            
            try:
                self.filename4 = self.filename2[0].split(" ")
                self.filename5 = str(self.filename4[0]+self.filename4[1])
                self.filename3 = self.filename5 + ".jpg"
            except Exception:
                self.filename3 = self.filename2[0] + ".jpg"

            self.jpg_picture_list.append(self.filename3)


            if self.filename3 in self.pictures_already_converted:
                print(f"\033[93m file already converted: \033[0m {self.filename2[0]}")
                self.jpg_picture_list.remove(self.filename3)
                #result_available.set()
                pass
            elif self.filename3 in self.jpg_already_converted:
                print(f"\033[93m file already converted: \033[0m {self.filename3}")
                #result_available.set()
                pass
            else:
                system_string = r"cd {} & magick convert {} {} & exit"   # the command that will execute the picture converter
                system_format = system_string.format(self.pythonfiles_directory, str(self.filename), self.filename3) # we go into the given file path and convert the pictures.
                #print(system_format_list)
                print(f"file being converted: {self.filename}")
                process = subprocess.Popen(system_format, shell=True)
                process.wait()
        result_available.set()

    def move_picture(self):
        self.string_to_move_picture = "{}\converted_pictures"
        self.string_to_move_picture2 = self.string_to_move_picture.format(self.pythonfiles_directory)  # the directory where the converted pictures will be

        for xx_convert_count in self.jpg_picture_list:
            try:
                #print("juu")
                shutil.move(xx_convert_count, self.string_to_move_picture2)
                
            except Exception:
                print("\033[91m a converted file could not be moved into the target folder, the converted file is in the same folder as the original one \033[0m")
                print(f" \033[91m the file that couldn't be moved: \033[0m {xx_convert_count}")
                

        print(f"\033[92m converted files have been successfully moved to the folder at directory: \033[0m {self.string_to_move_picture2}") 


        

        
convert_picture = convert()
t1 = threading.Thread(target=convert_picture.convert_picture(0))
t2 = threading.Thread(target=convert_picture.convert_picture(1))
t3 = threading.Thread(target=convert_picture.convert_picture(2))
t4 = threading.Thread(target=convert_picture.convert_picture(3))


t1.start()
t2.start()
t3.start()
t4.start()


result_available.wait()
t5 = threading.Thread(target=convert_picture.move_picture())
t5.start()

    





