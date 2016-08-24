#!/usr/bin/python3

# -*- coding: utf-8 -*-
### GUI Encrypter by Zhu Haoqing (Originally Zhang Jingye) ###
### Rev: 5.0
### Runtime Environment: Python3
### Hexage Mode added (USE WITH CAUTION!!!)
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
            self.lang = settings["Language"]
            self.mode = settings["Mode"]
            self.encode = settings["Encoding"]
            self.cipher = settings["Cipher"]

            if lang == "en_US": from lang import en_US as liblang
            else:               from lang import zh_CN as liblang

            self.liblang = liblang
        except:
            file = open("options", "w")
            lang = "Language=" + default.lang
            mode = "Mode=" + default.mode
            encode = "Encoding=" + default.encoding
            cipher = "Cipher=" + default.cipher
            from lang import en_US as liblang
            file.write("\n".join((lang, mode, encode, cipher)))
            file.close()

            self.lang = lang
            self.mode = mode
            self.cipher = cipher
            self.encode = encode
            self.liblang = liblang

    def lang_register(self, widget):
        self.set_stat = True
        if widget.get_label() == "English": self.lang = "en_US"
        else:                               self.lang = "zh_CN"

    def mode_register(self, widget):
        self.set_stat = True
        if widget.get_label() == self.liblang.lbl_set_label[2]:
            self.mode = "Normal"
        else:
            self.mode = "Hex"

    def encode_register(self, widget):
        self.set_stat = True
        if widget.get_label() == "UTF-8": self.encode = "UTF"
        else:                             self.encode = "Uni"

    def settings_dialog(self, widget, win):
        opt_win = Gtk.Window()
        opt_win.set_title(self.liblang.menu_edit_[4])
        opt_win.set_resizable(False)
        opt_win.set_size_request(200, -1)
        opt_win.set_transient_for(win)
        opt_win.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        opt_win.set_modal(True)
        opt_win.set_destroy_with_parent(True)
        opt_win.set_border_width(10)
        opt_win.connect("key_press_event", event_esc_exit, self.liblang)

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
        norm = Gtk.RadioButton(label=self.liblang.lbl_set_label[2])
        hexm = Gtk.RadioButton(group=norm, label=self.liblang.lbl_set_label[3])
        norm.connect("toggled", self.mode_register)
        hexm.connect("toggled", self.mode_register)
        box_mode.pack_start(norm, True, True, 0)
        box_mode.pack_start(hexm, True, True, 0)

        frame_encode = Gtk.Frame(label="Encodings")
        box_general.pack_start(frame_encode, True, True, 5)
        box_encode = Gtk.Box()
        frame_encode.add(box_encode)
        utf = Gtk.RadioButton(label="UTF-8")
        uni = Gtk.RadioButton(label="Unicode", group=utf)
        utf.connect("toggled", self.encode_register)
        uni.connect("toggled", self.encode_register)
        box_encode.pack_start(utf, True, True, 0)
        box_encode.pack_start(uni, True, True, 0)

        box_btn = Gtk.Box()
        box_general.pack_end(box_btn, True, False, 3)
        apply_button = Gtk.Button(self.liblang.lbl_set_btn[0])
        close_button = Gtk.Button(self.liblang.lbl_set_btn[1])
        apply_button.connect("clicked", self.applyset)
        close_button.connect("clicked", \
                lambda a, b: b.destroy(), opt_win)
        box_btn.pack_start(apply_button, False, False, 0)
        box_btn.pack_end(close_button, False, False, 0)

        (eng if self.lang == "en_US" else chn).set_active(True)
        (hexm if self.lang == "Normal" else norm).set_active(True)
        (uni if self.lang == "UTF" else utf).set_active(True)

        self.set_stat = False
        opt_win.add(box_general)
        opt_win.show_all()

    def applyset(self, button):
        if self.set_stat:
            file = open("options", "w")
            lang = "Language=" + self.lang
            mode = "Mode=" + self.mode
            encode = "Encoding=" + self.encode
            file.write("\n".join((lang, mode, encode)))
            file.close()
            Settings()
            os.execl(sys.executable, sys.executable, *sys.argv)# Restart

class main_window(Gtk.Window):

    def init_UI(self, _set):
        add_ = lambda a: (a, "_" + a)
        ### Basic Window ###
        title_method = Set.liblang.lbl_set_label[3 if Set.mode == "Hex" else 2]
        self.set_title(_set.liblang.title + " - " + title_method + " " + _set.liblang.lbl_set_label[1])
        self.set_icon_name(prog_ico_name)
        self.set_resizable(False)
        self.set_size_request(400, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.connect("key_press_event", event_esc_exit, _set.liblang)

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
        preference_submenu = Gtk.Action(*add_(_set.liblang.menu_edit_[4]), None, None).create_menu_item()

        copy_submenu.connect("activate", clipbd_cb, "copy")
        cut_submenu.connect("activate", clipbd_cb, "cut")
        paste_submenu.connect("activate", clipbd_cb, "paste")
        selectall_submenu.connect("activate", selectall, self)
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

        edit_menu = Gtk.Action(*add_("Edit"), None, None).create_menu_item()
        menubar.append(edit_menu)
        edit_menu.set_submenu(sub_edit_menu)

        # Help Menu #
        sub_help_menu = Gtk.Menu()
        help_submenu = Gtk.Action(*add_(_set.liblang.menu_help), None, None).create_menu_item()
        menu_separater = Gtk.SeparatorMenuItem()
        about_submenu = Gtk.Action(*add_(_set.liblang.lbl_btn[3]), None, None).create_menu_item()

        help_submenu.connect("activate", showhelp, self, _set.liblang)
        about_submenu.connect("activate", about_program, win, _set.liblang)

        help_submenu.add_accelerator("activate", accelgroup, Gdk.keyval_from_name("F1"), 0, Gtk.AccelFlags.VISIBLE)

        sub_help_menu.append(help_submenu)
        sub_help_menu.append(menu_separater)
        sub_help_menu.append(about_submenu)

        help_menu = Gtk.Action(*add_("Help"), None, None).create_menu_item()
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

        self.text_buf = Gtk.TextBuffer()
        text_box = Gtk.TextView(buffer=self.text_buf)
        text_box.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scrolled_window.add(text_box)

        ### Separater ###
        box_general.pack_start(Gtk.Separator(), False, False, 7)

        ### Message Box ###
        box_stat = Gtk.Box()
        box_msg = Gtk.Box()
        box_timeused = Gtk.Box()

        box_general.pack_start(box_stat, False, False, 0)
        box_general.pack_start(box_msg, False, False, 0)
        box_general.pack_start(box_timeused, False, False, 0)

        lbl_stat = Gtk.Label()
        lbl_msg = Gtk.Label()
        lbl_timeused = Gtk.Label()

        mono = lambda a: "<span font=\"Ubuntu Mono 12\">%s</span>" % a
        lbl_stat.set_markup(mono(_set.liblang.lbl_label[1]))
        lbl_msg.set_markup(mono(_set.liblang.lbl_label[2]))
        lbl_timeused.set_markup(mono(_set.liblang.lbl_label[3]))
        del mono

        lbl_stat.set_tooltip_text(_set.liblang.tooltip[1])
        lbl_msg.set_tooltip_text(_set.liblang.tooltip[2])
        lbl_timeused.set_tooltip_text(_set.liblang.tooltip[3])

        self.strvarstat = Gtk.Label()
        self.strvarmsg = Gtk.Label()
        self.strvartimeused = Gtk.Label()

        box_stat.pack_start(lbl_stat, False, False, 0)
        box_stat.pack_end(self.strvarstat, False, False, 0)

        box_msg.pack_start(lbl_msg, False, False, 0)
        box_msg.pack_end(self.strvarmsg, False, False, 0)

        box_timeused.pack_start(lbl_timeused, False, False, 0)
        box_timeused.pack_end(self.strvartimeused, False, False, 0)

        ### Buttons ###
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box_general.pack_start(btn_box, False, False, 2)

        encrypt_btn = Gtk.Button(_set.liblang.lbl_btn[0], None, True)
        decrypt_btn = Gtk.Button(_set.liblang.lbl_btn[1], None, True)
        clear_btn = Gtk.Button(_set.liblang.lbl_btn[2], None, True)
        about_btn = Gtk.Button(_set.liblang.lbl_btn[3], None, True)

        encrypt_btn.set_tooltip_text(_set.liblang.tooltip[4])
        decrypt_btn.set_tooltip_text(_set.liblang.tooltip[5])
        clear_btn.set_tooltip_text(_set.liblang.tooltip[6])
        about_btn.set_tooltip_text(_set.liblang.tooltip[7])

        encrypt_btn.connect("clicked", encrypt, self, _set)
        decrypt_btn.connect("clicked", decrypt, self, _set)
        clear_btn.connect("clicked", cleartext, self, True)
        about_btn.connect("clicked", about, self, _set.liblang)

        btn_box.pack_start(encrypt_btn, True, True, 0)
        btn_box.pack_start(decrypt_btn, True, True, 0)
        btn_box.pack_start(clear_btn, True, True, 0)
        btn_box.pack_start(about_btn, True, True, 0)
        btn_box.set_homogeneous(True)

### Program ###
Set = Settings()
prog_ico_name = "emblem-readonly"
show_notification(Set.liblang.notification)

win = main_window()
win.init_UI(Set)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
