#!/usr/bin/env python
#coding=utf-8
from mylib import *
import MyGlobal
from des_ede2 import *
import os
import sys
from optparse import OptionParser
from optparse import OptionGroup
#解决中文帮助
reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
parser=None

def getOption():
    #工具说明
    global parser
    USAGE='usage: %prog [option] args \n默认工作模式为ECB'
    parser=OptionParser(USAGE)
    
    #文件操作选项
    group1=OptionGroup(parser,"文件操作")
    group1.add_option('--keyfile',action='store',dest='keyfile',default=False,help='密钥文件')
    group1.add_option('--textfile',action='store',dest='textfile',default=False,help='进行加密解密的文件')
    #DES-EDE2
    group3=OptionGroup(parser,'DES-EDE2模式')
    group3.add_option("--key2",action='store',dest='key2',default=False,help='指定key2，将会进行DES-EDE2模式加密解密')
    group3.add_option("--key2file",action='store',dest='key2file',default=False,help='指定key2file，将会进行DES-EDE2模式加密解密')
    #运行模式
    #group4=OptionGroup(parser,'对称密码体制运行模式')
    #group4.add_option("--method",action="store",default=MyGlobal.METHOD,type='int',dest='method',help="工作模式：1)ECB(默认)  2)CBC  3)CFB  4)OFB")
    #group4.add_option("--IV",action="store",default=MyGlobal.IV,dest='IV',help="不指定默认为"+MyGlobal.IV)
    #自测选项
    group2=OptionGroup(parser,'自测操作')
    group2.add_option("--testself",action="store_true",dest="test",default=False,help="自测模式"+'key="12345678",text="123456789"')
    
    #基本选项
    parser.add_option('-m','--mode',action='store',type='int',dest='mode',default=False,help='选择加密为1 选择解密为2')
    parser.add_option('-k','--key',action='store',dest='key',default=False,help='密钥字符串')
    parser.add_option('-t','--text',action='store',dest='text',default=False,help='进行加密解密的字符串')
    #parser.add_option('-p',action='store',type='int',dest='printl',default=MyGlobal.PRINTLEVEL,help='终端打印等级,默认值为'+str(MyGlobal.PRINTLEVEL))
    #parser.add_option('-l',action='store',type='int',dest='level',default=MyGlobal.LOGLEVEL,help='日志保存的等级,默认值为'+str(MyGlobal.LOGLEVEL))
    #parser.add_option('--logfile',action='store',dest='logfile',type='string',default=MyGlobal.LOGNAME,help='日志文件名,默认值为'+str(MyGlobal.LOGNAME))
    parser.add_option('--thread',action='store',type='int',dest='thread',default=MyGlobal.LOTHREAD,help='设置线程数,默认值为'+str(MyGlobal.LOTHREAD))
    #添加分组选项
    parser.add_option_group(group1)   
    parser.add_option_group(group2)
    parser.add_option_group(group3)
    #parser.add_option_group(group4)
    #参数处理
    (opts,args)=parser.parse_args(sys.argv)
    #必要参数处理
    if len(sys.argv)==1:
        print "ERROR: 未设置参数."
        doHelp()
	#是否设置为自测
    if opts.test!=False:
        MyGlobal.MODE=1
        MyGlobal.KEY="12345678"
        MyGlobal.PLAINTEXT="123456789"
    else:
        MyGlobal.MODE=opts.mode
    #必须密钥
    if opts.keyfile!=False:
        MyGlobal.KEY=doFile(opts.keyfile)
    elif opts.key!=False:
        MyGlobal.KEY=opts.key
    #必须处理文件
    if opts.textfile!=False:
        MyGlobal.FILENAME=opts.textfile
        if opts.mode==1:
            #模式为加密
            MyGlobal.PLAINTEXT=doFile(opts.textfile)
        elif opts.mode==2:
            #模式为解密
            MyGlobal.CIPHERTEXT=doFile(opts.textfile)
    elif opts.text!=False:
        if opts.mode==1:
            #模式为加密
            MyGlobal.PLAINTEXT=opts.text
        elif opts.mode==2:
            #模式为解密
            MyGlobal.CIPHERTEXT=opts.text
    #3DES参数处理
    if opts.key2!=False:
        MyGlobal.KEY2=opts.key2
    elif opts.key2file!=False:
        MyGlobal.KEY2=doFile(opts.key2file)

    #缺乏必要参数或者参数格式错误
    if str(MyGlobal.MODE)=="":
        print "ERROR: 未设置加密(1)或者解密(2)."
        doHelp()
    elif (str(MyGlobal.PLAINTEXT)=="") and (str(MyGlobal.CIPHERTEXT)=="") :
        print "ERROR: 需要加密或解密的数据为空."
        doHelp()
    elif (str(MyGlobal.KEY)=="") or (len(str(MyGlobal.KEY))!=8) :
        #print "ERROR: 密钥为空或者不为8字节."+str(MyGlobal.KEY),len(str(MyGlobal.KEY))
        #doHelp()
        MyGlobal.KEY=goodkey(MyGlobal.KEY)
    elif (MyGlobal.KEY2!="") and (len(str(MyGlobal.KEY2))!=8):
        #print "ERROR: 密钥2不为8字节"
        #doHelp()
        MyGlobal.KEY2=goodkey(MyGlobal.KEY2)
    elif len(str(MyGlobal.IV))!=8:
        print "ERROR:初始变量不为8字节"
        doHelp()

    #其他参数处理
    #MyGlobal.PRINTLEVEL=opts.printl
    #MyGlobal.LOGLEVEL=opts.level
    #MyGlobal.LOGNAME=opts.logfile
    MyGlobal.LOTHREAD=opts.thread
    
    #创建des对象
    if opts.test!=False:
        #加密模式
        createDes(MyGlobal.MODE)
        #解密模式
        MyGlobal.MODE=2
        createDes(MyGlobal.MODE)
    else:
        createDes(MyGlobal.MODE)

def createDes(mode):
    if MyGlobal.KEY2=="":
        mydes=MyDes()
        if mode==1:
            mydes.encrypt(MyGlobal.PLAINTEXT,mode)
        elif mode==2:
            mydes.decrypt(MyGlobal.CIPHERTEXT,mode)
    else:
        if mode==1:
            mydes=ede2(MyGlobal.KEY, MyGlobal.KEY2, MyGlobal.PLAINTEXT).encrypt()
        elif mode==2:
            mydes=ede2(MyGlobal.KEY, MyGlobal.KEY2, MyGlobal.CIPHERTEXT).decrypt()

def doHelp():
    global parser
    parser.print_help()
    sys.exit(1)

def doFile(filename):
    #print "执行文件处理"
    objfile=myFile()
    return objfile.rfMmap(filename)

def goodkey(key):
    while True:
        if str(type(key))[7:10]=='str':
            mylen=len(key)
        else:
            mylen=key.size()
        #print mylen
        if mylen<8:
            key+='\x00'
        elif mylen>8:
            key=key[:8]
        else:
            break
    return key

def main():
    getOption()

if __name__=='__main__':
    main()
