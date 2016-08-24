from scale import scale
from time import time, ctime
class s_tape(str):

    def __init__(self, iterable=None):
        self.ptr = 0

    def get(self, i=-1, l=1):
        i = self.ptr if i == -1 else i
        self.ptr += l
        return self[i:i + l]

def A2FF(num):
    result = ""
    while num > 0:
        result = chr(num % 256) + result
        num //= 256
    return result

def FF2A(string):
    result = 0
    unit = 1
    for i in string[::-1]:
        result += ord(i) * unit
        unit *= 256
    return result

def zhu_encrypt(string):
    from random import randint
    #string = string.encode()        # To UTF-8
    string = s_tape(string)

    # Time encryption
    cur_time = str(int(time() * 1000))
    while int(cur_time[10:13]) < 9: cur_time = str(int(time() * 1000))
    _ = lambda a,b: cur_time[a:b]
    time_parts = [_(0, 3), _(3, 7), _(7, 10), _(10, 13)]
    del _
    enc_time = ""
    enc_time_order = ""
    for i in range(3, -1, -1):
        index = randint(0, i)
        time_parts.append(time_parts.pop(index))
        enc_time_order += str(index)
    temp = "{b}{l}{v}"              # Base, length, value
    for i in time_parts:
        base = randint(16, 64)
        enc = scale(10, base, i)
        enc_time += temp.format(b=scale(10, 64, base - 1), \
                l=len(enc), v=enc)
    key = int(time_parts[-1])
    mul = (256 // key) + 1
    enc_time += scale(10, 64, 10 + mul) + enc_time_order

    # String encryption
    key *= mul
    enc_str = ""
    while string.ptr < len(string):
        val = FF2A(string.get(l=randint(1, 6)))
        base = randint(16, 64)
        enc = scale(10, base, key + val)
        enc_str += temp.format(b=scale(10, 64, base - 1), l=len(enc), v=enc)

    return ''.join((enc_time, enc_str, hex(hash(string)).strip("-")[2:]))

def zhu_decrypt(code):
    code = s_tape(code)
    dec_time = []
    for i in range(4):
        base = int(scale(64, 10, code.get())) + 1
        length = int(code.get())
        enc = code.get(l=length)
        dec_time.append(scale(base, 10, enc))
    mul = int(scale(64, 10, code.get())) - 10
    order = code.get(l=4)
    key = int(dec_time[-1]) * mul
    for i, o_i in zip(order[::-1], range(4)):
        dec_time.insert(int(i), dec_time.pop())

    dec_str = ""
    while not code[code.ptr].isdigit():
        base = int(scale(64, 10, code.get())) + 1
        length = int(code.get())
        enc = code.get(l=length)
        dec_str += A2FF(int(scale(base, 10, enc)) - key)
    _hash = code.get(l=16)
    if _hash != hex(hash(dec_str)).strip("-")[2:]:
        raise Exception("Decryption Failed.")
    date = ctime(int("".join(dec_time[:3]))).split()
    date = " ".join((date[4], *date[1:4]))
    return dec_str, date
