#!/usr/bin/python3

#from scale import scale
from scale_strict import scale
from time import time, ctime
import os

extra = {}
accept_set = True

xhash = lambda a: os.popen("./hashx '%s'" % str(a)).read()[:-1]

class tape(list):

    def __init__(self, iterable=None):
        super().__init__(iterable)
        self.typ = type(iterable)
        self.ptr = 0

    def get(self, l=1):
        self.ptr += l
        if self.typ == list: return self[self.ptr - l:self.ptr]
        else: return "".join(self[self.ptr - l:self.ptr])

def A2FF(num):
    result = []
    while num > 0:
        result = [num % 256] + result
        num //= 256
    return result
    #return "".join([chr(i) for i in result])
    #return bytearray(result).decode()

def FF2A(l):
    result = 0
    unit = 1
    for i in l[::-1]:
        result += i * unit
        unit *= 256
    return result

def enc_blv(value):
    base = randint(16, 64)
    value = scale(10, base, value)
    length = len(value)
    return scale(10, 64, base) + length + value

def dec_blv(string):
    base = int

def encrypt(string, _set):
    from random import randint
    _string = tape(list(string.encode()))         # To UTF-8

    # Time encryption
    cur_time = str(int(time() * 1000))
    while int(cur_time[10:13]) < 9: cur_time = str(int(time() * 1000))
    _ = lambda a,b: cur_time[a:b]
    time_parts = [_(0, 3), _(3, 7), _(7, 10), _(10, 13)]
    del _
    enc_time = ""
    enc_time_order = ""
    key = 0
    for i in range(3, -1, -1):
        index = randint(0, i)
        enc_time_order += str(index)
        base = randint(16, 64)
        key = time_parts.pop(index)
        enc = scale(10, base, key)
        enc_time += scale(10, 64, base - 1) + str(len(enc)) + enc
    key = int(key)
    mul = (256 // key) + 1
    enc_time += scale(10, 64, 10 + mul) + enc_time_order

    # String encryption
    key *= mul
    print("enc::key::", key)
    enc_str = ""
    while _string.ptr < len(_string):
        val = FF2A(_string.get(randint(1, 6)))
        base = randint(16, 64)
        enc = scale(10, base, key + val)
        print("enc::(b l v) %s(%d) %s(%d) %s(%d)" % (\
                scale(10, 64, base - 1),
                base,
                scale(10, 64, len(enc)),
                len(enc),
                enc,
                key + val))
        enc_str += scale(10, 64, base - 1) + scale(10, 64, len(enc)) + enc

    return ''.join((enc_time, enc_str, xhash(string))), len(enc_str)

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

    dec_str = []
    while not code[code.ptr].isdigit():
        _base = code.get()
        base = int(scale(64, 10, _base)) + 1
        _length = code.get()
        length = int(scale(64, 10, _length))
        _dec = code.get(length)
        dec = int(scale(base, 10, _dec))
        print("dec::(b l v) %s(%d) %s(%d) %s(%d)" % (\
                _base,
                base,
                _length,
                length,
                _dec,
                dec))
        dec_str += A2FF(dec - key)
    dec_str = bytearray(dec_str).decode()
    _hash = code.get(16)
    if _hash != xhash(dec_str):
        print(dec_str, xhash(dec_str), _hash)
        raise ValueError("Hash match failed.")
    date = ctime(int("".join(dec_time[:3]))).split()
    date = " ".join((date[4], *date[1:4]))
    return dec_str, date
