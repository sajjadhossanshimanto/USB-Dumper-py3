# -*- coding: utf-8 -*-
import base64
import os
import random
import time
import shutil
import stat
import tkinter as tk
from tkinter import filedialog
from icon import img  # Assuming icon.py contains the base64-encoded icon

USB = 'F:'  # Set to F: disk for testing
SAVE = 'C:/usbCopy'  # Default directory to save
OLD = []
disk_dict = {
    'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0,
    'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
    'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0
}

# Copy USB disk contents
def usb_walker():
    global SAVE
    global USB
    if os.path.exists(SAVE):
        print('Deleting existing directory!')
        try:
            os.chmod(SAVE, stat.S_IREAD | stat.S_IWRITE)
            shutil.rmtree(SAVE)
        except Exception as e:
            print(f"Error: {e}")
            SAVE = SAVE + 'NewFile' + str(random.random() * 10)

    print(f'Destination Directory: {SAVE}')
    print('Copying...')

    shutil.copytree(USB, SAVE)  # Native Python to copy files

# Determine whether the content of the USB disk has changed
def get_usb():
    global OLD
    NEW = os.listdir(USB)
    if len(NEW) == len(OLD):
        print("USB content has not changed")
        return 0
    else:
        OLD = NEW
        return 1

# Check if the USB drive exists
def usb_copy():
    global USB
    for i in range(26):
        name = chr(i + ord('A')) + ':'
        print(name)
        if os.path.exists(name):
            disk_dict[chr(i + ord('A'))] = 1
            print(f'Disk exists: {chr(i + ord("A"))}')

    while True:
        for i in range(26):
            name = chr(i + ord('A')) + ':'
            if not os.path.exists(name):
                disk_dict[chr(i + ord('A'))] = 0
            if os.path.exists(name) and disk_dict[chr(i + ord('A'))] == 0:
                USB = name
                print("USB detected")
                if get_usb():
                    try:
                        usb_walker()
                    except Exception as e:
                        print(f"Error: {e}")

        print("No USB detected, entering sleep mode")
        time.sleep(1)  # Sleep duration
        print("Sleep ended")

def choose_dir():
    global SAVE
    SAVE = filedialog.askdirectory(parent=root, initialdir="/", title='Pick a directory') + '/usbCopy'
    print(f'Save in: {SAVE}')

def click_button():
    root.withdraw()
    usb_copy()

if __name__ == '__main__':
    root = tk.Tk()
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    root.iconbitmap("tmp.ico")
    root.title('USB Dumper')
    root.geometry('700x400')
    tk.Label(
        root,
        text='\n\nYou can use this application to automatically copy \nthe files and folders from the USB '
             'that is connected to your computer\n Default file path:   C:\\usbCopy\n\nSolemnly swear that you are up to no good\n'
    ).pack()
    tk.Label(root, text='Bug report:\ngithub.com/Ginray/USB-Dumper/issues\n\n').pack()
    tk.Button(root, text='Change Save Directory', command=choose_dir).pack()
    tk.Button(root, text='Start USB Dumper', command=click_button).pack()
    root.mainloop()
