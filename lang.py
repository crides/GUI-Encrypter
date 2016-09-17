#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-

class en_US:
    title = "Encrypter" 
    
    notification = "Program Started!"
    
    msg_err_gen = "There is an Error."
    msg_err_unk = "Unknown encrypted code."
    msg_err_met = "Unknown method: %s"
    msg_met_nava = "No methods avaliable."
    msg_stat_enc = ["Encryption Failed.", "Encryption Succeeded."]
    msg_stat_dec = ["Decryption Failed.", "Decryption Succeeded."]
    
    time_encryption = "%dms"
    time_encrypted = "Encrypted on: "
    
    lbl_label = ["TextBox", "Status", "Message", "Time Used"]
    lbl_btn = ["E_ncrypt", "_Decrypt", "_Clear", "About"]
    lbl_set_frm = ["Language", "Encoding", "Methods", "Extra"]
    lbl_no_ext = "No extras available."
    
    tooltip = ["Text Box for Encryption and Decryption", "Indicate the status of the Encrypter", "For extra output messages like Error", "Time usage of the process", "Encrypt Text", "Decrypt Text", "Clear Status & Text", "Show About Text", "Methods used to encrypt and decrypt", "Refresh available methods"]
    
    abt_comment = "Encrypt your texts and strings"
    
    about = \
"""This is a program which is used to encrypt and decrypt strings written by Zhu Haoqing. The Program is originally written by zhangjingye (Github: zhangjingye03) in JavaScript, translated by zhuhaoqing (Github: Irides-Chromium) into Python3. The Program can only decrypt strings which were encrypted by (any branches, or the original web version by Zhang Jingye) this program.
CopyRight (C) 2014 ~ 2016
All Rights Reserved.

Author: <zjy@sugus>
Translater: <zhuhaoqing@live.cn>
Version 5.0

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

This program is written by:
Zhang Jingye.
And translated by:
Zhu Haoqing
"""
    
    help = \
"""This is the Help of the Encrypter. Enter text or cipher into the Text Box and encrypt or decrypt.
Press Escape to close the program.
Press F1 to show this help.
You can also use the mnemonic keys (Alt+n/d/c) to activate the buttons."""
    
    menu_edit = "Edit"
    menu_help = "Help"
    menu_edit_ = ["Copy", "Cut", "Paste", "Select all", "Preference"]

    set_note = "Note: You should restart the program to apply the change.\n注意：您应重启程序来应用选项"
    
class zh_CN:
    title = "加密器"
    
    notification = "程序启动！"
    
    msg_err_gen = "程序出错"
    msg_err_met = "未知方法: %s"
    msg_err_unk = "未知加密字符串"
    msg_met_nava = "无可用方法"
    msg_stat_enc = ["加密失败", "加密成功"]
    msg_stat_dec = ["解密失败", "解密成功"]
    
    time_encryption = "%d毫秒"
    time_encrypted = "此时被加密："
    
    lbl_label = ["文本框", "状态", "信息", "耗时"]
    
    lbl_btn = ["加密(_n)", "解密(_d)", "清除(_c)", "关于"]
    lbl_set_frm = ["语言", "编码", "方法", "附加"]
    lbl_no_ext = "没有可用的附加选项。"
    
    tooltip = ["加密与解密用的文本框", "显示加密器的状态", "用于像错误等更多的信息", "过程耗时", "加密文字", "解密文字", "清除状态和文字", "显示关于", "加密与解密用的方法", "刷新方法"]
    
    abt_comment = "加密你的字符串"
    about = \
"""这是一个由 Zhu Haoqing 编写的用于加密和解密字符串的程序。这个程序原本由 zhangjingye (Github: zhangjingye03) 用JavaScript编写，由 Zhu Haoqing (Github: Irides-Chromium) 翻译成为 Python3。本程序只能解密由(任意分支或原网页版的)本程序加密的字符串。
版权所有(C) 2014 ~ 2016
作者： <zjy@sugus>
翻译： <zhuhaoqing@live.cn>
版本： 5.0

本程序是免费的软件；您可以在自由软件基金会(即Free Software Foundation)发行的通用公共许可证 (GNU General Public Lisence) 的条件下重新发行和/或更改它；可以是版本2.0，或者(按您的选择)任何之后的版本。
本程序是为了希望它有用而发布的，但没有任何担保；甚至没有对(它的)可销售性或特定目的的适应性。详见GNU General Public License。
您应该与本程序一并收到了一份通用公共许可证；如果没有，应写信到自由软件基金会公司，美国，麻州02110-1301，波士顿，富兰克林街51号5层。

本程序由Zhang Jingye编写
并由Zhu Haoqing转译
"""
    
    help = \
"""这是本加密器的帮助。将文本或密码输入到文本框中然后加密或解密。
按Esc来结束本程序，按F1来显示本帮助。
您也可以用快捷键(Alt+n/d/c)来激活各个按钮。"""
    
    menu_edit = "编辑"
    menu_help = "帮助"
    menu_edit_ = ["拷贝", "剪切", "粘帖", "全选", "选项"]

    set_note = "Note: You should restart the program to apply the change.\n注意：您应重启程序来应用选项"
