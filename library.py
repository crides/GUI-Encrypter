#!/usr/bin/python3

from time import time
from importlib import import_module
import os, sys
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Notify", "0.7")
from gi.repository import Gtk, Gdk, Notify

prog_ico_name = "emblem-readonly"

def find_methods():
    modules = {}
    for file in filter(lambda a: a.endswith(".py"), os.listdir("methods")):
        module_name = file[:-3]
        modules.update( \
                {module_name: import_module('methods.' + module_name)})
    return modules

def event_esc_exit(window, event):
    if event.keyval == Gdk.keyval_from_name("Escape"): window.destroy()

def clipbd_cb(button, self, action):
    clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    if action == "copy": self.text_buf.copy_clipboard(clip)
    elif action == "cut": self.text_buf.cut_clipboard(clip, True)
    elif action == "paste": self.text_buf.paste_clipboard(clip, None, True)
    elif action == "auto_copy":
        clip.set_text(self.text_buf.get_text(*self.text_buf.get_bounds(), True), -1)
        show_notification("String copied into clipboard.")

def selectall(botton, self):
    self.text_buf.select_range(*win.text_buf.get_bounds())

def showhelp(button, win, res):
    helpwin = Gtk.Window()
    helpwin.set_transient_for(win)
    helpwin.set_title(res.menu_help)
    helpwin.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
    helpwin.set_destroy_with_parent(True)
    helpwin.set_border_width(10)
    helpwin.set_resizable(False)
    helpwin.connect("key_press_event", event_esc_exit)

    helplabel = Gtk.Label(res.help)
    helplabel.set_line_wrap(True)
    helplabel.set_max_width_chars(30)
    helpwin.add(helplabel)
    helpwin.show_all()

def about_program(button, win, res):
    GPL_License = open("LICENSE").read()
    about = Gtk.AboutDialog(win)
    about.set_program_name("GEncrypter")
    about.set_version("5.0")
    about.set_copyright("Copyright © 2012-2014 Jingye Zhang\n" \
                        "Copyright © 2014-2016 Haoqing Zhu")
    about.set_comments(res.abt_comment)
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

def encrypt(button, self, env):
    text = self.text_buf.get_text(*self.text_buf.get_bounds(), True)
    cleartext(None, self, False)
    if text == "" or text == "\n" or text == " ":
        set_text_mono(self.strvarmsg, env.res.msg_err_gen)
    elif "encrypt" not in vars(globals()[env.method]):
        set_text_mono(self.strvarmsg, "No encrypt method in module.")
    else:
        ### Setting Analysis ###
        extra_args = []
        if globals()[env.method].accept_set: extra_args.append(env)
        if len(globals()[env.method].extra) != 0:
            extra_args.append(env.extra)

        start_time = time() * 1000
        ect_str = globals()[env.method].encrypt(text, *extra_args)
        need_time = time() * 1000 - start_time
        dct_str, _ = globals()[env.method].decrypt(ect_str, *extra_args)
        ### Verification ###
        if dct_str != text:
            set_text_mono(self.strvarstat, env.res.msg_stat_enc[0])
        else:
            set_text_mono(self.strvarstat, env.res.msg_stat_enc[1])
            set_text_mono(self.strvartimeused, env.res.time_encryption % need_time)
            self.text_buf.set_text(ect_str)
            clipbd_cb(None, self, "auto_copy")

def decrypt(button, self, env):
    ect_str = self.text_buf.get_text(*self.text_buf.get_bounds(), True)
    cleartext(None, self, False)
    if ect_str == "" or ect_str == "\n" or ect_str == " ":
        set_text_mono(self.strvarmsg, env.res.msg_err_gen)
    elif "decrypt" not in vars(globals()[env.method]):
        set_text_mono(self.strvarmsg, "No decrypt method in module.")
    else:
        ### Setting Analysis ###
        extra_args = []
        if globals()[env.method].accept_set: extra_args.append(env)
        if len(globals()[env.method].extra) != 0:
            extra_args.append(env.extra)

        start_time = time() * 1000
        text = globals()[env.method].decrypt(ect_str, *extra_args)
        need_time = time() * 1000 - start_time
        if type(text) == tuple and len(text) == 2:
            dct_str, date = text
            self.text_buf.set_text(dct_str)
            set_text_mono(self.strvarstat, env.res.msg_stat_dec[1])
            set_text_mono(self.strvarmsg, env.res.time_encrypted + date)
            set_text_mono(self.strvartimeused, str(need_time) + env.res.time_encryption)
            clipbd_cb(None, self, "auto_copy")
        else:
            set_text_mono(self.strvarstat, env.res.msg_stat_dec[0])

def cleartext(button, self, with_textbox):
    self.strvarstat.set_text("")
    self.strvarmsg.set_text("")
    self.strvartimeused.set_text("")
    if with_textbox: self.text_buf.set_text("")

def about(button, self, res):
    cleartext(None, self, True)
    self.text_buf.set_text(res.about)

class default():
    lang = "en_US"
    encode = "ASCII"
    method = "method_zhang"
    extra = {}
