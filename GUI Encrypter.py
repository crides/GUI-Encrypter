#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
### GUI Encrypter by Zhu Haoqing(Originally Zhangjingye) ###
### Rev: 2.0
### Runtime Environment: Python3

#   FUNCTIONS

#   scale           Change Scale for the Number
#   count           Count Numbers of Items in Iterables
#   cleartext       Clear Text and Info in Window
#   reverse         Turn the string around
#   encrypt         General Decryption Function (Button Encrypt)
#   decrypt         General Decryption Function (Button Decrypt)
#   encrypter       Encrypt the String and Output
#   decrypter       Decrypt the String and Output
#   uc3             Intermediate Encryption Funtion
#   un3             Intermediate Decryption Funtion
#   ABOUT           Docstring of About
#   about           Show About
#   Quit            Quit the Program (Keyboard Escape)
#   selectall       Edit menu -> selectall
#   HELP            Doctring of Help
#   showhelp        Help menu -> Help
#   preference      Edit menu -> Preference

import Lang
import Library
from Library import *

import tkinter
import tkinter.font
import time
from math import floor
from random import random
from tkinter import ttk

Settings()

### Basic Window ###
root = tkinter.Tk()
root.title(liblang.Title)
root.resizable(False, False)

y = root.winfo_screenheight()/2 - 250
x = root.winfo_screenwidth()/2 - 235
root.geometry("445x470+%d+%d" % (x, y))

### Frame in Window ###
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0)

### Menu Bar ###
root.tk.call('tk', 'windowingsystem')
root.option_add('*tearOff', False)
menubar = tkinter.Menu(root)

edit = tkinter.Menu(menubar, tearoff=0)
edit.add_command(label=liblang.Menu_Edit_[0])
edit.add_command(label=liblang.Menu_Edit_[1])
edit.add_command(label=liblang.Menu_Edit_[2])
edit.add_command(label=liblang.Menu_Edit_[3])
edit.add_separator()

edit.add_command(label=liblang.Menu_Edit_[4])

edit.entryconfigure(liblang.Menu_Edit_[0], command=lambda: root.event_generate("<Control-x>"))
edit.entryconfigure(liblang.Menu_Edit_[1], command=lambda: root.event_generate("<Control-c>"))
edit.entryconfigure(liblang.Menu_Edit_[2], command=lambda: root.event_generate("<Control-v>"))
edit.entryconfigure(liblang.Menu_Edit_[3], command=selectall)
edit.entryconfigure(liblang.Menu_Edit_[4], command=Settings.SettingDialog)
menubar.add_cascade(label=liblang.Menu_Edit, menu=edit)

Help = tkinter.Menu(menubar, tearoff=0)
Help.add_command(label=liblang.Menu_Help, command=showhelp)
Help.add_command(label=liblang.Lbl_Btn[3], command=about)
menubar.add_cascade(label=liblang.Menu_Help, menu=Help)

root.config(menu=menubar)

### Var Def ###
TimeUsed = tkinter.StringVar()
TextStatus = tkinter.StringVar()
Message = tkinter.StringVar()

### Font ###
ubuntus = tkinter.font.Font(family='Ubuntu', size=10)
ubuntu = tkinter.font.Font(family='Ubuntu', size=12)
uMono = tkinter.font.Font(family='Ubuntu Mono', size=13)

### Text Box ###
TextBox = tkinter.Text(mainframe, height=15, width=40, font=ubuntu, wrap='word')
TextBox.grid(column=1, row=2, columnspan=4, sticky='NSWE')
TextBox.grid_columnconfigure(1, weight=1)
TextBox.grid_rowconfigure(1, weight=1)

# Scroll Bar #
s = ttk.Scrollbar(mainframe, command=TextBox.yview)
s.grid(column=5, row=2, sticky='NS')
TextBox['yscrollcommand'] = s.set

### Button ###
tkinter.Button(mainframe, width=8, text=liblang.Lbl_Btn[0], font=ubuntus, command=encrypt).grid(column=1, row=6, sticky='NWSE')
tkinter.Button(mainframe, width=8, text=liblang.Lbl_Btn[1], font=ubuntus, command=decrypt).grid(column=2, row=6, sticky='NWSE')
tkinter.Button(mainframe, width=8, text=liblang.Lbl_Btn[2], font=ubuntus, command=cleartext).grid(column=3, row=6, sticky='NWSE')
tkinter.Button(mainframe, width=8, text=liblang.Lbl_Btn[3], font=ubuntus, command=about).grid(column=4, row=6, sticky='NWSE')

### Labeling ###
ttk.Label(mainframe, text=liblang.Lbl_Label[0], font=ubuntu).grid(row=1, column=1, sticky='NW')
ttk.Label(mainframe, text=liblang.Lbl_Label[1], font=uMono).grid(column=1, row=3, sticky='SW')
ttk.Label(mainframe, textvariable=TextStatus, font=uMono).grid(column=2, row=3, columnspan=3, sticky='NE')
ttk.Label(mainframe, text=liblang.Lbl_Label[2], font=uMono).grid(column=1, row=4, sticky='SW')
ttk.Label(mainframe, textvariable=Message, font=uMono).grid(column=2, row=4, columnspan=3, sticky='NE')
ttk.Label(mainframe, text=liblang.Lbl_Label[3], font=uMono).grid(column=1, row=5, sticky='NW')
ttk.Label(mainframe, textvariable=TimeUsed, font=uMono).grid(column=3, row=5, columnspan=2, sticky='NE')

### Padding ###
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.bind('<Escape>', Quit)
root.bind('<F1>', showhelp)
TextBox.focus()
root.mainloop()
