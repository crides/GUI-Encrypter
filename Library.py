#   FUNCTIONS

#   scale           Change Scale for the Number
#   count           Count Numbers of Items in Iterables
#   reverse         Turn the string around
#   encrypter       Encrypt the String and Output
#   decrypter       Decrypt the String and Output
#   hexencrypter    For Encryption of Hexage Mode
#   hexdecrypter    For Decryption of Hexage Mode
#   uc3             Intermediate Encryption Funtion
#   un3             Intermediate Decryption Funtion

import time
from math import floor
from random import random
import os, sys
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gdk, Notify

program_icon_name = 'emblem-readonly'

def event_esc_exit(widget, event, liblang, window=None):
    if event.keyval == Gdk.keyval_from_name('Escape'):
        window.destroy()
        if liblang.Title in window.get_title():
            Gtk.main_quit()

def quit_window(button, window):
    window.destroy()

def Restart():
    current = sys.executable
    os.execl(current, current, *sys.argv)

def clipboard_callback(button, action, self):
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    if action == 'copy':
        self.TextBox_buffer.copy_clipboard(clipboard)
    elif action == 'cut':
        self.TextBox_buffer.cut_clipboard(clipboard, True)
    elif action == 'paste':
        self.TextBox_buffer.paste_clipboard(clipboard, None, True)
    elif action == 'auto_copy':
        text_start, text_end = self.TextBox_buffer.get_bounds()
        text = self.TextBox_buffer.get_text(text_start, text_end, True)[:-1]
        clipboard.set_text(text, -1)
        show_notification('String copied into clipboard.')

def selectall(button, self):
    sel_start, sel_end = self.TextBox_buffer.get_bounds()
    self.TextBox_buffer.select_range(sel_start, sel_end)

def showhelp(button):
    helpwin = Gtk.Window()
    helpwin.set_transient_for(win)
    helpwin.set_title(liblang.Menu_Help)
    helpwin.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
    helpwin.set_destroy_with_parent(True)
    helpwin.set_border_width(10)
    helpwin.set_resizable(False)
    helpwin.connect('key_press_event', event_esc_exit, helpwin)

    helplabel = Gtk.Label(liblang.HELP.__doc__)
    helplabel.set_line_wrap(True)
    helplabel.set_max_width_chars(30)
    helpwin.add(helplabel)
    helpwin.show_all()

def about_program(button):
    GPL_License = open('GPL_License').read()
    aboutdialog = Gtk.AboutDialog(win)
    aboutdialog.set_program_name('GEncrypter')
    aboutdialog.set_version('4.0')
    aboutdialog.set_copyright('Copyright © 2012-2014 Jingye Zhang\nCopyright © 2014-2016 Haoqing Zhu')
    aboutdialog.set_comments(liblang.Abt_Comment)
    aboutdialog.set_license(GPL_License)
    aboutdialog.set_wrap_license(True)
    aboutdialog.set_authors(['<a href="https://github.com/zhangjingye03">Jingye Zhang</a>', '<a href="https://github.com/Irides-Chromium">Haoqing Zhu</a>'])
    aboutdialog.set_website('https://github.com/Irides-Chromium/GUI-Encrypter')
    aboutdialog.set_website_label('Github project repository')
    aboutdialog.set_logo_icon_name(program_icon_name)
    aboutdialog.set_transient_for(win)
    aboutdialog.run()
    aboutdialog.destroy()

def show_notification(message):
    Notify.init('GEncrypter')
    notification = Notify.Notification.new('GEncrypter', message, program_icon_name)
    notification.show()

def scale(cur, res, num):
# Default Settings
    cur = int(cur)
    res = int(res)
    num = str(num)
    inmode = 0
    outmode = 0
    error = False
    CapsFlag = True
    Defined = True
    Float = False
    Positive = True

    # Input
    if cur > 62 or res > 62: Defined = False
    if num.count('.') == 1:
        Float =True
    if num.count('-') == 1:
        Positive = False
        num = str(num)[1:]
    if cur > 36: inmode = 1
    if res > 36: outmode = 1
    bak = str(num)
    num = 0
    numofdigits = count(bak)

    if inmode == 1:
        for i in range(0, numofdigits):
            try: digitnum = ord(bak[i])
            except: error = True
            if digitnum >= 65 and digitnum <= 91:
                digit = digitnum - 29
            elif digitnum >= 97 and digitnum <= 122:
                digit = digitnum - 87
            else: digit = int(chr(digitnum))
            if digit >= cur: error = True
            num += digit*int(cur)**(n-i-1)
            num = int(num)
            digitnum = 0
            digit = 0
    else:
        for i in range(0, numofdigits):
            try: digitnum = ord(bak[i])
            except: error = True
            if digitnum >= 97 and digitnum <= 122:
                digit = digitnum - 87
            else: digit = int(chr(digitnum))
            if digit >= cur: error = True
            num += digit*int(cur)**(numofdigits-i-1)
            num = int(num)
            digitnum = 0
            digit = 0

    # Output
    if res != 10:
        strdigit = ''
        for i in range(1, 17):
            if int(res)**i > num:
                numofdigits = i
                break
        digit = 0
        if outmode == 1:
            for i in range(1, numofdigits + 1):
                digit = num%int(res)
                digitnum = digit
                if digit >= 10 and digit <= 35:
                    digitnum = chr(int(digit + 87))
                if digit >= 36 and digit <= 61:
                    digitnum = chr(int(digit + 29))
                strdigit = str(digitnum) + strdigit
                num = int(floor(num/int(res)))
            num = strdigit
        else:
            for i in range(1, numofdigits + 1):
                digit = num%int(res)
                digitnum = digit
                if digit >= 10 and digit <= 35:
                    digitnum = chr(int(digit + 87))
                strdigit = str(digitnum) + strdigit
                num = int(floor(num/int(res)))
            num = strdigit
    if error == True:
        raise Exception("ERROR")
    if error == False and Defined == True:
        if Positive == False:
            num = '-' + str(num)
        return num

def count(iterable):
    if type(iterable) == type(2):
        iterable = str(iterable)
    count = 0
    for i in iterable:
        count += 1
    return int(count)

def reverse(string):
    List = list(str(string))
    List.reverse()
    reversedd = ''.join(List)
    return reversedd

def encrypter(string, mode):
    try:
        startTime = str(int(time.time()*1000))
        part1 = startTime[10:13]
        part2 = string
        part3 = int(round(random()*100))
        part4 = startTime[0:5]
        part5 = int(round(random()*10))
        if part5 == 0: part5 = 10
        part6 = startTime[5:10]
        
        ectpart1 = scale(10, 15, reverse(part1))
        ectpart2 = uc3(part2, part1, part4)
        ectpart3 = scale(10, 3, part3)
        ectpart4 = reverse(scale(10, 36, (int(part4) + 15 - int(ectpart3))))
        ectpart5 = scale(10, 9, part5)
        ectpart6 = reverse(scale(10, 35, (int(part6) - 15*part5)))

        retn = '~'
        if mode == 'Normal':
            retn += ectpart1 + 'n' + '!'
        if mode == 'Hex':
            retn += ectpart1 + '!'
        retn += ectpart2 + '!'
        retn += ','.join((ectpart3, ectpart4, ectpart5, ectpart6))
        endTime = int(time.time()*1000)
        TimeUsed = int(endTime) - int(startTime)
        return retn, TimeUsed
    except:
        pass

def decrypter(code, checksum):
    try:
        startTime = int(time.time()*1000)
        code = code[1:].split('!')
        if code[0][-1] == 'h'\
        or code[0][-1] == 'n':
            code[0] = code[0][:-1]
            
        part2 = code[1]
        part36 = code[2].split(',');

        dctpart1 = reverse(int(code[0], 15))
        dctpart3 = int(part36[0], 3)
        dctpart4 = int(reverse(part36[1]), 36) - 15 + int(part36[0])
        dctpart5 = int(part36[2])
        dctpart6 = int(reverse(part36[3]), 35) + (15*dctpart5)
        dctpart2 = un3(part2, dctpart1, dctpart4)
        
        endTime = int(time.time()*1000)
        needtime = endTime - startTime
        retn = dctpart2
        if not checksum:
            ecttime = str(dctpart4) + str(dctpart6) + str(dctpart1)
            tc = time.ctime(float(ecttime[0:10])).split(' ')
            date = ' '.join((tc[4], tc[1], tc[2], tc[3]))
            retn = dctpart2, date, needtime
        return retn
    except:
        pass

def hexencrypter(code):
	try:
		string = code.split('!')
		code1 = string[0]
		code3 = string[2]
		stringlist = string[1].split(',')
		hexcode = ''
		for HEX in stringlist:
			hexcode += '÷'
			if HEX[0] == '-':
				hexcode += '-'
				HEX = HEX[1:]
			if count(HEX) % 2 == 1:
				HEX = '0' + HEX
			for i in range(0, count(HEX), 2):
				hexcode += chr(int(HEX[i:i+2], 16))
		hexcode = hexcode[1:]
		code1 += 'h'
		result = '!'.join((code1, hexcode, code3))
		return result
	except:
		pass

def hexdecrypter(hcode):
	try:
		hexcode = hcode.split('!')
		code1 = hexcode[0][:-1]
		code3 = hexcode[2]
		HEXlist = hexcode[1].split('÷')
		string = ''
		for HEX in HEXlist:
			string += ','
			if HEX[0] == '-':
				string += '-'
				HEX = HEX[1:]
			for i in HEX:
				string += hex(ord(i))[2:]
		string = string[1:]
		result = '!'.join((code1, string, code3))
		return result
	except:
		pass

def uc3(this, utc, it):
    retn = ''
    utc = int(utc)
    it = int(it)
    n = count(this)
    for i in range(n):
        if i%2 != 0:
            retn += str(scale(10, 15, str(ord(this[i]) + int(utc) - int(i)))) + ','
        else:
            retn += str(scale(10, 12, str(ord(this[i]) - int(it) + int(i)))) + ','

    retn = retn[0:-1];
    return retn

def un3(this, utc, it):
    retn = ''
    utc = int(utc)
    it = int(it)
    tmmp = this.split(',')
    for i in range(count(tmmp)):
        if i%2 != 0:
            retn += chr(int(tmmp[i], 15) - utc + int(i))
        else:
            retn += chr(int(tmmp[i], 12) + int(it) - i)
    return retn

def set_text_mono(label, text):
    label.set_markup('<span font="Ubuntu Mono 12">%s</span>' % text)

def encrypt(button, self):
    text_start, text_end = self.TextBox_buffer.get_bounds()
    Text = self.TextBox_buffer.get_text(text_start, text_end, True)
    if Text == ''\
    or Text == '\n'\
    or Text == ' ':
        cleartext(None, self, False)
        set_text_mono(self.StrVarMsg, liblang.Msg_ERR)
    else:
        ect_str = encrypter(Text, omode)
        ect_str = ect_str[0]
        needtime = ect_str[1]
        dct_str = decrypter(ect_str, True)
        if dct_str != Text:
            cleartext(None, self, False)
            set_text_mono(self.StrVarStat, liblang.Msg_Stat_Enc[0])
        else:
            if omode == 'Hex':
                ect_str = hexencrypter(ect_str)
            cleartext(None, self, False)
            set_text_mono(self.StrVarStat, liblang.Msg_Stat_Enc[1])
            set_text_mono(self.StrVarTimeUsed, str(needtime) + liblang.Time_Encryption)
            self.TextBox_buffer.set_text(ect_str)
            clipboard_callback(None, 'auto_copy', self)

def decrypt(button, self):
    text_start, text_end = self.TextBox_buffer.get_bounds()
    ect_str = self.TextBox_buffer.get_text(text_start, text_end, True)
    if ect_str == ''\
    or ect_str == '\n'\
    or ect_str == ' '\
    or ect_str[0] != '~':
        cleartext(None, self, True)
        set_text_mono(self.StrVarMsg, liblang.Msg_ERR)
    else:
        flag = ect_str.split('!')[0][-1]
        if flag == 'h':
            midect_str = hexdecrypter(ect_str)
            Text = decrypter(midect_str, False)
        else:
            Text = decrypter(ect_str, False)
        if type(Text) == type(('2',)):
            cleartext(None, self, False)
            self.TextBox_buffer.set_text(Text[0])
            set_text_mono(self.StrVarStat, liblang.Msg_Stat_Dec[1])
            set_text_mono(self.StrVarMsg, liblang.Time_Encrypted + Text[1])
            set_text_mono(self.StrVarTimeUsed, str(Text[2]) + liblang.Time_Encryption)
            clipboard_callback(None, 'auto_copy', self)
        else:
            cleartext(None, self, False)
            set_text_mono(self.StrVarStat, liblang.Msg_Stat_Dec[0])

def cleartext(button, self, not_with_text):
    self.StrVarStat.set_text('')
    self.StrVarMsg.set_text('')
    self.StrVarTimeUsed.set_text('')
    if not_with_text == False:
        self.TextBox_buffer.set_text('')

def about(button=None, self=None):
    cleartext(None, self, False)
    self.TextBox_buffer.set_text(liblang.ABOUT.__doc__)

class Default():
    lang = 'en_US'
    mode = 'Normal'
