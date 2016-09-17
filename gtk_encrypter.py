#!/usr/bin/python3

# -*- coding: utf-8 -*-
### GUI Encrypter by Zhu Haoqing (Originally Zhang Jingye) ###
### Rev: 5.0
### Auto Copy after process added
### Time bugs fixed

import lang
from library import *
from configparser import ConfigParser

class Environ():

    def __init__(self):
        self.config = ConfigParser()
        self.config.optionxform = lambda a:a
        try:
            self.config.read("options")
            _normal = self.config["Normal"]
            self.lang = _normal.get("Language", default.lang)
            self.encode = _normal.get("Encoding", default.encode)
            self.method = _normal.get("Method", default.method)
        except:
            self.config["Normal"] = {"Language": default.lang,
                                "Encoding": default.encode,
                                "Method": default.method}
        try:
            _extra = self.config["Extra"]
            self.extra = {k: _extra[k] for k in _extra}
        except:
            self.config["Extra"] = {}
        with open("options", "w") as f: self.config.write(f)
            #self.lang = default.lang
            #self.method = default.method
            #self.encode = default.encode
            #self.extra = default.extra

        if self.method not in find_methods(): set_text_mono( \
                self.strvarmsg, env.res.msg_err_met % self.method)

        self.res = vars(lang)[self.lang]

    def register(self, button):
        label = button.get_label()
        if label == "English": self.lang = "en_US"
        elif label == "中文":  self.lang = "zh_CN"
        elif label == "UTF-8": self.encode = "UTF"
        elif label == "Unicode": self.encode = "Uni"

    def method_register(self, button):
        self.method = button.get_label()

    def extra_register(self, button, label):
        self.extra[label] = eval(button.get_label())

    def load_methods(self, button, grid, opt_win, box=None):
        methods = find_methods()
        globals().update(methods)
        grid.remove_column(0)
        grid.remove_column(0)
        if len(methods) == 0: grid.attach( \
                Gtk.Label(self.res.msg_met_nava), 0, 0, 1, 1)
        group = None
        for i, v in enumerate(methods):
            rb = Gtk.RadioButton(label=v, group=group)
            if i == 0: group = rb
            grid.attach(rb, *divmod(i, 2)[::-1], 1, 1)
            rb.connect("clicked", self.method_register)
            if box: rb.connect("clicked", self.load_extras, box, opt_win)
            if v == self.method: rb.set_active(True)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)

        opt_win.show_all()

    def load_extras(self, button, box, opt_win):
        for child in box.get_children(): box.remove(child)
        extra = globals()[self.method].extra
        if extra == {}:
            box.pack_start(Gtk.Label(self.res.lbl_no_ext), True, True, 5)
            return
        for key in extra:
            ava_values = extra[key]
            grid = Gtk.Grid()
            box.pack_start(grid, True, True, 3)
            grid.attach(Gtk.Label(key), 0, 0, 1, 1)
            group = None
            for num, val in enumerate(ava_values):
                rb = Gtk.RadioButton(label=str(val), group=group)
                if num == 0: group = rb
                grid.attach(rb, 1, num, 1, 1)
                rb.connect("clicked", self.extra_register, key)
                if val == self.extra.get(key): rb.set_active(True)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        opt_win.show_all()

    def settings_dialog(self, widget, win):
        opt_win = Gtk.Window()
        opt_win.set_title(self.res.menu_edit_[4])
        #opt_win.set_resizable(False)
        opt_win.set_transient_for(win)
        opt_win.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        opt_win.set_modal(True)
        opt_win.set_destroy_with_parent(True)
        opt_win.set_border_width(10)
        #opt_win.connect("key-press-event", event_esc_exit)
        opt_win.connect("delete-event", self.applyset, win)

        box_general = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        frame_lang = Gtk.Frame(label=self.res.lbl_set_frm[0])
        box_general.pack_start(frame_lang, True, True, 5)
        box_lang_b = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        frame_lang.add(box_lang_b)
        box_lang_s = Gtk.Box()
        box_lang_b.pack_start(box_lang_s, True, True, 0)
        eng = Gtk.RadioButton(label="English")
        chn = Gtk.RadioButton(group=eng, label="中文")
        eng.connect("toggled", self.register)
        chn.connect("toggled", self.register)
        box_lang_s.pack_start(eng, True, True, 0)
        box_lang_s.pack_end(chn, True, True, 0)

        note = Gtk.Label(self.res.set_note)
        note.set_line_wrap(True)
        note.set_max_width_chars(30)
        note.set_single_line_mode(False)
        box_lang_b.pack_start(note, True, True, 5)

        frame_encode = Gtk.Frame(label=self.res.lbl_set_frm[1])
        box_general.pack_start(frame_encode, True, True, 5)
        box_encode = Gtk.Box()
        frame_encode.add(box_encode)
        utf = Gtk.RadioButton(label="UTF-8")
        uni = Gtk.RadioButton(label="Unicode", group=utf)
        utf.connect("toggled", self.register)
        uni.connect("toggled", self.register)
        box_encode.pack_start(utf, True, True, 0)
        box_encode.pack_start(uni, True, True, 0)

        frame_method = Gtk.Frame(label=self.res.lbl_set_frm[2])
        box_general.pack_start(frame_method, True, True, 5)
        frame_method.set_tooltip_text(self.res.tooltip[8])
        box_method = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        frame_method.add(box_method)
        btn_refresh = Gtk.Button.new_from_icon_name("view-refresh", \
                Gtk.IconSize.LARGE_TOOLBAR)
        box_method.pack_start(btn_refresh, False, False, 3)
        btn_refresh.set_tooltip_text(self.res.tooltip[9])
        grid_method = Gtk.Grid()
        box_method.pack_start(grid_method, False, False, 3)

        frame_extra = Gtk.Frame(label=self.res.lbl_set_frm[3])
        box_general.pack_start(frame_extra, True, True, 5)
        box_extra = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        frame_extra.add(box_extra)
        self.load_methods(None, grid_method, opt_win, box_extra)
        btn_refresh.connect("clicked", self.load_methods, \
                grid_method, opt_win, box_extra)
        self.load_extras(None, box_extra, opt_win)

        (eng if self.lang == "en_US" else chn).set_active(True)
        (utf if self.encode == "UTF" else uni).set_active(True)

        opt_win.add(box_general)
        opt_win.show_all()

    def applyset(self, opt_win, event, main_win):
        self.config["Normal"] = {
                "Language": self.lang,
                "Encoding": self.encode,
                "Method": self.method}
        self.config["Extra"] = self.extra
        with open("options", "w") as f: self.config.write(f)
        main_win.set_title(self.res.title + " - " + \
                self.res.lbl_set_frm[2] + ": " + self.method)

class main_window(Gtk.Window):

    def __init__(self, env):
        super().__init__()
        add_ = lambda a: (a, "_" + a)
        ### Basic Window ###
        self.set_title(env.res.title + " - " + \
                env.res.lbl_set_frm[2] + ": " + env.method)
        self.set_icon_name(prog_ico_name)
        self.set_resizable(False)
        self.set_size_request(400, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        #self.connect("key-press-event", event_esc_exit)

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
        copy_submenu = Gtk.MenuItem(env.res.menu_edit_[0])
        cut_submenu = Gtk.MenuItem(env.res.menu_edit_[1])
        paste_submenu = Gtk.MenuItem(env.res.menu_edit_[2])
        selectall_submenu = Gtk.MenuItem(env.res.menu_edit_[3])
        preference_submenu = Gtk.Action(*add_(env.res.menu_edit_[4]), None, None).create_menu_item()

        copy_submenu.connect("activate", clipbd_cb, self, "copy")
        cut_submenu.connect("activate", clipbd_cb, self, "cut")
        paste_submenu.connect("activate", clipbd_cb, self, "paste")
        selectall_submenu.connect("activate", selectall, self)
        preference_submenu.connect("activate", env.settings_dialog, self)

        preference_submenu.add_accelerator("activate", accelgroup, \
                Gdk.keyval_from_name("P"), \
                Gdk.ModifierType.CONTROL_MASK \
                | Gdk.ModifierType.MOD1_MASK, Gtk.AccelFlags.VISIBLE)

        sub_edit_menu.append(copy_submenu)
        sub_edit_menu.append(cut_submenu)
        sub_edit_menu.append(paste_submenu)
        sub_edit_menu.append(selectall_submenu)
        sub_edit_menu.append(Gtk.SeparatorMenuItem())
        sub_edit_menu.append(preference_submenu)

        edit_menu = Gtk.Action(*add_("Edit"), None, None).create_menu_item()
        menubar.append(edit_menu)
        edit_menu.set_submenu(sub_edit_menu)

        # Help Menu #
        sub_help_menu = Gtk.Menu()
        help_submenu = Gtk.Action(*add_(env.res.menu_help), None, None).create_menu_item()
        about_submenu = Gtk.Action(*add_(env.res.lbl_btn[3]), None, None).create_menu_item()

        help_submenu.connect("activate", showhelp, self, env.res)
        about_submenu.connect("activate", about_program, self, env.res)

        help_submenu.add_accelerator("activate", accelgroup, Gdk.keyval_from_name("F1"), 0, Gtk.AccelFlags.VISIBLE)

        sub_help_menu.append(help_submenu)
        sub_help_menu.append(Gtk.SeparatorMenuItem())
        sub_help_menu.append(about_submenu)

        help_menu = Gtk.Action(*add_("Help"), None, None).create_menu_item()
        menubar.append(help_menu)
        help_menu.set_submenu(sub_help_menu)

        ### Text Box ###
        align = Gtk.Alignment()
        align.set(0, 0, 0, 0)
        align.set_padding(2, 0, 10, 0)

        lbl_textbox = Gtk.Label()
        lbl_textbox.set_markup("<b>%s</b>" % env.res.lbl_label[0])
        lbl_textbox.set_tooltip_text(env.res.tooltip[0])
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
        lbl_stat.set_markup(mono(env.res.lbl_label[1]))
        lbl_msg.set_markup(mono(env.res.lbl_label[2]))
        lbl_timeused.set_markup(mono(env.res.lbl_label[3]))
        del mono

        lbl_stat.set_tooltip_text(env.res.tooltip[1])
        lbl_msg.set_tooltip_text(env.res.tooltip[2])
        lbl_timeused.set_tooltip_text(env.res.tooltip[3])

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
        btn_box = Gtk.Box(spacing=6)
        box_general.pack_start(btn_box, False, False, 2)

        btn_encrypt = Gtk.Button(env.res.lbl_btn[0], None, True)
        btn_decrypt = Gtk.Button(env.res.lbl_btn[1], None, True)
        btn_clear = Gtk.Button(env.res.lbl_btn[2], None, True)
        btn_about = Gtk.Button(env.res.lbl_btn[3], None, True)

        btn_encrypt.set_tooltip_text(env.res.tooltip[4])
        btn_decrypt.set_tooltip_text(env.res.tooltip[5])
        btn_clear.set_tooltip_text(env.res.tooltip[6])
        btn_about.set_tooltip_text(env.res.tooltip[7])

        btn_encrypt.connect("clicked", encrypt, self, env)
        btn_decrypt.connect("clicked", decrypt, self, env)
        btn_clear.connect("clicked", cleartext, self, True)
        btn_about.connect("clicked", about, self, env.res)

        btn_box.pack_start(btn_encrypt, True, True, 0)
        btn_box.pack_start(btn_decrypt, True, True, 0)
        btn_box.pack_start(btn_clear, True, True, 0)
        btn_box.pack_start(btn_about, True, True, 0)
        btn_box.set_homogeneous(True)

### Program ###
env = Environ()
prog_ico_name = "emblem-readonly"
show_notification(env.res.notification)

win = main_window(env)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
