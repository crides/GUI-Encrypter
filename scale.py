#!/usr/bin/python3

def scale(cur, res, num):
# Default Settings
    num = str(num)
    error = False
    defined = positive = True

    # Input
    if cur not in range(2, 37) or res not in range(2, 37): defined = False
    if num.count("-") == 1:
        positive = False
        num = num[1:]
    result = 0
    unit = 1

    if cur != 10:
        for i in num[::-1]:
            value = ord(i)
            if value in range(48, 58): value -= 48
            elif value in range(97, 123): value -= 87
            elif value in range(65, 92): value -= 55
            if value >= cur: error = True
            result += value * unit
            unit *= cur

    # Output
    if res != 10:
        num = int(result or num)
        result = ""
        while num > 0:
            value = num % res
            if value < 10: digit = value + 48
            elif value <= 35: digit = value + 87
            result = chr(digit) + result
            num //= res
    if error: raise Exception("ERROR")
    elif defined:
        if not positive: result = "-" + str(result)
        return result
