
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

    # From
    if cur > 62 or res > 62: Defined = False
    if num.count('.') == 1:
        Float =True
    if num.count('-') == 1:
        Positive = False
        num = str(num)[1:]
    if cur > 36: inmode = 1
    if res > 36: outmode = 1
    l = str(num)
    num = 0
    n = count(l)

    if inmode == 1:
        for i in range(0, n):
            try: b = ord(l[i])
            except: error = True
            if b >= 65 and b <= 91:
                a = b - 29
            elif b >= 97 and b <= 122:
                a = b - 87
            else: a = int(chr(b))
            if a >= cur: error = True
            num += a*int(cur)**(n-i-1)
            num = int(num)
            b = 0
            a = 0
    else:
        for i in range(0, n):
            try: b = ord(l[i])
            except: error = True
            if b >= 97 and b <= 122:
                a = b - 87
            else: a = int(chr(b))
            if a >= cur: error = True
            num += a*int(cur)**(n-i-1)
            num = int(num)
            b = 0
            a = 0

    # To
    if res != 10:
        s = ''
    for i in range(1, 17):
        if int(res)**i > num:
            n = i
        break
    a = 0
    if outmode == 1:
        for i in range(1, n+1):
            a = num%int(res)
            b = a
            if a >= 10 and a <= 35:
                b = chr(int(a + 87))
            if a >= 36 and a <= 61:
                b = chr(int(a + 29))
            s = str(b) + s
            num = int(floor(num/int(res)))
            num = s
    else:
        for i in range(1, n+1):
            a = num%int(res)
            b = a
            if a >= 10 and a <= 35:
                b = chr(int(a + 87))
            s = str(b) + s
            num = int(floor(num/int(res)))
            num = s
    if error == True:
        return 'ERROR'
    if error == False and Defined == True:
        if Positive == False:
            num = '-' + str(num)
    return num

def count(string):
    if type(string) == type(2):
        string = str(string)
    count = 0
    for i in string:
        count += 1
    return int(count)

def cleartext():
    TextStatus.set('')
    Message.set('')
    TimeUsed.set('')
    TextBox.delete('1.0', 'end')


def reverse(string):
    string = str(string)
    l = list(string)
    l.reverse()
    s = ''.join(l)
    return s

def encrypt(*args):
    Text = TextBox.get('1.0', 'end')
    if Text == '' or Text == '\n' or Text == ' ':
        Message.set(liblang.Msg_ERR)
    uText = Text.encode('utf-8')
    bak = Text
    jmh = encrypter(Text)
    Text = jmh[0]
    needtime = jmh[1]
    ol = decrypter(Text, True)
    dct = ol
    if dct != bak:
        TextStatus.set(liblang.Msg_Stat_Enc[0])
    else:
        cleartext()
        TextStatus.set(liblang.Msg_Stat_Enc[1])
        TimeUsed.set(str(needtime) + liblang.Time_Encryption)
        TextBox.insert('1.0', Text)

def encrypter(string):
##    try:
        ret = '~'
        d = str(int(time.time()*1000))
        part2 = d[10:13]
        p2 = scale(10, 25, reverse(part2))
        part4 = string;
        part6 = int(round(random()*100))
        p6 = scale(10, 3, part6)
        part7 = d[0:5]
        p7 = reverse(scale(10, 36, (int(part7) + 25 - int(p6))))
        part8 = int(round(random()*10));
        if part8 == 0: part8 = 10
        p8 = scale(10, 9, part8)
        part9 = d[5:10]
        p9 = reverse(scale(10, 35, (int(part9) - 25*part8)))
        p4 = uc3(part4, part2, part7)
        ret += p2 +'!'
        ret += p4 +'!'
        ret += p6 + ','
        ret += p7 + ','
        ret += p8 + ','
        ret += p9
        lastTime = int(time.time()*1000)
        TimeUsed = int(lastTime) - int(d)
        return ret, TimeUsed
##    except:
##        e = Exception()
##        return e

def decrypt(*args):
    Text = TextBox.get('1.0', 'end')
    if Text == '' or Text == '\n' or Text == ' ' or Text[0] != '~':
        Message.set(liblang.Msg_ERR)
    Text = decrypter(Text, False)
    if type(Text) == type(('2',)):
        cleartext()
        TextBox.insert('1.0', Text[0])
        TextStatus.set(Text[1])
        Message.set(Text[2])
        TimeUsed.set(str(Text[3]) + liblang.Time_Encryption) 
    else:
        TextStatus.set(liblang.Msg_Stat_Dec[0])

def decrypter(string, checksum):
##    try:
        fT = int(time.time()*1000)
        string = string[1:-1]
        string = string.split('!')
        part2 = reverse(int(string[0], 25))
        part69 = string[2].split(',');
        part6 = int(part69[0], 3)
        part7 = int(reverse(part69[1]), 36) - 25 + int(part69[0])
        part8 = int(part69[2])
        part9 = reverse(part69[3])
        part9 = int(part9, 35) + (25*part8)
        part4 = string[1]
        part4 = un3(part4, part2, part7);
        lT = int(time.time()*1000)
        needtime = lT - fT
        retn = part4
        if not checksum:
            ectime = str(part7) + str(part9) + str(part2)
            tc = time.ctime(float(ectime[0:10])).split(' ')
            date = tc[4] + ' ' + tc[1] + ' ' + tc[2] + ' ' + tc[3]
            texts = liblang.Msg_Stat_Dec[1]
            msg = liblang.Time_Encrypted + date
            retn = part4, texts, msg, needtime
        return retn

def uc3(this, utc, it):
    retn = ''
    utc = int(utc)
    it = int(it)
    n = count(this)
    for i in range(n):
        if i%2 != 0:
            retn += str(scale(10, 25, str(ord(this[i]) + int(utc) - i))) + ','
        else:
            retn += str(scale(10, 26, str(ord(this[i]) - int(it) + int(i)))) + ','

    retn = retn[0:-1];
    return retn

def un3(this, utc, it):
    retn = ''
    utc = int(utc)
    it = int(it)
    tmmp = this.split(',')
    for i in range(count(tmmp)):
        if i%2 != 0:
            retn += chr(int(int(tmmp[i], 25) - utc + int(i)))
        else:
            retn += chr(int(tmmp[i], 26) + int(it) - i)
    return retn

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

class Default():
    lang = 'en_US'
    mode = 'normal'

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
