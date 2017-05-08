#-*- coding: UTF-8 -*-
import sys
import os
import requests
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import CB_Global

#####################################################################################
#主课程 zk 管理模块

#由 用户名 与 密码 获取课程 返回课程信息列表
def get_classes(name,pswd):
    r = log_in(name,pswd)
    if((CB_Global.zk_LOGINERR_NOUSR == r) or (CB_Global.zk_LOGINERR_NOPSWD == r)):
        return r
    begin = 0
    _class_name = ''
    _teacher_name = ''
    classes = []
    while (1):
        judge = CB_Global.zk_judge_pa.search(r, pos=begin)
        if (None == judge):
            break
        if (_is_class_module(judge.group(0))):
            aclass = CB_Global.zk_cpa18.search(r, pos=begin)
            begin = aclass.end()
            msglist = CB_Global.zk_mpa.findall(aclass.group(0))
            result = _deal_with_cm(msglist)
            _class_name = result['课程名']
            _teacher_name = result['教师名']
            classes.append(result)
        else:
            aclass = CB_Global.zk_cpa7.search(r, pos=begin)
            begin = aclass.end()
            msglist = CB_Global.zk_mpa.findall(aclass.group(0))
            result = _deal_with_tm(msglist, _class_name, _teacher_name)
            classes.append(result)
        #ttt = raw_input()
    return classes

#登陆教务网 并且返回网页代码
def log_in(name,pswd):
    mydata = {
        'zjh':name,
        'mm':pswd
    }
    s = requests.post("http://zhjw.dlut.edu.cn//loginAction.do", timeout=2, headers=CB_Global.my_headers, data=mydata)
    s.encoding = 'gbk'
    #检查 账户名存在 与密码正误
    if (CB_Global.zk_checkusr_pa.search(s.text)):
        return CB_Global.zk_LOGINERR_NOUSR
    if (CB_Global.zk_checkpswd_pa.search(s.text)):
        return CB_Global.zk_LOGINERR_NOPSWD
    _cookies = s.cookies
    r = requests.get('http://zhjw.dlut.edu.cn/xkAction.do?actionType=6',timeout=2, cookies=_cookies, )
    r.encoding = 'gbk'
    return r.text

#判断是否是课程模块 否则问同一课程其他信息模块
def _is_class_module(_line_0):
    return None != CB_Global.zk_is_class_module_pa.search(_line_0)

#处理课程模块并提取信息 返回字典
def _deal_with_cm(msglist):
    result = {}
    result['课程名'] = "".join(__typicalsplit(msglist[CB_Global.zk_cm_classname]).split())
    result['课程周'] = "".join(__typicalsplit(msglist[CB_Global.zk_cm_weeks]).split())
    result['课程日'] = "".join( __typicalsplit(msglist[CB_Global.zk_cm_weekdays]).split())
    result['课程节'] = "".join(__typicalsplit(msglist[CB_Global.zk_cm_classtime]).split())
    result['课程长'] = "".join(__typicalsplit(msglist[CB_Global.zk_cm_classlong]).split())
    result['课程楼'] = "".join(__typicalsplit(msglist[CB_Global.zk_cm_classblock]).split())
    result['课程室'] = "".join(__typicalsplit(msglist[CB_Global.zk_cm_classroom]).split())
    teachername = "".join(__typicalsplit(msglist[CB_Global.zk_cm_teachername]).split());
    teachername = teachername[0:len(teachername)-1]
    result['教师名'] = teachername
    return result

#处理信息模块并提取信息 返回字典
def _deal_with_tm(msglist,classname,teachername):
    result = {}
    result['课程名'] = classname
    result['教师名'] = teachername
    result['课程周'] = "".join(__typicalsplit(msglist[CB_Global.zk_tm_weeks]).split())
    result['课程日'] = "".join(__typicalsplit(msglist[CB_Global.zk_tm_weekdays]).split())
    result['课程节'] = "".join(__typicalsplit(msglist[CB_Global.zk_tm_classtime]).split())
    result['课程长'] = "".join(__typicalsplit(msglist[CB_Global.zk_tm_classlong]).split())
    result['课程楼'] = "".join(__typicalsplit(msglist[CB_Global.zk_tm_classblock]).split())
    result['课程室'] = "".join(__typicalsplit(msglist[CB_Global.zk_tm_classroom]).split())
    return result

#以分号为切割符 获取后面的部分
def __typicalsplit(s):
    return s.split(';')[1]

#####################################################################################
#时间管理模块





#获取当前周数
def Get_thiswweek():
    gaptime = date.today() - CB_Global.oldtime
    thisweek = CB_Global._setup_weeknum + gaptime.days / 7
    return thisweek



###############################################
#用户名 密码记录文件

#正选课程
zk_usrRecordpath = os.path.abspath(os.path.join(os.path.dirname(__file__),'zkusr'))

def zk_WriteRecord(usr, pswd):
    recordFile = open(zk_usrRecordpath,'w')
    recordFile.write(usr + pswd)
    recordFile.close()

def zk_ReadRecord():
    t = []
    if(os.path.exists(zk_usrRecordpath)):
        recordFile = open(zk_usrRecordpath,'r')
        record = recordFile.read()
        recordFile.close()
        usr = record[0:9]
        pswd = record[9:17]
        t.append(usr)
        t.append(pswd)
    return t
