from scale import scale
from time import time, ctime

extra = {}
accept_set = True

class tape(list):

    def __init__(self, iterable=None):
        super().__init__(iterable)
        self.ptr = 0

    def get(self, l=1):
        self.ptr += l
        return "".join(self[self.ptr - l:self.ptr])

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

def encrypt(string, _set):
    from random import randint
    #string = string.encode()        # To UTF-8
    _string = tape(string)

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
    while _string.ptr < len(_string):
        val = FF2A(_string.get(randint(1, 6)))
        base = randint(16, 64)
        enc = scale(10, base, key + val)
        enc_str += temp.format(b=scale(10, 64, base - 1), l=len(enc), v=enc)

    return ''.join((enc_time, enc_str, hex(hash(string)).strip("-")[2:]))

def decrypt(code, _set):
    code = tape(code)
    dec_time = []
    for i in range(4):
        base = int(scale(64, 10, code.get())) + 1
        length = int(code.get())
        enc = code.get(length)
        dec_time.append(scale(base, 10, enc))
    mul = int(scale(64, 10, code.get())) - 10
    order = code.get(4)
    key = int(dec_time[-1]) * mul
    for i, o_i in zip(order[::-1], range(4)):
        dec_time.insert(int(i), dec_time.pop())

    dec_str = ""
    while not code[code.ptr].isdigit():
        base = int(scale(64, 10, code.get())) + 1
        length = int(code.get())
        enc = code.get(length)
        dec_str += A2FF(int(scale(base, 10, enc)) - key)
    _hash = code.get(16)
    if _hash != hex(hash(dec_str)).strip("-")[2:]:
        print(dec_str, hex(hash(dec_str)).strip("-")[2:], _hash)
        raise ValueError("Hash match failed.")
    date = ctime(int("".join(dec_time[:3]))).split()
    date = " ".join((date[4], *date[1:4]))
    return dec_str, date
