#!/usr/bin/python3

# -*- coding: utf-8 -*-
### GUI Encrypter by Zhu Haoqing(Originally Zhang Jingye) ###
### Rev: 4.0
### Runtime Environment: Python3
### Hexage Mode added
### Auto Copy after process added
### Time bugs fixed

import lang
from library import *
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Notify", "0.7")

from gi.repository import Gtk, Gdk, Notify

class Settings():

    set_stat = False

    def __init__(self):
        try:
            file = open("options").read()
            if file == "": raise IOError
            lines = file.splitlines()
            settings = {}
            for line in lines:
                data = line.split("=")
                settings[data[0]] = data[1]
            lang = settings.get("Language")
            mode = settings.get("Mode")
            encode = settings.get("Encoding")

            if lang == "en_US":
                from lang import en_US as liblang
            else:
                from lang import zh_CN as liblang

            self.olang = lang
            self.omode = mode
            self.oencode = encode
            self.liblang = liblang
        except:
            file = open("options", "w")
            lang = "Language=" + Default.lang
            mode = "Mode=" + Default.mode
            encode = "Encoding=" + Default.encoding
            from lang import en_US as liblang
            file.write("\n".join((lang, mode, encode)))
            file.close()

            self.olang = lang
            self.omode = mode
            self.oencode = encode
            self.liblang = liblang

    def lang_register(self, widget):
        self.set_stat = True
        if widget.get_label() == "English":
            self.olang = "en_US"
        else:
            self.olang = "zh_CN"

    def mode_register(self, widget):
        self.set_stat = True
        if widget.get_label() == liblang.lbl_set_label[2]:
            self.omode = "Normal"
        else:
            self.omode = "Hex"

    def encode_register(self, widget):
        self.set_stat = True
        if widget.get_label() == "ASCII":
            self.oencode = "ASCII"
        else:
            self.oencode = "Unicode"

    def settings_dialog(self, widget=None, win=None):
        opt_win = Gtk.Window()
        opt_win.set_title(self.liblang.menu_edit_[4])
        opt_win.set_resizable(False)
        opt_win.set_size_request(200, -1)
        opt_win.set_transient_for(win)
        opt_win.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        opt_win.set_modal(True)
        opt_win.set_destroy_with_parent(True)
        opt_win.set_border_width(10)
        opt_win.connect("key_press_event", event_esc_exit, self.liblang, opt_win)

        box_general = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        frame_lang = Gtk.Frame(label=self.liblang.lbl_set_label[0])
        box_general.pack_start(frame_lang, True, True, 5)
        box_lang_b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        frame_lang.add(box_lang_b)
        box_lang_s = Gtk.Box()
        box_lang_b.pack_start(box_lang_s, True, True, 0)
        eng = Gtk.RadioButton(label="English")
        chn = Gtk.RadioButton(group=eng, label="中文")
        eng.connect("toggled", self.lang_register)
        chn.connect("toggled", self.lang_register)
        box_lang_s.pack_start(eng, True, True, 0)
        box_lang_s.pack_end(chn, True, True, 0)

        note = Gtk.Label(self.liblang.set_note)
        note.set_line_wrap(True)
        note.set_max_width_chars(30)
        note.set_single_line_mode(False)
        box_lang_b.pack_start(note, True, True, 5)

        frame_mode = Gtk.Frame(label=self.liblang.lbl_set_label[1])
        box_general.pack_start(frame_mode, True, True, 5)
        box_mode = Gtk.Box()
        frame_mode.add(box_mode)
        nrm = Gtk.RadioButton(label=self.liblang.lbl_set_label[2])
        hexmode = Gtk.RadioButton(group=nrm, label=self.liblang.lbl_set_label[3])
        nrm.connect("toggled", self.mode_register)
        hexmode.connect("toggled", self.mode_register)
        box_mode.pack_start(nrm, True, True, 0)
        box_mode.pack_start(hexmode, True, True, 0)

        frame_encode = Gtk.Frame(label="Encodings")
        box_general.pack_start(frame_encode, True, True, 5)
        box_encode = Gtk.Box()
        frame_encode.add(box_encode)
        asc = Gtk.RadioButton(label="ASCII")
        uni = Gtk.RadioButton(label="Unicode", group=asc)
        asc.connect("toggled", self.encode_register)
        uni.connect("toggled", self.encode_register)
        box_encode.pack_start(asc, True, True, 0)
        box_encode.pack_start(uni, True, True, 0)

        box_btn = Gtk.Box()
        box_general.pack_end(box_btn, True, False, 3)
        apply_button = Gtk.Button(self.liblang.lbl_set_btn[0])
        close_button = Gtk.Button(self.liblang.lbl_set_btn[1])
        apply_button.connect("clicked", self.applyset, self)
        close_button.connect("clicked", quit_window, opt_win)
        box_btn.pack_start(apply_button, False, False, 0)
        box_btn.pack_end(close_button, False, False, 0)

        if self.olang == "en_US": eng.set_active(True)
        else: chn.set_active(True)
        if self.omode == "Normal": nrm.set_active(True)
        else: hexmode.set_active(True)

        self.set_stat = False
        opt_win.add(box_general)
        opt_win.show_all()

    def applyset(self, button):
        if self.set_stat:
            file = open("options", "w")
            lang = "Language=" + olang
            mode = "Mode=" + omode
            encode = "Encoding=" + oencode
            file.write("\n".join((lang, mode, encode)))
            file.close()
            Settings()
            Restart()

class main_window(Gtk.Window):

    def init_UI(self, _set):
        ### Basic Window ###
        self.set_title(_set.liblang.title + " - " + title_mode + " " + _set.liblang.lbl_set_label[1])
        self.set_icon_name(prog_ico_name)
        self.set_resizable(False)
        self.set_size_request(400, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.connect("key_press_event", event_esc_exit, _set.liblang, win)

        ### General Box ###
        box_general = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box_general)

        ### Menu ###
        menubar = Gtk.MenuBar()
        menubar.set_hexpand(True)
        box_general.pack_start(menubar, False, False, 0)

        accelgroup = Gtk.AccelGroup()
        self.add_accel_group(accelgroup)

        # Edit Menu #
        sub_edit_menu = Gtk.Menu()
        copy_submenu = Gtk.MenuItem(_set.liblang.menu_edit_[0])
        cut_submenu = Gtk.MenuItem(_set.liblang.menu_edit_[1])
        paste_submenu = Gtk.MenuItem(_set.liblang.menu_edit_[2])
        selectall_submenu = Gtk.MenuItem(_set.liblang.menu_edit_[3])
        menu_separater = Gtk.SeparatorMenuItem()
        preference_submenu = Gtk.Action(_set.liblang.menu_edit_[4], "_" + _set.liblang.menu_edit_[4], None, None).create_menu_item()

        copy_submenu.connect("activate", clipboard_callback, "copy")
        cut_submenu.connect("activate", clipboard_callback, "cut")
        paste_submenu.connect("activate", clipboard_callback, "paste")
        selectall_submenu.connect("activate", selectall)
        preference_submenu.connect("activate", _set.settings_dialog, self)

        preference_submenu.add_accelerator("activate", accelgroup, \
                Gdk.keyval_from_name("P"), \
                Gdk.ModifierType.CONTROL_MASK \
                | Gdk.ModifierType.MOD1_MASK, Gtk.AccelFlags.VISIBLE)

        sub_edit_menu.append(copy_submenu)
        sub_edit_menu.append(cut_submenu)
        sub_edit_menu.append(paste_submenu)
        sub_edit_menu.append(selectall_submenu)
        sub_edit_menu.append(menu_separater)
        sub_edit_menu.append(preference_submenu)

        edit_menu = Gtk.Action("Edit", "_Edit", None, None).create_menu_item()
        menubar.append(edit_menu)
        edit_menu.set_submenu(sub_edit_menu)

        # Help Menu #
        sub_help_menu = Gtk.Menu()
        help_submenu = Gtk.Action(_set.liblang.menu_help, "_" + _set.liblang.menu_help, None, None).create_menu_item()
        menu_separater = Gtk.SeparatorMenuItem()
        about_submenu = Gtk.Action(_set.liblang.lbl_btn[3], "_" + _set.liblang.lbl_btn[3], None, None).create_menu_item()

        help_submenu.connect("activate", showhelp, self, _set.liblang)
        about_submenu.connect("activate", about_program, win, _set.liblang)

        help_submenu.add_accelerator("activate", accelgroup, Gdk.keyval_from_name("F1"), 0, Gtk.AccelFlags.VISIBLE)

        sub_help_menu.append(help_submenu)
        sub_help_menu.append(menu_separater)
        sub_help_menu.append(about_submenu)

        help_menu = Gtk.Action("Help", "_Help", None, None).create_menu_item()
        menubar.append(help_menu)
        help_menu.set_submenu(sub_help_menu)

        ### Text Box ###
        align = Gtk.Alignment()
        align.set(0, 0, 0, 0)
        align.set_padding(2, 0, 10, 0)

        lbl_textbox = Gtk.Label()
        lbl_textbox.set_markup("<b>%s</b>" % _set.liblang.lbl_label[0])
        lbl_textbox.set_tooltip_text(_set.liblang.tooltip[0])
        box_general.pack_start(align, False, False, 0)
        align.add(lbl_textbox)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        scrolled_window.set_hexpand(False)
        scrolled_window.set_vexpand(True)
        box_general.pack_start(scrolled_window, True, True, 0)

        self.textbox_buf = Gtk.TextBuffer()
        text_box = Gtk.TextView(buffer=self.textbox_buf)
        text_box.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scrolled_window.add(text_box)

        ### Separater ###
        separater = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        box_general.pack_start(separater, False, False, 7)

        ### Message Box ###
        box_stat = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        box_msg = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        box_timeused = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        box_general.pack_start(box_stat, False, False, 0)
        box_general.pack_start(box_msg, False, False, 0)
        box_general.pack_start(box_timeused, False, False, 0)

        lbl_stat = Gtk.Label()
        lbl_msg = Gtk.Label()
        lbl_timeused = Gtk.Label()

        lbl_stat.set_markup("<span font=\"Ubuntu Mono 12\">%s</span>" % _set.liblang.lbl_label[1])
        lbl_msg.set_markup("<span font=\"Ubuntu Mono 12\">%s</span>" % _set.liblang.lbl_label[2])
        lbl_timeused.set_markup("<span font=\"Ubuntu Mono 12\">%s</span>" % _set.liblang.lbl_label[3])

        lbl_stat.set_tooltip_text(_set.liblang.tooltip[1])
        lbl_msg.set_tooltip_text(_set.liblang.tooltip[2])
        lbl_timeused.set_tooltip_text(_set.liblang.tooltip[3])

        self.StrVarStat = Gtk.Label()
        self.StrVarMsg = Gtk.Label()
        self.StrVarTimeUsed = Gtk.Label()

        box_stat.pack_start(lbl_stat, False, False, 0)
        box_stat.pack_end(self.StrVarStat, False, False, 0)

        box_msg.pack_start(lbl_msg, False, False, 0)
        box_msg.pack_end(self.StrVarMsg, False, False, 0)

        box_timeused.pack_start(lbl_timeused, False, False, 0)
        box_timeused.pack_end(self.StrVarTimeUsed, False, False, 0)

        ### Buttons ###
        boxBtn = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box_general.pack_start(boxBtn, False, False, 2)

        btnEncrypt = Gtk.Button(_set.liblang.lbl_btn[0], None, True)
        btnDecrypt = Gtk.Button(_set.liblang.lbl_btn[1], None, True)
        btnClear = Gtk.Button(_set.liblang.lbl_btn[2], None, True)
        btnAbout = Gtk.Button(_set.liblang.lbl_btn[3], None, True)

        btnEncrypt.set_tooltip_text(_set.liblang.tooltip[4])
        btnDecrypt.set_tooltip_text(_set.liblang.tooltip[5])
        btnClear.set_tooltip_text(_set.liblang.tooltip[6])
        btnAbout.set_tooltip_text(_set.liblang.tooltip[7])

        btnEncrypt.connect("clicked", encrypt, self, _set.liblang)
        btnDecrypt.connect("clicked", decrypt, self, _set.liblang)
        btnClear.connect("clicked", cleartext, self, False)
        btnAbout.connect("clicked", about, self, _set.liblang)

        boxBtn.pack_start(btnEncrypt, True, True, 0)
        boxBtn.pack_start(btnDecrypt, True, True, 0)
        boxBtn.pack_start(btnClear, True, True, 0)
        boxBtn.pack_start(btnAbout, True, True, 0)
        boxBtn.set_homogeneous(True)

### Program ###
Set = Settings()

if Set.omode == "Hex":
    title_mode = Set.liblang.lbl_set_label[3]
else:
    title_mode = Set.liblang.lbl_set_label[2]

prog_ico_name = "emblem-readonly"

show_notification(Set.liblang.notification)

win = main_window()
win.init_UI(Set)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
