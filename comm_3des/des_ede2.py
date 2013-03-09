#!/usr/bin/env python
#coding=utf-8

import os
import sys
from mylib import *
import MyGlobal

class ede2(object):
    def __init__(self, key1, key2, data):
        self.key1 = key1
        self.key2 = key2
        self.data = data
    
    def encrypt(self):
        #key1,En
        MyGlobal.FLAG_3=0
        MyGlobal.FLAG_F=1
        MyGlobal.MODE = 1
        MyGlobal.KEY = self.key1
        MyGlobal.CIPHERTEXT = self.getResult(self.data)
        print "\nkey1加密结果:\n"+myFile().showFile(MyGlobal.FILENAME,1)
        #MyGlobal.CIPHERTEXT = self.getAsciiResult(MyGlobal.CIPHERTEXT)
        #print MyGlobal.CIPHERTEXT
        #key2,De
        MyGlobal.FLAG_F=0
        MyGlobal.FLAG_3=0
        MyGlobal.MODE = 2
        MyGlobal.KEY = self.key2
        MyGlobal.PLAINTEXT = self.getResult(MyGlobal.CIPHERTEXT)
        print "\nkey2解密结果:\n"+myFile().showFile(MyGlobal.FILENAME,2)
        #MyGlobal.PLAINTEXT = self.getAsciiResult(MyGlobal.PLAINTEXT)
        #print MyGlobal.PLAINTEXT
        #key1,En
        MyGlobal.FLAG_F=0
        MyGlobal.FLAG_3=0
        MyGlobal.MODE = 1
        MyGlobal.KEY = self.key1
        MyGlobal.CIPHERTEXT = self.getResult(MyGlobal.PLAINTEXT)
        print "\n明文加密结果:\n"+myFile().showFile(MyGlobal.FILENAME,1)
        os.remove(MyGlobal.FILENAME+"_de")
        #MyGlobal.CIPHERTEXT = self.getAsciiResult(MyGlobal.CIPHERTEXT)
        #print MyGlobal.CIPHERTEXT

    def decrypt(self):
        #key1,De
        MyGlobal.FLAG_F=0
        MyGlobal.FLAG_3=0
        MyGlobal.MODE = 2
        MyGlobal.KEY = self.key1
        MyGlobal.PLAINTEXT = self.getResult(self.data)
        print "\nkey1解密结果:\n"+myFile().showFile(MyGlobal.FILENAME,2)
        #MyGlobal.PLAINTEXT = self.getAsciiResult(MyGlobal.PLAINTEXT)
        #print MyGlobal.PLAINTEXT
        #key2,En      
        MyGlobal.FLAG_F=0
        MyGlobal.FLAG_3=0
        MyGlobal.MODE = 1
        MyGlobal.KEY = self.key2
        MyGlobal.CIPHERTEXT = self.getResult(MyGlobal.PLAINTEXT)
        print "\nkey2加密结果:\n"+myFile().showFile(MyGlobal.FILENAME,1)
        #MyGlobal.CIPHERTEXT = self.getAsciiResult(MyGlobal.CIPHERTEXT)
        #print MyGlobal.CIPHERTEXT
        #key1,De
        MyGlobal.FLAG_F=0
        MyGlobal.FLAG_3=1
        MyGlobal.MODE = 2
        MyGlobal.KEY = self.key1
        MyGlobal.PLAINTEXT = self.getResult(MyGlobal.CIPHERTEXT)
        print "\n密文解密结果:\n"+myFile().showFile(MyGlobal.FILENAME,2)
        os.remove(MyGlobal.FILENAME+"_en")
        #MyGlobal.PLAINTEXT = self.getAsciiResult(MyGlobal.PLAINTEXT)
        #print MyGlobal.PLAINTEXT

    def getResult(self, data):
        result = MyDes().crypt(data, MyGlobal.MODE)
        if MyGlobal.MODE==1:
            return myFile().readFile(MyGlobal.FILENAME,MyGlobal.MODE)
        elif MyGlobal.MODE==2:
            return myFile().readFile(MyGlobal.FILENAME,MyGlobal.MODE)

    def getAsciiResult(self, result):
        result = result.replace(" ","")
        result = StrBinary().b2a_hex(result)
        return result
