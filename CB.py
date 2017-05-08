#-*- coding: UTF-8 -*-
import sys
import os
import wx

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import CB_Global
import uiBase

import zk_classesmanager
import dwsy2_classesmanager
import ks_classesmanager



app = wx.App()
win = wx.Frame(None,title='DUTshadow',size=(1300,750))
bkg = wx.Panel(win)



#zk_hbox = uiBase._ui_addClass(bkg,uiBase.zkname,'教务账号: ','教务密码: ')
#dwsy2_hbox = uiBase._ui_addClass(bkg,uiBase.dwsy2name,'平台账号: ','平台密码: ')

#初始化 读取用户名 密码 模块
def _zkinit():
    if(os.path.exists(zk_classesmanager.zk_usrRecordpath)):
        record = zk_classesmanager.zk_ReadRecord()
        uiBase._currentusr[uiBase.zkname] = []
        uiBase._currentusr[uiBase.zkname].append(record[0])
        uiBase._currentusr[uiBase.zkname].append(record[1])
        return 1
    return 0

def _dwsy2_init():
    if(os.path.exists(dwsy2_classesmanager.dwsy2_usrRecordpath)):
        record = dwsy2_classesmanager.dwsy2_ReadRecord()
        uiBase._currentusr[uiBase.dwsy2name] = []
        uiBase._currentusr[uiBase.dwsy2name].append(record[0])
        uiBase._currentusr[uiBase.dwsy2name].append(record[1])
        return 1
    return 0

def _ks_init():
    if(os.path.exists(ks_classesmanager.ks_usrRecordpath)):
        record = ks_classesmanager.ks_ReadRecord()
        uiBase._currentusr[uiBase.ksname] = []
        uiBase._currentusr[uiBase.ksname].append(record[0])
        uiBase._currentusr[uiBase.ksname].append(record[1])
        return 1
    return 0

def init():
    #判断是否可以search
    judge = 1
    judge = _zkinit()
    judge = _dwsy2_init()
    judge = _ks_init()



#写记录模块
def writeRecord():
    if((uiBase.zkname in uiBase._currentusr) and ([] != uiBase._currentusr[uiBase.zkname])):
        zk_classesmanager.zk_WriteRecord(
            uiBase._currentusr[uiBase.zkname][uiBase._USRSTR], uiBase._currentusr[uiBase.zkname][uiBase._PSWDSTR]
        )
    if ((uiBase.dwsy2name in uiBase._currentusr) and ([] != uiBase._currentusr[uiBase.dwsy2name])):
        dwsy2_classesmanager.dwsy2_WriteRecord(
            uiBase._currentusr[uiBase.dwsy2name][uiBase._USRSTR], uiBase._currentusr[uiBase.dwsy2name][uiBase._PSWDSTR]
        )
    if ((uiBase.ksname in uiBase._currentusr) and ([] != uiBase._currentusr[uiBase.ksname])):
        ks_classesmanager.ks_WriteRecord(
            uiBase._currentusr[uiBase.ksname][uiBase._USRSTR], uiBase._currentusr[uiBase.ksname][uiBase._PSWDSTR]
        )

def _Search(searchweek):
    for i in range(1, 13):
        for j in range(1, 8):
            uiBase._boxes[i][j].SetValue('')
    uiBase.__Search(searchweek)
    writeRecord()

def Search(event):
    searchweek = zk_classesmanager.Get_thiswweek()
    if('' != b1_weekTXT.GetValue()):
        searchweek = int(b1_weekTXT.GetValue())
    else:
        b1_weekTXT.SetValue(str(searchweek))
    _Search(searchweek)

def UpSearch(event):
    searchweek = zk_classesmanager.Get_thiswweek()
    if ('' != b1_weekTXT.GetValue()):
        searchweek = int(b1_weekTXT.GetValue()) + 1
    b1_weekTXT.SetValue(str(searchweek))
    _Search(searchweek)

def DownSearch(event):
    searchweek = zk_classesmanager.Get_thiswweek()
    if ('' != b1_weekTXT.GetValue()):
        searchweek = int(b1_weekTXT.GetValue()) - 1
        if(searchweek <= 0):
            reuturn
    b1_weekTXT.SetValue(str(searchweek))
    _Search(searchweek)

def SelectClass(event):
    select_dia = uiBase.SelClassDia()
    select_dia.Show()


hbox1 = wx.BoxSizer()
b1_selectBtN = wx.Button(bkg,label='select')
b1_selectBtN.Bind(wx.EVT_BUTTON, SelectClass)

b1_searchBTN = wx.Button(bkg,label='search')
b1_searchBTN.SetBackgroundColour('Green')
b1_searchBTN.Bind(wx.EVT_BUTTON, Search)
b1_searchBTN.SetDefault()

b1_weekupBTN = wx.Button(bkg,label='up')
b1_weekupBTN.Bind(wx.EVT_BUTTON, UpSearch)

b1_weekdnBTN = wx.Button(bkg,label='down')
b1_weekdnBTN.Bind(wx.EVT_BUTTON, DownSearch)

b1_weekTXT = wx.TextCtrl(bkg)
b1_weeklable = wx.StaticText(bkg,label="周",style=wx.ALIGN_BOTTOM)
b1_weeklable.SetBackgroundColour('WHEAT')

hbox1.Add(b1_selectBtN,flag = wx.ALL | wx.EXPAND,proportion = 0)
hbox1.Add(b1_searchBTN,flag = wx.ALL | wx.EXPAND,proportion = 1)
hbox1.Add(b1_weekupBTN,flag = wx.ALL|wx.EXPAND,proportion = 0)
hbox1.Add(b1_weekdnBTN,flag = wx.ALL|wx.EXPAND,proportion = 0)
hbox1.Add(b1_weekTXT,flag = wx.ALL|wx.EXPAND,proportion = 0)
hbox1.Add(b1_weeklable,flag = wx.ALL,proportion = 0)



hbox2 = wx.BoxSizer()
b2_headlable = wx.StaticText(bkg,label='',style=wx.ALIGN_CENTER)
b2_headlable.SetBackgroundColour('White')
b2_week1lable = wx.StaticText(bkg,label='星期一',style=wx.ALIGN_CENTER)
b2_week1lable.SetBackgroundColour('White')
b2_week2lable = wx.StaticText(bkg,label='星期二',style=wx.ALIGN_CENTER)
b2_week2lable.SetBackgroundColour('White')
b2_week3lable = wx.StaticText(bkg,label='星期三',style=wx.ALIGN_CENTER)
b2_week3lable.SetBackgroundColour('White')
b2_week4lable = wx.StaticText(bkg,label='星期四',style=wx.ALIGN_CENTER)
b2_week4lable.SetBackgroundColour('White')
b2_week5lable = wx.StaticText(bkg,label='星期五',style=wx.ALIGN_CENTER)
b2_week5lable.SetBackgroundColour('White')
b2_week6lable = wx.StaticText(bkg,label='星期六',style=wx.ALIGN_CENTER)
b2_week6lable.SetBackgroundColour('White')
b2_week7lable = wx.StaticText(bkg,label='星期日',style=wx.ALIGN_CENTER)
b2_week7lable.SetBackgroundColour('White')
hbox2.Add(b2_headlable,proportion = 1,flag = wx.ALL,border = 1)
hbox2.Add(b2_week1lable,proportion = 1,flag = wx.ALL,border = 1)
hbox2.Add(b2_week2lable,proportion = 1,flag = wx.ALL,border = 1)
hbox2.Add(b2_week3lable,proportion = 1,flag = wx.ALL,border = 1)
hbox2.Add(b2_week4lable,proportion = 1,flag = wx.ALL,border = 1)
hbox2.Add(b2_week5lable,proportion = 1,flag = wx.ALL,border = 1)
hbox2.Add(b2_week6lable,proportion = 1,flag = wx.ALL,border = 1)
hbox2.Add(b2_week7lable,proportion = 1,flag = wx.ALL,border = 1)

vbox = wx.BoxSizer(wx.VERTICAL)
for i in range(1,13):
    hbox = wx.BoxSizer()
    #headlable = wx.StaticText(bkg, label=classtime[i], style=wx.ALIGN_CENTER|wx.TE_MULTILINE)
    headlable = wx.TextCtrl(bkg, value=CB_Global.classtime[i], style=wx.ALIGN_CENTER | wx.TE_MULTILINE | wx.TE_READONLY)
    headlable.SetBackgroundColour('White')
    hbox.Add(headlable, proportion=1, flag=wx.ALL | wx.EXPAND, border=1)
    uiBase._boxes[i] = ['NULL']
    for j in range(1,8):
        lable = wx.TextCtrl(bkg, style=wx.ALIGN_CENTER | wx.TE_MULTILINE | wx.TE_READONLY)
        lable.SetBackgroundColour('White')
        hbox.Add(lable, proportion=1, flag=wx.ALL | wx.EXPAND, border=1)
        uiBase._boxes[i].append(lable)
    vbox.Add(hbox, flag=wx.EXPAND, proportion=1)

total_vbox = wx.BoxSizer(wx.VERTICAL)
total_vbox.Add(hbox1,flag = wx.EXPAND,proportion = 0)
#total_vbox.Add(zk_hbox,flag = wx.EXPAND, proportion = 0)
#total_vbox.Add(dwsy2_hbox,flag = wx.EXPAND, proportion = 0)
total_vbox.Add(hbox2,flag = wx.EXPAND,proportion = 0)
total_vbox.Add(vbox,flag = wx.EXPAND,proportion = 1,)

bkg.SetSizer(total_vbox)

init()


win.Show()

app.MainLoop()
