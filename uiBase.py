#-*- coding: UTF-8 -*-
import sys
import os
import wx

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import CB_Global
import zk_classesmanager
import dwsy2_classesmanager
import ks_classesmanager

#每个格子TextCtrl的引用
_boxes = {}  #课程格子 行是课程节 列是星期

_CHECKBOX = 0
_USRTXT = 1
_PSWDTXT = 2
_USRSTR = 0
_PSWDSTR = 1
#课程选择表的字典 键值是checkbox 0：usrtxt引用 1：pswdtxt引用
_selectboxes = {}
#课程选择表的字典 键值是课程名 0：用户名字符串 1：密码字符串
_currentusr = {}
#临时保存用户名以及密码输入框的引用
_TXTboxes = {}

#课程名
zkname = ' 正选课程  '
dwsy2name = '大物实验二'
ksname = '     考试      '


#查询并绘制正选课程
def __Search(searchweek):
    try:
        '''
        zk_name = _currentusr[zkname][_USRSTR]
        zk_pswd = _currentusr[zkname][_PSWDSTR]
        dwsy2_name = _currentusr[dwsy2name][_USRSTR]
        dwsy2_pswd = _currentusr[dwsy2name][_PSWDSTR]
        ks_name = _currentusr[ksname][_USRSTR]
        ks_pswd = _currentusr[ksname][_PSWDSTR]
        if (('' == zk_nameTXT) or ('' == dwsy2_nameTXT) or ('' == ks_name)):
            dlg = wx.MessageBox(message='without input name', style=wx.YES | wx.ICON_WARNING)
        else:
            if (('' == zk_pswdTXT) or ('' == dwsy2_pswdTXT) or ('' == ks_pswd)):
                dlg = wx.MessageBox(message='without input password', style=wx.YES | wx.ICON_WARNING)
            else:
                classes = []

                zk_classes = zk_classesmanager.get_classes(zk_name, zk_pswd)
                if (CB_Global.zk_LOGINERR_NOUSR == zk_classes):
                    dlg = wx.MessageBox(message=zkname + ' 用户名不存在', style=wx.YES | wx.ICON_WARNING)
                elif (CB_Global.zk_LOGINERR_NOPSWD == zk_classes):
                    dlg = wx.MessageBox(message=zkname + ' 密码错误', style=wx.YES | wx.ICON_WARNING)

                dwsy_classes = dwsy2_classesmanager.get_classes(dwsy2_name, dwsy2_pswd)
                if(CB_Global.dwsy2_LOGINERR_NOUSR == dwsy_classes):
                    dlg = wx.MessageBox(message=dwsy2name + ' 用户名不存在', style=wx.YES | wx.ICON_WARNING)
                elif (CB_Global.dwsy2_LOGINERR_NOPSWD == dwsy_classes):
                    dlg = wx.MessageBox(message=dwsy2name + ' 密码错误', style=wx.YES | wx.ICON_WARNING)

                ks_classes = ks_classesmanager.get_classes(ks_name,ks_pswd)
                if (CB_Global.ks_LOGINERR_NOUSR == ks_classes):
                    dlg = wx.MessageBox(message=ksname + ' 用户名不存在', style=wx.YES | wx.ICON_WARNING)
                elif (CB_Global.ks_LOGINERR_NOPSWD == ks_classes):
                    dlg = wx.MessageBox(message=ksname + ' 密码错误', style=wx.YES | wx.ICON_WARNING)

                classes = zk_classes + dwsy_classes + ks_classes
                '''
        classes = []
        if(zkname in _currentusr):
            zk_name = _currentusr[zkname][_USRSTR]
            zk_pswd = _currentusr[zkname][_PSWDSTR]
            zk_classes = zk_classesmanager.get_classes(zk_name, zk_pswd)
            if (CB_Global.zk_LOGINERR_NOUSR == zk_classes):
                dlg = wx.MessageBox(message=zkname + ' 用户名不存在', style=wx.YES | wx.ICON_WARNING)
            elif (CB_Global.zk_LOGINERR_NOPSWD == zk_classes):
                dlg = wx.MessageBox(message=zkname + ' 密码错误', style=wx.YES | wx.ICON_WARNING)
            classes += zk_classes
        if(dwsy2name in _currentusr):
            dwsy2_name = _currentusr[dwsy2name][_USRSTR]
            dwsy2_pswd = _currentusr[dwsy2name][_PSWDSTR]
            dwsy_classes = dwsy2_classesmanager.get_classes(dwsy2_name, dwsy2_pswd)
            if (CB_Global.dwsy2_LOGINERR_NOUSR == dwsy_classes):
                dlg = wx.MessageBox(message=dwsy2name + ' 用户名不存在', style=wx.YES | wx.ICON_WARNING)
            elif (CB_Global.dwsy2_LOGINERR_NOPSWD == dwsy_classes):
                dlg = wx.MessageBox(message=dwsy2name + ' 密码错误', style=wx.YES | wx.ICON_WARNING)
            classes += dwsy_classes
        if(ksname in _currentusr):
            ks_name = _currentusr[ksname][_USRSTR]
            ks_pswd = _currentusr[ksname][_PSWDSTR]
            ks_classes = ks_classesmanager.get_classes(ks_name, ks_pswd)
            if (CB_Global.ks_LOGINERR_NOUSR == ks_classes):
                dlg = wx.MessageBox(message=ksname + ' 用户名不存在', style=wx.YES | wx.ICON_WARNING)
            elif (CB_Global.ks_LOGINERR_NOPSWD == ks_classes):
                dlg = wx.MessageBox(message=ksname + ' 密码错误', style=wx.YES | wx.ICON_WARNING)
            classes += ks_classes

        _DrawClass(classes, searchweek)

    except requests.exceptions.ConnectTimeout:
        dlg = wx.MessageBox(message='连接超时', style=wx.YES | wx.ICON_WARNING)
    except requests.exceptions.ReadTimeout:
        dlg = wx.MessageBox(message='网络不畅,或请连接校园网', style=wx.YES | wx.ICON_WARNING)
    except requests.exceptions.ConnectionError:
        dlg = wx.MessageBox(message='网络不畅,或请连接校园网', style=wx.YES | wx.ICON_WARNING)

#绘制课程
def _DrawClass(classes, searchweek):
    for aclass in classes:
        if (0 == CB_Global.is_theweek(aclass, searchweek)):
            continue
        beginnum = int(aclass['课程节'])
        lastnum = int(aclass['课程长'])
        day = int(aclass['课程日'])
        for i in range(beginnum, beginnum + lastnum):
            _boxes[i][day].SetDefaultStyle(wx.TextAttr("black", "white"))
            oldvalue = _boxes[i][day].GetValue()
            if('' != oldvalue):
                _boxes[i][day].SetDefaultStyle(wx.TextAttr("red", "white"))
            _boxes[i][day].SetValue(
                oldvalue + aclass['课程名'] + '\n' + aclass['教师名'] + '\n@' + aclass['课程楼'] + ' ' + aclass['课程室'] + '\n\n')

#####################################################对话框模块

def checkboxfun(event):
    box = event.GetEventObject()
    if(box.IsChecked()):
        _selectboxes[box][_USRTXT].Enable(True)
        _selectboxes[box][_USRTXT].SetBackgroundColour('white')
        _selectboxes[box][_PSWDTXT].Enable(True)
        _selectboxes[box][_PSWDTXT].SetBackgroundColour('white')
    else:
        _selectboxes[box][_USRTXT].Enable(False)
        _selectboxes[box][_USRTXT].SetBackgroundColour('#F2F2F2')
        _selectboxes[box][_PSWDTXT].Enable(False)
        _selectboxes[box][_PSWDTXT].SetBackgroundColour('#F2F2F2')

#添加课程栏目 用于扩展
def _ui_addClass(bkg,classnamelabelstr,usrnamelabelstr,pswdlabelstr):
    hbox = wx.BoxSizer()

    checkbox = wx.CheckBox(bkg, -1, "", style=wx.RB_GROUP)

    b_classnamelabel = wx.StaticText(bkg, label=classnamelabelstr)
    b_classnamelabel.SetBackgroundColour('White')
    b_usrnameTXT = wx.TextCtrl(bkg)
    b_usrnameTXT.SetBackgroundColour('#F2F2F2')
    b_usrnameTXT.Enable(False)
    b_pswdTXT = wx.TextCtrl(bkg, style=wx.TE_PASSWORD)
    b_pswdTXT.Enable(False)
    b_pswdTXT.SetBackgroundColour('#F2F2F2')
    b_usrnamelable = wx.StaticText(bkg, label=usrnamelabelstr, style=wx.ALIGN_BOTTOM)
    b_usrnamelable.SetBackgroundColour('White')
    b_pswdlable = wx.StaticText(bkg, label=pswdlabelstr, style=wx.ALIGN_BOTTOM)
    b_pswdlable.SetBackgroundColour('White')

    checkbox.Bind(wx.EVT_CHECKBOX, checkboxfun, checkbox)

    hbox.Add(checkbox, proportion=0, flag=wx.ALL)
    hbox.Add(b_classnamelabel, proportion = 0,flag = wx.ALL | wx.EXPAND)
    hbox.Add(b_usrnamelable, proportion=0, flag=wx.ALL | wx.EXPAND)
    hbox.Add(b_usrnameTXT, proportion=1, flag=wx.ALL)
    hbox.Add(b_pswdlable, proportion=0, flag=wx.ALL | wx.EXPAND)
    hbox.Add(b_pswdTXT, flag=wx.ALL, proportion=1)

    _selectboxes[checkbox] = []
    _selectboxes[checkbox].append(0)
    _selectboxes[checkbox].append(b_usrnameTXT)
    _selectboxes[checkbox].append(b_pswdTXT)

    _TXTboxes[classnamelabelstr] = []
    _TXTboxes[classnamelabelstr].append(checkbox)
    _TXTboxes[classnamelabelstr].append(b_usrnameTXT)
    _TXTboxes[classnamelabelstr].append(b_pswdTXT)

    #记录 hbox usrtxt pswdtxt 的引用
    #返回 hbox
    return hbox



class SelClassDia(wx.Frame):
    def cancelbtn_fun(self, event):
        self.Destroy()
    def okbtn_fun(self, event):
        _currentusr.clear()
        for i in _TXTboxes:
            if(_TXTboxes[i][_CHECKBOX].IsChecked()):
                _currentusr[i] = []
                _currentusr[i].append(_TXTboxes[i][_USRTXT].GetValue())
                _currentusr[i].append(_TXTboxes[i][_PSWDTXT].GetValue())
        self.Destroy()
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'SelectClasses', size=(800, 450), style=wx.CLOSE_BOX)

        self.total_vbox = wx.BoxSizer(wx.VERTICAL)


        #上层scroll
        self.scrollwin = wx.ScrolledWindow(self,style=wx.VSCROLL)
        self.scrollwin.SetBackgroundColour("white")
        # self.scrolled_window.SetScrollbars(1, 1, 400, 300)
        self.scrollwin.SetVirtualSize((1000, 1000))
        self.scrollwin.SetScrollRate(20, 20)

        #scroll sizer 包含 课程选择sizer
        self.scrollvbox = wx.BoxSizer(wx.VERTICAL)

        zkh = _ui_addClass(self.scrollwin,zkname,'教务账号','教务密码')
        self.scrollvbox.Add(zkh,flag = wx.EXPAND, proportion = 0)
        dwsy2h = _ui_addClass(self.scrollwin,dwsy2name,'平台账号','平台密码')
        self.scrollvbox.Add(dwsy2h,flag = wx.EXPAND, proportion = 0)
        ksh = _ui_addClass(self.scrollwin, ksname, '教务账号', '教务密码')
        self.scrollvbox.Add(ksh, flag=wx.EXPAND, proportion=0)

        self.scrollwin.SetSizer(self.scrollvbox)

        #根据初始化值初始化输入框
        if({} != _currentusr):
            for i in _currentusr:
                _TXTboxes[i][_CHECKBOX].SetValue(True)
                _TXTboxes[i][_USRTXT].SetValue(_currentusr[i][_USRSTR])
                _TXTboxes[i][_USRTXT].Enable(True)
                _TXTboxes[i][_USRTXT].SetBackgroundColour("white")
                _TXTboxes[i][_PSWDTXT].SetValue(_currentusr[i][_PSWDSTR])
                _TXTboxes[i][_PSWDTXT].Enable(True)
                _TXTboxes[i][_PSWDTXT].SetBackgroundColour("white")

        #button
        self.ok_btn = wx.Button(self,label='确定')
        self.ok_btn.Bind(wx.EVT_BUTTON, self.okbtn_fun)
        self.ok_btn.SetDefault()

        self.cancel_btn = wx.Button(self,label='取消')
        self.cancel_btn.Bind(wx.EVT_BUTTON,self.cancelbtn_fun)

        #scroll sizer
        self.hbox1 = wx.BoxSizer()
        self.hbox1.Add(self.scrollwin,flag = wx.EXPAND, proportion = 1)


        #button sizer
        self.hbox2 = wx.BoxSizer()
        self.hbox2.Add(self.ok_btn,proportion = 1)
        self.hbox2.Add(self.cancel_btn,proportion = 1,border = 5)

        self.total_vbox.Add(self.hbox1,flag = wx.EXPAND, proportion = 1)
        self.total_vbox.Add(self.hbox2, flag=wx.EXPAND, proportion=0)


        self.SetSizer(self.total_vbox)



