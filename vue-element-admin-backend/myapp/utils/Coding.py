# -*- utf-8 -*-
# @Time: 2021/5/5 23:06
# @Author: CACode
# @File: Coding.py
# @Software: PyCharm


def HexStrToBytes(text):
    return bytes.fromhex(text)


def BytesToHexStr(text):
    """
    字节转hex字符串
    :param text:
    :return:
    """
    return text.hex()
