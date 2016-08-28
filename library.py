#!/usr/bin/python3

from time import time, ctime
from math import floor
from random import random
from importlib import import_module
import os, sys
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Notify", "0.7")
from gi.repository import Gtk, Gdk, Notify

prog_ico_name = "emblem-readonly"

def find_modules():
    modules = []
    for file in filter(lambda a: a.endswith(".py"), os.listdir("methods")):
        module_name = file[:-3]
        modules.append(module_name)
        exec("globals()['{}'] = import_module('methods.{}')" \
                .format(module_name))
    return modules

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

def set_text_mono(label, text):
    label.set_markup("<span font=\"Ubuntu Mono 12\">%s</span>" % text)

def encrypt(button, self, _set, modules):
    text = self.text_buf.get_text(*self.text_buf.get_bounds(), True)
    if text == "" or text == "\n" or text == " ":
        cleartext(None, self, True)
        set_text_mono(self.strvarmsg, _set.liblang.msg_err_gen)
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

def decrypt(button, self, _set, modules):
    un3 = utf_un3 if _set.encode == "UTF-8" else uni_un3
    ect_str = self.text_buf.get_text(*self.text_buf.get_bounds(), True)
    if ect_str == "" or ect_str == "\n"\
    or ect_str == " " or ect_str[0] != "~":
        cleartext(None, self, False)
        set_text_mono(self.strvarmsg, _set.liblang.msg_err_gen)
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
    encoding = "ASCII"
    method = "method_zhang"
    extra = []
