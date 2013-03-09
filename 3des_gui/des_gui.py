#!/usr/bin/env python
#coding=utf-8

import sys,os
mypath=os.path.abspath('../comm_des')
if mypath not in sys.path:
    sys.path.append(mypath)
from mylib import *
from MyGlobal import *
from commline import *
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class des_gui:
    global show_widget
    def __init__(self):
        self.gladefile="des_gui.glade"
        self.wTree=gtk.glade.XML(self.gladefile)
        dic={
        "on_window1_destory":gtk.main_quit,
        "on_btn_about_clicked":self.btn_about_clicked,
        "on_view1_focus_in_event":self.view1_focus_in_event,
        "on_key1_focus_in_event":self.key1_focus_in_event,
        "on_key2_focus_in_event":self.key2_focus_in_event,
        "on_view1_focus_out_event":self.view1_focus_out_event,
        "on_key1_focus_out_event":self.key1_focus_out_event,
        "on_key2_focus_out_event":self.key2_focus_out_event,
        "on_btn_file_clicked":self.btn_file_clicked,        
        "on_btn_file1_clicked":self.btn_file1_clicked,   
        "on_btn_file2_clicked":self.btn_file2_clicked,
        "on_button5_clicked":self.button5_clicked,
        "on_btn_en_clicked":self.btn_en_clicked,
        "on_btn_de_clicked":self.btn_de_clicked,
        }
        self.wTree.signal_autoconnect(dic)
        self.window1=self.wTree.get_widget("window1")
        self.about_dialog=self.wTree.get_widget("aboutdialog1")
        self.dialog_file=self.wTree.get_widget("dialog_file")    
        self.dialog_file_key1=self.wTree.get_widget("dialog_file_key1")       
        self.dialog_file_key2=self.wTree.get_widget("dialog_file_key2")
        self.view1=self.wTree.get_widget("view1")
        self.view2=self.wTree.get_widget("view2")
        self.key1=self.wTree.get_widget("key1")
        self.key2=self.wTree.get_widget("key2")
        self.radio_textfile=self.wTree.get_widget("radio_textfile")
        self.radio_keyfile=self.wTree.get_widget("radio_keyfile")
        self.window1.show()
        self.flag_text=0
    
    def btn_en_clicked(self,widget):
        MyGlobal.MODE=1
        if self.flag_text==True:
            MyGlobal.PLAINTEXT=doFile(gui_comm().get_view_text(self.view1))
        else:
            MyGlobal.PLAINTEXT=gui_comm().get_view_text(self.view1)
        if self.flag_key==True:
            MyGlobal.KEY=doFile(gui_comm().get_view_text(self.key1))
            MyGlobal.KET2=doFile(gui_comm().get_view_text(self.key2))
        else:
            MyGlobal.KEY=gui_comm().get_view_text(self.key1)
            MyGlobal.KEY2=gui_comm().get_view_text(self.key2)
        if MyGlobal.KEY2=="":
            mydes=MyDes()
            mydes.encrypt(MyGlobal.PLAINTEXT,1)
        else:
            mydes=ede2(MyGlobal.KEY,MyGlobal.KEY2,MyGlobal.PLAINTEXT).encrypt()        
        gui_comm().set_value(self.view2,"加密结果:(只显示"+str(MyGlobal.MAXFILE)+"bytes以内的结果)\n"+myFile().showFile(MyGlobal.FILENAME,MyGlobal.MODE)[0:])
    def btn_de_clicked(self,widget):
        MyGlobal.MODE=2
        if self.flag_text==True:
            MyGlobal.CIPHERTEXT=doFile(gui_comm().get_view_text(self.view1))
        else:
            MyGlobal.CIPHERTEXT=gui_comm().get_view_text(self.view1)
        if self.flag_key==True:
            MyGlobal.KEY=doFile(gui_comm().get_view_text(self.key1))
            MyGlobal.KET2=doFile(gui_comm().get_view_text(self.key2))
        else:
            MyGlobal.KEY=gui_comm().get_view_text(self.key1)
            MyGlobal.KEY2=gui_comm().get_view_text(self.key2)
        if MyGlobal.KEY2=="":
            mydes=MyDes()
            mydes.decrypt(MyGlobal.CIPHERTEXT,2)
        else:
            mydes=ede2(MyGlobal.KEY,MyGlobal.KEY2,MyGlobal.CIPHERTEXT).decrypt()
        gui_comm().set_value(self.view2,"解密结果:(只显示"+str(MyGlobal.MAXFILE)+"bytes以内的结果)\n"+myFile().showFile(MyGlobal.FILENAME,MyGlobal.MODE)[0:])

    def btn_about_clicked(self,widget):
        self.about_dialog.show()        
    def view1_focus_in_event(self,widget,event):
#        import pdb
#        pdb.set_trace()
        self.flag_text=self.radio_textfile.get_active()
        gui_comm().widget_focus_in_dialog(self.view1,self.dialog_file,self.flag_text)
    def key1_focus_in_event(self,widget,event):
        self.flag_key=self.radio_keyfile.get_active()
        gui_comm().widget_focus_in_dialog(self.key1,self.dialog_file_key1,self.flag_key)
    def key2_focus_in_event(self,widget,event):
        self.flag_key=self.radio_keyfile.get_active()
        gui_comm().widget_focus_in_dialog(self.key2,self.dialog_file_key2,self.flag_key)
    def view1_focus_out_event(self,widget,event):
        self.view1_text=gui_comm().widget_focus_out_get(self.view1)
        #print gui_comm().get_view_text(self.view1)
    def key1_focus_out_event(self,widget,event):
        self.key1_text=gui_comm().widget_focus_out_get(self.key1)
        #print gui_comm().get_view_text(self.key1)
    def key2_focus_out_event(self,widget,event):
        self.key2_text=gui_comm().widget_focus_out_get(self.key2)
        #print gui_comm().get_view_text(self.key2)
    def btn_file_clicked(self,widget):
        #import pdb
        #pdb.set_trace()
        gui_comm().set_select(self.view1,self.dialog_file)
    def btn_file1_clicked(self,widget):
        #import pdb
        #pdb.set_trace()
        gui_comm().set_select(self.key1,self.dialog_file_key1)        
    def btn_file2_clicked(self,widget):
        #import pdb
        #pdb.set_trace()
        gui_comm().set_select(self.key2,self.dialog_file_key2)
    def button5_clicked(self,widget):
        self.radio_keyfile.is_focus()
        gui_comm().hide_dialog(self.dialog_file)
     
class gui_comm:
    #获得焦点时弹出选择框
    def widget_focus_in_dialog(self,widget,dialog,flag):
        #self.view1_b=self.view1.get_buffer()
        #self.view1_text=self.view1_b.get_text(self.view1_b.get_start_iter(),self.view1_b.get_end_iter())
        #print self.view1_text
        self.widget_text=gui_comm().get_view_text(widget)
        if flag==True and len(self.widget_text)==0:
            dialog.show()
    #失去焦点时获取值
    def widget_focus_out_get(self,widget):
        self.widget_text=gui_comm().get_view_text(widget)        
        return self.widget_text
    #设置值    
    def set_value(self,widget,mytextfile):
        #给文本框赋值
        self.view_b=widget.get_buffer()
        self.view_b.set_text("\n"+mytextfile)
    #设置值为弹出框的选择    
    def set_select(self,widget,dialog):
        self.filename=dialog.get_filename()
        #print self.filename
        dialog.hide()
        #给文本框赋值
        self.view_b=widget.get_buffer()
        self.view_b.set_text(self.filename)
    #隐藏弹出框
    def hide_dialog(self,dialog):
        dialog.hide()      
    def get_view_text(self,widget):
        widget_b=widget.get_buffer()
        widget_text=widget_b.get_text(widget_b.get_start_iter(),widget_b.get_end_iter())
        return widget_text

if __name__=='__main__':
    gui=des_gui()
    gtk.main()
