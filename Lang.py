#!/usr/bin/python3.4

class en_US():
    Title = 'GEncrypter' 
    
    notification = 'Program Started!'
    
    Msg_ERR = 'There is an Error.'
    Msg_Stat_Enc = ['Encryption Failed.', 'Encryption Succeeded.']
    Msg_Stat_Dec = ['Decryption Failed.', 'Decryption Succeeded.']
    
    Time_Encryption = 'ms'
    Time_Encrypted = 'Encrypted on: '
    
    Lbl_Label = ['TextBox', 'Status', 'Message', 'Time Used']
    Lbl_set_Label = ['Language', 'Mode', 'Normal', 'Hexage']
    
    Lbl_Btn = ['E_ncrypt', '_Decrypt', '_Clear', 'About']
    Lbl_set_Btn = ['Apply', 'Close']
    
    Tooltip = ['Text Box for Encryption and Decryption', 'Indicate the status of the Encrypter', 'For extra output messages like Error', 'Time usage of the process', 'Encrypt Text', 'Decrypt Text', 'Clear Status & Text', 'Show About Text']
    
    Abt_Comment = 'Encrypt your texts and strings'
    
    def ABOUT():
        '''This is a program which is used to encrypt and decrypt strings written by Zhu Haoqing. The Program is originally written by zhangjingye (Github: zhangjingye03) in JavaScript, translated by zhuhaoqing (Github: Irides-Chromium) into Python3. The Program can only decrypt strings which were encrypted by (any branches, or the original web version by Zhang Jingye) this program.
CopyRight (C) 2014 ~ 2016
All Rights Reserved.

Author: <zjy@sugus>
Translater: <zhuhaoqing@live.cn>
Version 4.0

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

This program is written by:
Zhang Jingye.
And translated by:
Zhu Haoqing
'''
    
    def HELP():
        '''This is the Help of the Encrypter. Enter text or cipher into the Text Box and encrypt or decrypt.
Press Escape to close the program.
Press F1 to show this help.
You can also use the mnemonic keys (Alt+n/d/c) to activate the buttons.'''
    
    Menu_Edit = 'Edit'
    Menu_Help = 'Help'
    Menu_Edit_ = ['Copy', 'Cut', 'Paste', 'Select all', 'Preference']

    set_Note = 'Note: You should restart the program to apply the change.\n注意：您应重启程序来应用选项'
    
class zh_CN():
    Title = '加密器'
    
    notification = '程序启动！'
    
    Msg_ERR = '程序出错'
    Msg_Stat_Enc = ['加密失败', '加密成功']
    Msg_Stat_Dec = ['解密失败', '解密成功']
    
    Time_Encryption = '毫秒'
    Time_Encrypted = '此时被加密：'
    
    Lbl_Label = ['文本框', '状态', '信息', '耗时']
    Lbl_set_Label = ['语言', '模式', '普通', '十六进制']
    
    Lbl_Btn = ['加密(_n)', '解密(_d)', '清除(_c)', '关于']
    Lbl_set_Btn = ['应用', '关闭']
    
    Tooltip = ['加密与解密用的文本框', '显示加密器的状态', '用于像错误等更多的信息', '过程耗时', '加密文字', '解密文字', '清除状态和文字', '显示关于']
    
    Abt_Comment = '加密你的字符串'
    def ABOUT():
        '''这是一个由 Zhu Haoqing 编写的用于加密和解密字符串的程序。这个程序原本由 zhangjingye (Github: zhangjingye03) 用JavaScript编写，由 Zhu Haoqing (Github: Irides-Chromium) 翻译成为 Python3。本程序只能解密由(任意分支或原网页版的)本程序加密的字符串。
版权所有(C) 2014 ~ 2016
作者： <zjy@sugus>
翻译： <zhuhaoqing@live.cn>
版本： 4.0

本程序是免费的软件；您可以在自由软件基金会(即Free Software Foundation)发行的通用公共许可证 (GNU General Public Lisence) 的条件下重新发行和/或更改它；可以是版本2.0，或者(按您的选择)任何之后的版本。
本程序是为了希望它有用而发布的，但没有任何担保；甚至没有对(它的)可销售性或特定目的的适应性。详见GNU General Public License。
您应该与本程序一并收到了一份通用公共许可证；如果没有，应写信到自由软件基金会公司，美国，麻州02110-1301，波士顿，富兰克林街51号5层。

本程序由Zhang Jingye编写
并由Zhu Haoqing转译
'''
    
    def HELP():
        '''这是本加密器的帮助。将文本或密码输入到文本框中然后加密或解密。
按Esc来结束本程序，按F1来显示本帮助。
您也可以用快捷键(Alt+n/s/c)来激活各个按钮。'''
    
    Menu_Edit = '编辑'
    Menu_Help = '帮助'
    Menu_Edit_ = ['拷贝', '剪切', '粘帖', '全选', '选项']

    set_Note = 'Note: You should restart the program to apply the change.\n注意：您应重启程序来应用选项'
