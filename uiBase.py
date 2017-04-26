#-*- coding: UTF-8 -*-
import sys
import os
import wx

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import CB_Global
import classesmanager

#每个格子TextCtrl的引用
_boxes = {}  #课程格子 行是课程节 列是星期

#课程选择表的字典 键值是课程名 对应列表 0：hbox的引用 1：hbox中usrtxt的引用 2：hbox中pswdtxt的引用
_HBOXS = 0
_USRTXT = 1
_PSWDTXT = 2
_selectboxes = {}


#查询并绘制正选课程
def zk_Search(searchweek, nameTXT, pswdTXT):
    try:
        if ('' == nameTXT):
            dlg = wx.MessageBox(message='without input name', style=wx.YES | wx.ICON_WARNING)
        else:
            if ('' == pswdTXT):
                dlg = wx.MessageBox(message='without input password', style=wx.YES | wx.ICON_WARNING)
            else:
                classes = classesmanager.get_classes(nameTXT, pswdTXT)
                if(CB_Global.zk_LOGINERR_NOUSR == classes):
                    dlg = wx.MessageBox(message='用户名不存在', style=wx.YES | wx.ICON_WARNING)
                elif(CB_Global.zk_LOGINERR_NOPSWD == classes):
                    dlg = wx.MessageBox(message='密码错误', style=wx.YES | wx.ICON_WARNING)
                else:
                    _zk_DrawClass(classes, searchweek)
    except requests.exceptions.ConnectTimeout:
        dlg = wx.MessageBox(message='连接超时', style=wx.YES | wx.ICON_WARNING)
    except requests.exceptions.ReadTimeout:
        dlg = wx.MessageBox(message='网络不畅,或请连接校园网', style=wx.YES | wx.ICON_WARNING)
    except requests.exceptions.ConnectionError:
        dlg = wx.MessageBox(message='网络不畅,或请连接校园网', style=wx.YES | wx.ICON_WARNING)

#绘制课程
def _zk_DrawClass(classes, searchweek):
    for aclass in classes:
        if (0 == classesmanager.zk_is_theweek(aclass, searchweek)):
            continue
        beginnum = int(aclass['课程节'])
        lastnum = int(aclass['课程长'])
        day = int(aclass['课程日'])
        for i in range(beginnum, beginnum + lastnum):
            oldvalue = _boxes[i][day].GetValue()
            if('' != oldvalue):
                _boxes[i][day].SetDefaultStyle(wx.TextAttr("red", "black"))
            _boxes[i][day].SetValue(
                oldvalue + aclass['课程名'] + '\n' + aclass['教师名'] + '\n@' + aclass['课程楼'] + ' ' + aclass['课程室'] + '\n')

#添加课程栏目 用于扩展
def _ui_addClass(bkg,classnamelabelstr,usrnamelabelstr,pswdlabelstr):
    hbox = wx.BoxSizer()

    b_classnamelabel = wx.StaticText(bkg, label=classnamelabelstr, style=wx.ALIGN_BOTTOM)
    b_classnamelabel.SetBackgroundColour('White')
    b_usrnameTXT = wx.TextCtrl(bkg)
    b_pswdTXT = wx.TextCtrl(bkg, style=wx.TE_PASSWORD)
    b_usrnamelable = wx.StaticText(bkg, label=usrnamelabelstr, style=wx.ALIGN_BOTTOM)
    b_usrnamelable.SetBackgroundColour('White')
    b_pswdlable = wx.StaticText(bkg, label=pswdlabelstr, style=wx.ALIGN_BOTTOM)
    b_pswdlable.SetBackgroundColour('White')

    hbox.Add(b_classnamelabel, proportion = 0,flag = wx.ALL | wx.EXPAND)
    hbox.Add(b_usrnamelable, proportion=0, flag=wx.ALL | wx.EXPAND)
    hbox.Add(b_usrnameTXT, proportion=1, flag=wx.ALL)
    hbox.Add(b_pswdlable, proportion=0, flag=wx.ALL | wx.EXPAND)
    hbox.Add(b_pswdTXT, flag=wx.ALL, proportion=1)

    _selectboxes[classnamelabelstr] = []
    _selectboxes[classnamelabelstr].append(hbox)
    _selectboxes[classnamelabelstr].append(b_usrnameTXT)
    _selectboxes[classnamelabelstr].append(b_pswdTXT)

    #记录 hbox usrtxt pswdtxt 的引用
    #返回 hbox
    return hbox




