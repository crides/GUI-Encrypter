import time
from math import floor
from random import random

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

def reverse(string):
    string = str(string)
    l = list(string)
    l.reverse()
    s = ''.join(l)
    return s

def encrypter(string):
##    try:
        ret = '~'
        d = str(int(time.time()*1000))
        part2 = d[10:13]
        p2 = scale(10, 15, reverse(part2))
        part4 = string;
        part6 = int(round(random()*100))
        p6 = scale(10, 3, part6)
        part7 = d[0:5]
        p7 = reverse(scale(10, 36, (int(part7) + 15 - int(p6))))
        part8 = int(round(random()*10));
        if part8 == 0: part8 = 10
        p8 = scale(10, 9, part8)
        part9 = d[5:10]
        p9 = reverse(scale(10, 35, (int(part9) - 15*part8)))
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

def decrypter(string, checksum):
##    try:
        fT = int(time.time()*1000)
        string = string[1:-1]
        string = string.split('!')
        part2 = reverse(int(string[0], 15))
        part69 = string[2].split(',');
        part6 = int(part69[0], 3)
        part7 = int(reverse(part69[1]), 36) - 15 + int(part69[0])
        part8 = int(part69[2])
        part9 = reverse(part69[3])
        part9 = int(part9, 35) + (15*part8)
        part4 = string[1]
        part4 = un3(part4, part2, part7);
        lT = int(time.time()*1000)
        needtime = lT - fT
        retn = part4
        if not checksum:
            ectime = str(part7) + str(part9) + str(part2)
            tc = time.ctime(float(ectime[0:10])).split(' ')
            date = tc[4] + ' ' + tc[1] + ' ' + tc[2] + ' ' + tc[3]
            retn = part4, date, needtime
        return retn

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
            retn += chr(int(int(tmmp[i], 15) - utc + int(i)))
        else:
            retn += chr(int(tmmp[i], 12) + int(it) - i)
    return retn

class Default():
    lang = 'en_US'
    mode = 'normal'
