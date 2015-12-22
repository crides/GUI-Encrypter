#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
### GUI Encrypter by Zhu Haoqing(Originally Zhangjingye) ###
### Rev: 3.0
### Runtime Environment: Python3
### Hexage Mode added

#   FUNCTIONS

#   cleartext       Clear Text and Info in Window
#   encrypt         General Decryption Function (Button Encrypt)
#   decrypt         General Decryption Function (Button Decrypt)
#   ABOUT           Docstring of About
#   about           Show About
#   Quit            Quit the Program (Keyboard Escape)
#   selectall       Edit menu -> selectall
#   showhelp        Help menu -> Help
#   Settings        Apply the Settings at Start, Show Preference Dialog, and Apply the Settings when Complete

import Lang
import Library
from Library import *

import tkinter
import tkinter.font
import time
from math import floor
from tkinter import ttk

def cleartext():
    TextStatus.set('')
    Message.set('')
    TimeUsed.set('')
    TextBox.delete('1.0', 'end')

def encrypt(*args):
    Text = TextBox.get('1.0', 'end')[:-1]
    if Text == ''\
    or Text == '\n'\
    or Text == ' ':
        cleartext()
        Message.set(liblang.Msg_ERR)
    else:
        ectstr = encrypter(Text, omode)
        code = ectstr[0]
        needtime = ectstr[1]
        dctstr = decrypter(code, True)
        if dctstr != Text:
            cleartext()
            TextStatus.set(liblang.Msg_Stat_Enc[0])
        else:
            if omode == 'Hex':
                code = hexencrypter(code)
            cleartext()
            TextStatus.set(liblang.Msg_Stat_Enc[1])
            TimeUsed.set(str(needtime) + liblang.Time_Encryption)
            TextBox.insert('1.0', code)

def decrypt(*args):
    Code = TextBox.get('1.0', 'end')
    if Code == ''\
    or Code == '\n'\
    or Code == ' '\
    or Code[0] != '~':
        cleartext()
        Message.set(liblang.Msg_ERR)
    else:
        flag = Code.split('!')[0][-1]
        print('FLAG::', flag)
        if flag == 'h':
            midCode = hexdecrypter(Code)
            print('midCode::', midCode)
            Text = decrypter(midCode, False)
        else:
            Text = decrypter(Code, False)
        if type(Text) == type(('2',)):
            cleartext()
            TextBox.insert('1.0', Text[0])
            TextStatus.set(liblang.Msg_Stat_Dec[1])
            Message.set(liblang.Time_Encrypted + Text[1])
            TimeUsed.set(str(Text[2]) + liblang.Time_Encryption) 
        else:
            cleartext()
            TextStatus.set(liblang.Msg_Stat_Dec[0])

def about(*args):
    cleartext()
    TextBox.insert('1.0', liblang.ABOUT.__doc__)
    
def Quit(*args):
    win.destroy()
    option.destroy()
    root.destroy()

def selectall():
    TextBox.tag_add("sel", "1.0", "end-1c")
    TextBox.mark_set("insert", "1.0")
    TextBox.see("insert")

def showhelp(*args):
    win = tkinter.Toplevel(root)
    win.title(liblang.Menu_Help)
    win.resizable(False, False)

    helpframe = ttk.Frame(win, padding='3 3 12 12')
    helpframe.grid(column=0, row=0)
    global helptext
    helptext = tkinter.StringVar()
    y = (win.winfo_screenheight() - 25)/2 - 50
    x = (win.winfo_screenwidth() - 65)/2 - 140
    win.geometry("275x100+%d+%d" % (x, y))
    ttk.Label(helpframe, width=35, textvariable=helptext, font=ubuntu, wrap=260).grid(column=0, row=0, rowspan=5, sticky='NSWE')
    helptext.set(liblang.HELP.__doc__)

class Settings():

    def __init__(self):
        try:
            file = open('options')
            lines = file.read()
            line = lines.splitlines()
            settings = {}
            for i in line:
                j = i.split('=')
                settings[j[0]] = j[1]
            file.close()
            
            global olang, omode
            olang = settings.get('Language')
            omode = settings.get('Mode')
            
            global liblang
            if olang == 'en_US':
                from Lang import en_US as liblang
            else:
                from Lang import zh_CN as liblang
                
        except:
            file = open('options', 'w')
            lang = 'Language' + '=' + Default.lang
            mode = 'Mode' + '=' + Default.mode
            file.write('\n'.join((lang, mode)))
            file.close()
            del lang, mode
            
            global olang, omode
            olang = 'en_US'
            omode = 'Normal'

    def SettingDialog():
        option = tkinter.Toplevel(root)
        option.title(liblang.Menu_Edit_[4])
        option.resizable(False, False)

        y = (option.winfo_screenheight() - 25)/2 - 100
        x = (option.winfo_screenwidth() - 65)/2 - 120
        option.geometry("235x205+%d+%d" % (x, y))
        
        optionframe = ttk.Frame(option, padding='3 3 12 12')
        optionframe.grid(column=0, row=0)

        global chosen1, chosen2
        chosen1 = tkinter.StringVar()
        chosen2 = tkinter.StringVar()
        
        langframe = tkinter.LabelFrame(optionframe, text=liblang.Lbl_set_Label[0], font=ubuntu)
        langframe.grid(column=0, row=1, columnspan=2, sticky='NSWE')
        eng = tkinter.Radiobutton(langframe, text='English', font=ubuntu, variable=chosen1, value='en_US')
        eng.grid(column=1, row=2, sticky='WN')
        chn = tkinter.Radiobutton(langframe, text='中文', font=ubuntu, variable=chosen1, value='zh_CN')
        chn.grid(column=2, row=2, sticky='WN')
        tkinter.Label(langframe, text=liblang.set_Note, font=ubuntus, wrap=220, anchor='w', justify='left').grid(column=1, row=3, columnspan=2, sticky='WN')

        modeframe = tkinter.LabelFrame(optionframe, text=liblang.Lbl_set_Label[1], font=ubuntu)
        modeframe.grid(column=0, row=2, columnspan=2, sticky='NSWE')
        nrm = tkinter.Radiobutton(modeframe, text=liblang.Lbl_set_Label[2], font=ubuntu, variable=chosen2, value='Normal')
        nrm.grid(column=1, row=4, sticky='WN')
        hexmode = tkinter.Radiobutton(modeframe, text=liblang.Lbl_set_Label[3], font=ubuntu, variable=chosen2, value='Hex')
        hexmode.grid(column=2, row=4, sticky='EN')

        if olang == 'en_US':eng.select()
        else:chn.select()
        if omode == 'Normal':nrm.select()
        else:hexmode.select()
        
        tkinter.Label(optionframe).grid(column=0, row=3)
        tkinter.Button(optionframe, text=liblang.Lbl_set_Btn[0], font=ubuntus, command=Settings.applyset).grid(column=0, row=4, sticky='WS')
        tkinter.Button(optionframe, text=liblang.Lbl_set_Btn[1], font=ubuntus, command=option.destroy).grid(column=1, row=4, sticky='ES')
        
    def applyset():

        lang = chosen1.get()
        mode = chosen2.get()
        file = open('options', 'w')
        lang = 'Language' + '=' + lang
        mode = 'Mode' + '=' + mode
        file.write('\n'.join((lang, mode)))
        file.close()
        Settings()

Settings()

if omode == 'Hex':
    title_mode = liblang.Lbl_set_Label[3]
else:
    title_mode = liblang.Lbl_set_Label[2]

### Basic Window ###
root = tkinter.Tk()
root.title(liblang.Title + ' - ' + title_mode + ' ' + liblang.Lbl_set_Label[1])
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

edit.entryconfigure(liblang.Menu_Edit_[0], command=lambda: root.event_generate("<Control-c>"))
edit.entryconfigure(liblang.Menu_Edit_[1], command=lambda: root.event_generate("<Control-x>"))
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