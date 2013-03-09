#!/usr/bin/python
#coding=utf-8

import os
import sys
import mmap
import math
import MyGlobal
import binascii
import threading

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
    def run(self):
		#print 'starting',self.name,'at:',ctime()
		self.res=apply(self.func,self.args)
		#print self.name,'finished at:',ctime()
    def getResult(self):
		return self.res

class _basedes():
    def setSubkey(self,subkey):
        MyGlobal.SUBKEY=subkey

    def getSubkey(self,i):
        return MyGlobal.SUBKEY[i]
    
    def getLkey(self):
        return MyGlobal.mvKEY[:28]
    def getRkey(self):
        return MyGlobal.mvKEY[28:]

class myFile():
    def countLine(self,filepath):
        fobj=open(filepath)
        count=len(fobj.readlines())
        fobj.close()
        return count

    def rfMmap(self,path):
        #内存映射
        if os.path.isfile(path):
            filename=path
        else:
            print "没有 %s 这个文件" % str(path)
            sys.exit(2)
        fobj=file(filename,"rb+")
        self.size=os.path.getsize(filename)
        fmap=mmap.mmap(fobj.fileno(),0)
        return fmap

    def showFile(self,filename,mode):
        try:
            if mode==1:
                filename+="_en"
            else:
                filename+="_de"
            self.size=os.path.getsize(filename)
            if self.size<=MyGlobal.MAXFILE:
                self.rfile=open(filename,"rb")
                #if MyGlobal.LINES==1:
                    #处理linux单行自动加换行
                    #message=filter(lambda x:x,map(lambda x:x.strip(),message))         
                myshow=""
                for i in range(self.size):
                    self.b1=self.rfile.read(1)
                    myshow+=StrBinary().bytes2hex(self.b1)
                return myshow
            else:
                if mode==1:
                    return "请查看"+os.path.abspath(filename)
                elif mode==2:
                    return "请查看"+os.path.abspath(filename)
        except ValueError:
            print "读取文件错误"
            return 0

    def readFile(self,filename,mode): 
            if mode==1:
                filename+="_en"
            else:
                filename+="_de"

            return self.rfMmap(filename)            

    def writeFile(self,filename,data,mode):
        try:
            if mode==1:
                filename+="_en"
            elif mode==2:
				filename+="_de"
            self.wfile=file(filename,"ab")
            self.wfile.write(data)
        except ValueError:
            print '写入文件错误'
            return 0
        self.wfile.close()
        return 1

    def cleanFile(self,filename,mode):
        try:
            if mode==1:
                filename+="_en"
            elif mode==2:
				filename+="_de"
            self.wfile=open(filename,"wb")
        except ValueError:
            print '清空文件错误'
            return 0
        self.wfile.close()
        return 1

class StrBinary():
    def a2b_hex(self,argstr):
        return binascii.b2a_hex(argstr)
    def b2a_hex(self,arghex):
        return binascii.a2b_hex(arghex)
    def a2b_bin(self,argstr):
        myhex=self.a2b_hex(argstr)
        return self.h2b_bin(myhex)
    def b2h_hex(self,argbin):
        return ''.join(hex(int(argbin,2))[2:])
    def h2b_bin(self,arghex):
        return ''.join(MyGlobal.hex_bin_map[x] for x in arghex)
    def int2bytes(self,argint):
        return MyGlobal.int_bytes_map[argint]
    def bytes2hex(self,bytes_hex):  
        return binascii.b2a_hex(bytes_hex)+" "

class MyDes(_basedes):
    def permutate(self,table,block):
        return map(lambda x:block[x-1],table)
    def permutateChoice(self,table,block):
        return self.permutate(table,block)
    def extendBox(self,table,block):
        return self.permutate(table,block)
    def loopMove(self,cd_key,i):
        step=MyGlobal.MoveBit[i]
        return cd_key[step:]+cd_key[:step]

    def roundKey(self,key):
        strbin=StrBinary()
        #key转换为二进制
        MyGlobal.bKEY=strbin.a2b_bin(key)
        #选择置换1
        MyGlobal.pc1KEY=self.permutateChoice(MyGlobal.PC1,MyGlobal.bKEY)
        MyGlobal.mvKEY=MyGlobal.pc1KEY
        MyGlobal.SUBKEY=[]
        for i in range(16):
           #分左右密钥
           c_key=self.getLkey()
           d_key=self.getRkey()
           c_key=self.loopMove(c_key,i)
           d_key=self.loopMove(d_key,i)
           MyGlobal.mvKEY=c_key+d_key
           #选择置换2
           MyGlobal.pc2KEY=self.permutateChoice(MyGlobal.PC2,MyGlobal.mvKEY)
           #子密钥
           if i==14 or i==15:
                print "第"+str(i+1)+"轮子密钥：\n",''.join(MyGlobal.pc2KEY)
           MyGlobal.SUBKEY.append(MyGlobal.pc2KEY)
        if MyGlobal.MODE==2:
           MyGlobal.SUBKEY.reverse()
            
    def crypt(self,data,mode):
        #import pdb
        #pdb.set_trace()
        if MyGlobal.FILENAME=="":
            MyGlobal.FILENAME="tmpDES"            
        myFile().cleanFile(MyGlobal.FILENAME,MyGlobal.MODE)
        self.roundKey(MyGlobal.KEY)
        #每个线程多少个分组
        if str(type(data))[7:10]=='str':
            datasize=len(data)
        else:
            datasize=data.size()
        if MyGlobal.FLAG_F==1:
            nblock=int(math.ceil(datasize/8.0)/MyGlobal.LOTHREAD)
            if datasize%8==0:
                nblock+=1
        else:
            nblock=(datasize/8)/MyGlobal.LOTHREAD
        #print "线程数",nblock
        if nblock<1:
            print "ERROR:请重新设置线程数.",nblock
            sys.exit(3)
        #线程步数
        nloops=range(MyGlobal.LOTHREAD)
        MyGlobal.resTHREAD=[]
        thblock=[]
        for i in nloops:
            block=[]
            for j in range(nblock):
                if MyGlobal.FLAG_F==1:
                    if i+1==MyGlobal.LOTHREAD and j+1==nblock:
                        block.append(self.blockFill(data))
                    else:    
                        block.append(data[(i*nblock+j)*8:8+(i*nblock+j)*8])
                else:
                    block.append(data[(i*nblock+j)*8:8+(i*nblock+j)*8])
            thblock.append(block)
        threads=[]        
        for i in nloops:
            t=MyThread(self.workThread,(nblock,thblock[i]),self.workThread.__name__)
            threads.append(t)
        for i in nloops:
            threads[i].start()
        for i in nloops:
            threads[i].join()
            #MyGlobal.resTHREAD.append(threads[i].getResult())
            resHex_th=self.resultHex(threads[i].getResult(),i)
            self.saveResult(resHex_th)
        #print "全部线程的返回",''.join(MyGlobal.resTHREAD[0])
        #return MyGlobal.resTHREAD

    def workThread(self,nblock,block):
        #import pdb
        #pdb.set_trace()
        resblock=[]
        #print "线程:"
        for i in range(nblock):
            #print "分组"+str(i+1)
            resblock+=self.blockRound(block[i])
        #print "一个线程返回",len(''.join(resblock))
        return resblock
        
    def blockFill(self,block):
        #import pdb
        #pdb.set_trace()
        if str(type(block))[7:10]=='str':
            bsize=len(block)
        else:
            bsize=block.size()
        bn=bsize/8
        n=bsize%8
        if n!=0:
            tblock=block[bn*8:]
            tblock+=self.fill(8-n)
        else:
            tblock=''
            tblock+=self.fill(8)
        return tblock

    def fill(self,bnum):
        zeroBytes=bnum-1
        fillBytes=StrBinary().int2bytes(bnum)
        tmp=''
        while zeroBytes>0:
            tmp+='\x00'
            zeroBytes-=1
        tmp+=fillBytes
        return tmp

    def blockRound(self,data):
        #import pdb
        #pdb.set_trace()
        strbin=StrBinary()
        bindata=strbin.a2b_bin(data)
        #IP置换
        ipPLAIN=self.permutate(MyGlobal.IP,bindata)
        #print "数据",bindata
        #print "IP",''.join(ipPLAIN),len(ipPLAIN)
        #左右分组
        Lround=ipPLAIN[:32]
        Rround=ipPLAIN[32:]
        for i in range(16):
            if i<15:       
                tmp_L=Lround
                Lround=Rround
                Rround=self.oxrStr(self.transForm(Rround,i),tmp_L)
            else:
                Rround=Rround
                Lround=self.oxrStr(self.transForm(Rround,i),Lround)
            #print i,Lround,len(Lround),Rround,len(Rround)
        resPLAIN=Lround+Rround
        ip1PLAIN=self.permutate(MyGlobal.IP_1,resPLAIN)
        #print "逆置换",''.join(ip1PLAIN),len(ip1PLAIN)
        return ip1PLAIN
     
    def transForm(self,bpart,i):
        exPLAIN=self.extendBox(MyGlobal.EBOX,bpart)
        adPLAIN=self.oxrStr(exPLAIN,self.getSubkey(i))
        sPLAIN=self.sBox(adPLAIN)
        pPLAIN=self.permutate(MyGlobal.PBOX,sPLAIN)
        return pPLAIN

    def sBox(self,bpart):
        res=""
        for i in range(8):
            row=int(bpart[i*6]+bpart[5+6*i],2)
            col=int(bpart[1+i*6:5+i*6],2)
            strbin=StrBinary()
            tmp=bin(MyGlobal.SBOX[i][row][col])[2:]
            while len(tmp)<4:
                tmp="0"+tmp
            res+=tmp
        return res
        
    def oxrStr(self,a,b):
        n=len(a)
        c=''
        for i in range(n):
            if a[i]==b[i]:
                c+="0"
            else:
                c+="1"
        return c

    def resultHex(self,res,i):
        myres=""
        strbin=StrBinary()
        #for i in range(len(res)):
            #tmp_list=res[i]
        for j in range(len(res)/8):
            tmp_bytes=res[j*8:8+8*j]
            for k in range(2):
                #print tmp_list
                myres+=strbin.b2h_hex(''.join(tmp_bytes[k*4:4+4*k]))
            myres+=" "
        #import pdb
        #pdb.set_trace()
        if MyGlobal.FLAG_3==1 and i+1==MyGlobal.LOTHREAD:
            myres=myres[:-int(myres[-2])*3]
        return myres                    
    
    def saveResult(self,result):
        result=result.replace(" ","")
        result=StrBinary().b2a_hex(result)
        filename=MyGlobal.FILENAME
        myFile().writeFile(filename,result,MyGlobal.MODE)

    def encrypt(self,data,mode):
        MyGlobal.FLAG_F=1
        MyGlobal.FLAG_3=0
        print "这是加密过程："
        self.crypt(data,mode)
        print "加密结果：(只显示小于"+str(MyGlobal.MAXFILE)+"bytes的结果)"
        print myFile().showFile(MyGlobal.FILENAME,mode)   
        MyGlobal.CIPHERTEXT=myFile().readFile(MyGlobal.FILENAME,mode)

    def decrypt(self,data,mode):
        MyGlobal.FLAG_F=0       
        MyGlobal.FLAG_3=1
        #import pdb
        #pdb.set_trace()
        print "这是解密过程："
        self.crypt(data,mode)
        print "解密结果：(只显示小于"+str(MyGlobal.MAXFILE)+"bytes的结果)"
        print myFile().showFile(MyGlobal.FILENAME,mode)
        MyGlobal.PLAINTEXT=myFile().readFile(MyGlobal.FILENAME,mode)
