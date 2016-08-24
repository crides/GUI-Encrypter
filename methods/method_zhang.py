#!/usr/bin/python3
from scale import scale

def encrypt(string, _set):
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

    retn = "~" + ectpart1 + "!" + ectpart2 + "!"
    retn += ",".join((ectpart3, ectpart4, ectpart5, ectpart6))
    time_used = int(time() * 1000) - int(start_time)
    return retn, time_used

def decrypt(code, _set):
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
    ecttime = str(dctpart4) + str(dctpart6) + str(dctpart1)
    tc = ctime(float(ecttime[0:10])).split()
    date = " ".join((tc[4], tc[1], tc[2], tc[3]))
    return dctpart2, date, needtime

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
        if i % 2 != 0: retn += scale(10, 15, ord(this[i]) + utc - i) + ","
        else:          retn += scale(10, 12, ord(this[i]) - it + i) + ","
    return retn[0:-1]

def utf_uc3(this, utc, it):
    retn = ""
    this = this.encode()
    for i in range(len(this)):
        if i % 2 != 0: retn += scale(10, 15, this[i] + utc - i) + ","
        else:          retn += scale(10, 12, this[i] - it + i) + ","
    return retn[0:-1]

def uni_un3(this, utc, it):
    retn = ""
    tmmp = this.split(",")
    for i in range(len(tmmp)):
        if i % 2 != 0: retn += chr(int(tmmp[i], 15) - utc + i)
        else:          retn += chr(int(tmmp[i], 12) + it - i)
    return retn

def utf_un3(this, utc, it):
    retn = []
    tmmp = this.split(",")
    for i in range(len(tmmp)):
        if i % 2 != 0: retn.append(int(tmmp[i], 15) - utc + i)
        else:          retn.append(int(tmmp[i], 12) + it - i)
    return bytes(retn).decode()
