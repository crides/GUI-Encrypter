#!/usr/bin/python3
#   FUNCTIONS

#   scale           Change Scale for the Number
#   count           Count Numbers of Items in Iterables
#   encrypter       Encrypt the String and Output
#   decrypter       Decrypt the String and Output
#   hexencrypter    For Encryption of Hexage Mode
#   hexdecrypter    For Decryption of Hexage Mode
#   uni_uc3             Intermediate Encryption Funtion
#   uni_un3             Intermediate Decryption Funtion

from time import time, ctime
from math import floor
from random import random
import os, sys
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Notify", "0.7")
from gi.repository import Gtk, Gdk, Notify

prog_ico_name = "emblem-readonly"

def event_esc_exit(window, event, liblang):
    if event.keyval == Gdk.keyval_from_name("Escape"):
        window.destroy()
        if liblang.title in window.get_title():
            Gtk.main_quit()

def clipbd_cb(self, button, action):
    clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    if action == "copy":
        self.text_buf.copy_clipboard(clip)
    elif action == "cut":
        self.text_buf.cut_clipboard(clip, True)
    elif action == "paste":
        self.text_buf.paste_clipboard(clip, None, True)
    elif action == "auto_copy":
        clip.set_text(self.text_buf.get_text(*self.text_buf.get_bounds(), True), -1)
        show_notification("String copied into clipboard.")

def selectall(botton, win):
    win.text_buf.select_range(*win.text_buf.get_bounds())

def showhelp(button, win, liblang):
    helpwin = Gtk.Window()
    helpwin.set_transient_for(win)
    helpwin.set_title(liblang.menu_help)
    helpwin.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
    helpwin.set_destroy_with_parent(True)
    helpwin.set_border_width(10)
    helpwin.set_resizable(False)
    helpwin.connect("key_press_event", event_esc_exit, liblang)

    helplabel = Gtk.Label(liblang.help)
    helplabel.set_line_wrap(True)
    helplabel.set_max_width_chars(30)
    helpwin.add(helplabel)
    helpwin.show_all()

def about_program(button, win, liblang):
    GPL_License = open("LICENSE").read()
    about = Gtk.AboutDialog(win)
    about.set_program_name("GEncrypter")
    about.set_version("4.0")
    about.set_copyright("Copyright © 2012-2014 Jingye Zhang\n" \
                        "Copyright © 2014-2016 Haoqing Zhu")
    about.set_comments(liblang.abt_comment)
    about.set_license(GPL_License)
    about.set_wrap_license(True)
    about.set_authors( \
        ["<a href=\"https://github.com/zhangjingye03\">Jingye Zhang</a>", \
        "<a href=\"https://github.com/Irides-Chromium\">Haoqing Zhu</a>"])
    about.set_website("https://github.com/Irides-Chromium/GUI-Encrypter")
    about.set_website_label("Github project repository")
    about.set_logo_icon_name(prog_ico_name)
    about.set_transient_for(win)
    about.run()
    about.destroy()

def show_notification(message):
    Notify.init("GEncrypter")
    Notify.Notification.new("GEncrypter", message, prog_ico_name).show()

def scale(cur, res, num):
# Default Settings
    num = str(num)
    error = False
    defined = positive = True

    # Input
    if cur not in range(2, 37) or res not in range(2, 37): defined = False
    if num.count("-") == 1:
        positive = False
        num = num[1:]
    result = 0
    unit = 1

    if cur != 10:
        for i in num[::-1]:
            value = ord(i)
            if value in range(48, 58): value -= 48
            elif value in range(97, 123): value -= 87
            elif value in range(65, 92): value -= 55
            if value >= cur: error = True
            result += value * unit
            unit *= cur

    # Output
    if res != 10:
        num = int(result or num)
        result = ""
        while num > 0:
            value = num % res
            if value < 10: digit = value + 48
            elif value <= 35: digit = value + 87
            result = chr(digit) + result
            num //= res
    if error: raise Exception("ERROR")
    elif defined:
        if not positive: result = "-" + str(result)
        return result

def encrypter(string, mode, uc3):
    start_time = str(int(time() * 1000))
    part1 = int(start_time[10:13])
    part2 = string
    part3 = round(random() * 100)
    part4 = int(start_time[0:5])
    part5 = round(random() * 10)
    if part5 == 0: part5 = 10
    part6 = int(start_time[5:10])

    ectpart1 = scale(10, 15, str(part1)[::-1])
    ectpart2 = uc3(part2, part1, part4)
    ectpart3 = scale(10, 3, part3)
    ectpart4 = scale(10, 36, part4 + 15 - int(ectpart3))[::-1]
    ectpart5 = scale(10, 9, part5)
    ectpart6 = scale(10, 35, part6 - 15 * part5)[::-1]

    retn = "~" + ectpart1
    retn += "n!" if mode == "Normal" else "h!"
    retn += ectpart2 + "!"
    retn += ",".join((ectpart3, ectpart4, ectpart5, ectpart6))
    time_used = int(time() * 1000) - int(start_time)
    return retn, time_used

def decrypter(code, checksum, un3):
    start_time = int(time() * 1000)
    code = code[1:].split("!")
    if code[0][-1] == "h"\
    or code[0][-1] == "n":
        code[0] = code[0][:-1]

    part2 = code[1]
    part36 = code[2].split(",");

    dctpart1 = int(str(int(code[0], 15))[::-1])
    dctpart3 = int(part36[0], 3)
    dctpart4 = int(part36[1][::-1], 36) - 15 + int(part36[0])
    dctpart5 = int(part36[2])
    dctpart6 = int(part36[3][::-1], 35) + (15 * dctpart5)
    dctpart2 = un3(part2, dctpart1, dctpart4)

    needtime = int(time() * 1000) - start_time
    retn = dctpart2
    if not checksum:
        ecttime = str(dctpart4) + str(dctpart6) + str(dctpart1)
        tc = ctime(float(ecttime[0:10])).split()
        date = " ".join((tc[4], tc[1], tc[2], tc[3]))
        retn = dctpart2, date, needtime
    return retn

def hexencrypter(code):
    code1, stringlist, code3 = code.split("!")
    stringlist = stringlist.split(",")
    hexcode = ""
    for HEX in stringlist:
        hexcode += "@"
        if HEX[0] == "-":
            hexcode += "-"
            HEX = HEX[1:]
        if len(HEX) % 2: HEX = "0" + HEX
        for i in range(0, len(HEX), 2):
            hexcode += chr(int(HEX[i:i+2], 16))
    hexcode = hexcode[1:]
    code1 += "h"
    return "!".join((code1, hexcode, code3))

def hexdecrypter(hcode):
    code1, HEXlist, code3 = hcode.split("!")
    code1 = code1[:-1]
    HEXlist = HEXlist.split("@")
    string = ""
    for HEX in HEXlist:
        string += ","
        if HEX[0] == "-":
            string += "-"
            HEX = HEX[1:]
        for i in HEX: string += hex(ord(i))[2:]
    string = string[1:]
    return "!".join((code1, string, code3))

def uni_uc3(this, utc, it):
    retn = ""
    for i in range(len(this)):
        if i % 2 != 0:
            retn += scale(10, 15, ord(this[i]) + utc - i) + ","
        else:
            retn += scale(10, 12, ord(this[i]) - it + i) + ","
    return retn[0:-1]

def utf_uc3(this, utc, it):
    retn = ""
    this = this.encode()
    for i in range(len(this)):
        if i % 2 != 0:
            retn += scale(10, 15, this[i] + utc - i) + ","
        else:
            retn += scale(10, 12, this[i] - it + i) + ","
    return retn[0:-1]

def uni_un3(this, utc, it):
    retn = ""
    tmmp = this.split(",")
    for i in range(len(tmmp)):
        if i % 2 != 0:
            retn += chr(int(tmmp[i], 15) - utc + i)
        else:
            retn += chr(int(tmmp[i], 12) + it - i)
    return retn

def utf_un3(this, utc, it):
    retn = []
    tmmp = this.split(",")
    for i in range(len(tmmp)):
        if i % 2 != 0:
            retn.append(int(tmmp[i], 15) - utc + i)
        else:
            retn.append(int(tmmp[i], 12) + it - i)
    return bytes(retn).decode()

def set_text_mono(label, text):
    label.set_markup("<span font=\"Ubuntu Mono 12\">%s</span>" % text)

def encrypt(button, self, _set):
    uc3 = utf_uc3 if _set.encode == "UTF-8" else uni_uc3
    un3 = utf_un3 if _set.encode == "UTF-8" else uni_un3
    text = self.text_buf.get_text(*self.text_buf.get_bounds(), True)
    if text == "" or text == "\n" or text == " ":
        cleartext(None, self, True)
        set_text_mono(self.strvarmsg, _set.liblang.msg_err)
    else:
        ect_str, needtime = encrypter(text, _set.mode, uc3)
        dct_str = decrypter(ect_str, True, un3)
        if dct_str != text:
            cleartext(None, self, True)
            set_text_mono(self.strvarstat, _set.liblang.msg_stat_enc[0])
        else:
            if _set.mode == "Hex":
                ect_str = hexencrypter(ect_str)
            cleartext(None, self, True)
            set_text_mono(self.strvarstat, _set.liblang.msg_stat_enc[1])
            set_text_mono(self.strvartimeused, str(needtime) + _set.liblang.time_encryption)
            self.text_buf.set_text(ect_str)
            clipbd_cb(None, "auto_copy", self)

def decrypt(button, self, _set):
    un3 = utf_un3 if _set.encode == "UTF-8" else uni_un3
    ect_str = self.text_buf.get_text(*self.text_buf.get_bounds(), True)
    if ect_str == "" or ect_str == "\n"\
    or ect_str == " " or ect_str[0] != "~":
        cleartext(None, self, False)
        set_text_mono(self.strvarmsg, _set.liblang.msg_err)
    else:
        flag = ect_str.split("!")[0][-1]
        if flag == "h":
            ect_str = hexdecrypter(ect_str)
        text = decrypter(ect_str, False, un3)
        if type(text) == type((2,)):
            cleartext(None, self, True)
            self.text_buf.set_text(text[0])
            set_text_mono(self.strvarstat, _set.liblang.msg_stat_dec[1])
            set_text_mono(self.strvarmsg, _set.liblang.time_encrypted + text[1])
            set_text_mono(self.strvartimeused, str(text[2]) + _set.liblang.time_encryption)
            clipbd_cb(None, "auto_copy", self)
        else:
            cleartext(None, self, True)
            set_text_mono(self.strvarstat, _set.liblang.msg_stat_dec[0])

def cleartext(button, self, with_textbox):
    self.strvarstat.set_text("")
    self.strvarmsg.set_text("")
    self.strvartimeused.set_text("")
    if with_textbox: self.text_buf.set_text("")

def about(button, self, liblang):
    cleartext(None, self, True)
    self.text_buf.set_text(liblang.about)

class default():
    lang = "en_US"
    mode = "Normal"
    encoding = "ASCII"
