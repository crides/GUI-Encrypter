#!/usr/bin/python3

# -*- coding: utf-8 -*-
### GUI Encrypter by Zhu Haoqing(Originally Zhang Jingye) ###
### Rev: 4.0
### Runtime Environment: Python3.4
### Hexage Mode added
### Auto Copy after process added
### Time bugs fixed

import Lang
from Library import *
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, Gdk, Notify

class Settings():

    set_stat = False

    def __init__(self):
        try:
            file = open('options')
            lines = file.read()
            if lines == '':
                raise IOError
            line = lines.splitlines()
            settings = {}
            for i in line:
                j = i.split('=')
                settings[j[0]] = j[1]
            file.close()
            olang = settings.get('Language')
            omode = settings.get('Mode')

            if olang == 'en_US':
                from Lang import en_US as liblang
            else:
                from Lang import zh_CN as liblang

            self.olang = olang
            self.omode = omode
            self.liblang = liblang
        except:
            file = open('options', 'w')
            olang = 'Language' + '=' + Default.lang
            omode = 'Mode' + '=' + Default.mode
            from Lang import en_US as liblang
            file.write('\n'.join((lang, mode)))
            file.close()

            self.olang = olang
            self.omode = omode
            self.liblang = liblang

    def lang_register(widget, self):
        self.set_stat = True
        global olang
        if widget.get_label() == 'English':
            olang = 'en_US'
        else:
            olang = 'zh_CN'

    def mode_register(widget, self):
        self.set_stat = True
        global omode
        if widget.get_label() == liblang.Lbl_set_Label[2]:
            omode = 'Normal'
        else:
            omode = 'Hex'

    def SettingDialog(button, self):
        optionwin = Gtk.Window()
        optionwin.set_title(liblang.Menu_Edit_[4])
        optionwin.set_resizable(False)
        optionwin.set_size_request(200, -1)
        optionwin.set_transient_for(win)
        optionwin.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        optionwin.set_modal(True)
        optionwin.set_destroy_with_parent(True)
        optionwin.set_border_width(10)
        optionwin.connect('key_press_event', event_esc_exit, liblang, optionwin)

        option_boxGeneral = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        option_frameLang = Gtk.Frame(label=liblang.Lbl_set_Label[0])
        option_boxGeneral.pack_start(option_frameLang, True, True, 5)
        option_boxLangb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        option_frameLang.add(option_boxLangb)
        option_boxLangs = Gtk.Box()
        option_boxLangb.pack_start(option_boxLangs, True, True, 0)
        eng = Gtk.RadioButton(label='English')
        chn = Gtk.RadioButton(group=eng, label='中文')
        eng.connect('toggled', self.lang_register, self)
        chn.connect('toggled', self.lang_register, self)
        option_boxLangs.pack_start(eng, True, True, 0)
        option_boxLangs.pack_end(chn, True, True, 0)

        note = Gtk.Label(liblang.set_Note)
        note.set_line_wrap(True)
        note.set_max_width_chars(30)
        note.set_single_line_mode(False)
        option_boxLangb.pack_start(note, True, True, 5)

        option_frameMode = Gtk.Frame(label=liblang.Lbl_set_Label[1])
        option_boxGeneral.pack_start(option_frameMode, True, True, 5)
        option_boxMode = Gtk.Box()
        option_frameMode.add(option_boxMode)
        nrm = Gtk.RadioButton(label=liblang.Lbl_set_Label[2])
        hexmode = Gtk.RadioButton(group=nrm, label=liblang.Lbl_set_Label[3])
        nrm.connect('toggled', self.mode_register, self)
        hexmode.connect('toggled', self.mode_register, self)
        option_boxMode.pack_start(nrm, True, True, 0)
        option_boxMode.pack_start(hexmode, True, True, 0)

        option_boxBtn = Gtk.Box()
        option_boxGeneral.pack_end(option_boxBtn, True, False, 3)
        btnApply = Gtk.Button(liblang.Lbl_set_Btn[0])
        btnClose = Gtk.Button(liblang.Lbl_set_Btn[1])
        btnApply.connect('clicked', self.applyset, self)
        btnClose.connect('clicked', quit_window, optionwin)
        option_boxBtn.pack_start(btnApply, False, False, 0)
        option_boxBtn.pack_end(btnClose, False, False, 0)

        if olang == 'en_US':eng.set_active(True)
        else:chn.set_active(True)
        if omode == 'Normal':nrm.set_active(True)
        else:hexmode.set_active(True)

        self.set_stat = False
        optionwin.add(option_boxGeneral)
        optionwin.show_all()

    def applyset(button, self):
        if self.set_stat:
            file = open('options', 'w')
            lang = 'Language' + '=' + olang
            mode = 'Mode' + '=' + omode
            file.write('\n'.join((lang, mode)))
            file.close()
            Settings()
            Restart()

class MainWindow(Gtk.Window):

    def InitUI(self):
        ### Basic Window ###
        self.set_title(liblang.Title + ' - ' + title_mode + ' ' + liblang.Lbl_set_Label[1])
        self.set_icon_name(program_icon_name)
        self.set_resizable(False)
        self.set_size_request(400, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.connect('key_press_event', event_esc_exit, liblang, win)

        ### General Box ###
        boxGeneral = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(boxGeneral)

        ### Menu ###
        menubar = Gtk.MenuBar()
        menubar.set_hexpand(True)
        boxGeneral.pack_start(menubar, False, False, 0)

        accelgroup = Gtk.AccelGroup()
        self.add_accel_group(accelgroup)

        # Edit Menu #
        sub_edit_menu = Gtk.Menu()
        copy_submenu = Gtk.MenuItem(liblang.Menu_Edit_[0])
        cut_submenu = Gtk.MenuItem(liblang.Menu_Edit_[1])
        paste_submenu = Gtk.MenuItem(liblang.Menu_Edit_[2])
        selectall_submenu = Gtk.MenuItem(liblang.Menu_Edit_[3])
        menu_separater = Gtk.SeparatorMenuItem()
        preference_submenu = Gtk.Action(liblang.Menu_Edit_[4], '_' + liblang.Menu_Edit_[4], None, None).create_menu_item()

        copy_submenu.connect('activate', clipboard_callback, 'copy', self)
        cut_submenu.connect('activate', clipboard_callback, 'cut', self)
        paste_submenu.connect('activate', clipboard_callback, 'paste', self)
        selectall_submenu.connect('activate', selectall, self)
        preference_submenu.connect('activate', Settings.SettingDialog, Settings)

        preference_submenu.add_accelerator('activate', accelgroup, Gdk.keyval_from_name('P'), Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK, Gtk.AccelFlags.VISIBLE)

        sub_edit_menu.append(copy_submenu)
        sub_edit_menu.append(cut_submenu)
        sub_edit_menu.append(paste_submenu)
        sub_edit_menu.append(selectall_submenu)
        sub_edit_menu.append(menu_separater)
        sub_edit_menu.append(preference_submenu)

        edit_menu = Gtk.Action('Edit', '_Edit', None, None).create_menu_item()
        menubar.append(edit_menu)
        edit_menu.set_submenu(sub_edit_menu)

        # Help Menu #
        sub_help_menu = Gtk.Menu()
        help_submenu = Gtk.Action(liblang.Menu_Help, '_' + liblang.Menu_Help, None, None).create_menu_item()
        menu_separater = Gtk.SeparatorMenuItem()
        about_submenu = Gtk.Action(liblang.Lbl_Btn[3], '_' + liblang.Lbl_Btn[3], None, None).create_menu_item()

        help_submenu.connect('activate', showhelp)
        about_submenu.connect('activate', about_program)

        help_submenu.add_accelerator('activate', accelgroup, Gdk.keyval_from_name('F1'), 0, Gtk.AccelFlags.VISIBLE)

        sub_help_menu.append(help_submenu)
        sub_help_menu.append(menu_separater)
        sub_help_menu.append(about_submenu)

        help_menu = Gtk.Action('Help', '_Help', None, None).create_menu_item()
        menubar.append(help_menu)
        help_menu.set_submenu(sub_help_menu)

        ### Text Box ###
        align = Gtk.Alignment()
        align.set(0, 0, 0, 0)
        align.set_padding(2, 0, 10, 0)

        Lbltextbox = Gtk.Label()
        Lbltextbox.set_markup('<b>%s</b>' % liblang.Lbl_Label[0])
        Lbltextbox.set_tooltip_text(liblang.Tooltip[0])
        boxGeneral.pack_start(align, False, False, 0)
        align.add(Lbltextbox)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        scrolledwindow.set_hexpand(False)
        scrolledwindow.set_vexpand(True)
        boxGeneral.pack_start(scrolledwindow, True, True, 0)

        self.TextBox_buffer = Gtk.TextBuffer()
        TextBox = Gtk.TextView(buffer=self.TextBox_buffer)
        TextBox.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scrolledwindow.add(TextBox)

        ### Separater ###
        separater = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        boxGeneral.pack_start(separater, False, False, 7)

        ### Message Box ###
        boxStat = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        boxMsg = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        boxTimeUsed = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        boxGeneral.pack_start(boxStat, False, False, 0)
        boxGeneral.pack_start(boxMsg, False, False, 0)
        boxGeneral.pack_start(boxTimeUsed, False, False, 0)

        LblStat = Gtk.Label()
        LblMsg = Gtk.Label()
        LblTimeUsed = Gtk.Label()

        LblStat.set_markup('<span font="Ubuntu Mono 12">%s</span>' % liblang.Lbl_Label[1])
        LblMsg.set_markup('<span font="Ubuntu Mono 12">%s</span>' % liblang.Lbl_Label[2])
        LblTimeUsed.set_markup('<span font="Ubuntu Mono 12">%s</span>' % liblang.Lbl_Label[3])

        LblStat.set_tooltip_text(liblang.Tooltip[1])
        LblMsg.set_tooltip_text(liblang.Tooltip[2])
        LblTimeUsed.set_tooltip_text(liblang.Tooltip[3])

        self.StrVarStat = Gtk.Label()
        self.StrVarMsg = Gtk.Label()
        self.StrVarTimeUsed = Gtk.Label()

        boxStat.pack_start(LblStat, False, False, 0)
        boxStat.pack_end(self.StrVarStat, False, False, 0)

        boxMsg.pack_start(LblMsg, False, False, 0)
        boxMsg.pack_end(self.StrVarMsg, False, False, 0)

        boxTimeUsed.pack_start(LblTimeUsed, False, False, 0)
        boxTimeUsed.pack_end(self.StrVarTimeUsed, False, False, 0)

        ### Buttons ###
        boxBtn = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        boxGeneral.pack_start(boxBtn, False, False, 2)

        btnEncrypt = Gtk.Button(liblang.Lbl_Btn[0], None, True)
        btnDecrypt = Gtk.Button(liblang.Lbl_Btn[1], None, True)
        btnClear = Gtk.Button(liblang.Lbl_Btn[2], None, True)
        btnAbout = Gtk.Button(liblang.Lbl_Btn[3], None, True)

        btnEncrypt.set_tooltip_text(liblang.Tooltip[4])
        btnDecrypt.set_tooltip_text(liblang.Tooltip[5])
        btnClear.set_tooltip_text(liblang.Tooltip[6])
        btnAbout.set_tooltip_text(liblang.Tooltip[7])

        btnEncrypt.connect('clicked', encrypt, self)
        btnDecrypt.connect('clicked', decrypt, self)
        btnClear.connect('clicked', cleartext, self, False)
        btnAbout.connect('clicked', about, self)

        boxBtn.pack_start(btnEncrypt, True, True, 0)
        boxBtn.pack_start(btnDecrypt, True, True, 0)
        boxBtn.pack_start(btnClear, True, True, 0)
        boxBtn.pack_start(btnAbout, True, True, 0)
        boxBtn.set_homogeneous(True)

### Program ###
Set = Settings()
omode = Set.omode
olang = Set.olang
liblang = Set.liblang

if omode == 'Hex':
    title_mode = liblang.Lbl_set_Label[3]
else:
    title_mode = liblang.Lbl_set_Label[2]

program_icon_name = 'emblem-readonly'

show_notification(liblang.notification)

win = MainWindow()
win.InitUI()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
