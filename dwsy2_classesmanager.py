#-*- coding: UTF-8 -*-
import sys
import os
import requests
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import CB_Global

def get_classes(name,pswd):
    r = log_in(name,pswd)
    if((CB_Global.dwsy2_LOGINERR_NOUSR == r) or (CB_Global.dwsy2_LOGINERR_NOPSWD == r)):
        return r
    classes = []
    cmodules = CB_Global.dwsy2_cpa.findall(r)
    for i in cmodules:
        if (CB_Global.dwsy2_is_chosen_pa.search(i)):
            continue
        classes.append(deal_with_aclass(i))
    return classes


def deal_with_aclass(cmoudule):
    t = cmoudule.split(u'地点;')[1]
    result = {}
    result['课程楼'] = "".join(t.split('<br>')[0].split())
    result['课程室'] = ''
    result['课程名'] = "".join(t.split('>')[2].split('<')[0].split())

    tt = t.split(u"<!--预约状态//-->")[1]

    result['课程周'] = "".join(tt.split(u'第')[1].split(u'周')[0].split())
    result['课程周'] = result['课程周'] + '-' + result['课程周']
    result['课程日'] = CB_Global.day_Chi2int["".join(tt.split(u'周')[1].split(' ')[0].split())]
    result['课程节'] = "".join(tt.split(u'周')[1].split(' ')[1].split('-')[0].split())
    result['教师名'] = "".join(tt.split(u'节')[1].split('<')[0].split())

    high = "".join(tt.split(u'周')[1].split(' ')[1].split('-')[1].split(u'节')[0].split())
    result['课程长'] = str(int(high) - int(result['课程节']) + 1)
    return result

#登陆 大连理工 ⌚️教学管理平台  role:2 为学生登陆  role:1 为教师登陆 默认为2
def log_in(name,pswd):
    mydata = {
        'userid' : name,
        'password' : pswd,
        'role' : '2'
    }
    s = requests.post('http://202.118.65.73/system/sysselect.php',data=mydata,headers = CB_Global.my_headers, timeout = 2)
    _cookies1 = s.cookies

    if ('url=..' not in s.content):
        return CB_Global.dwsy2_LOGINERR_NOUSR
    url1 = 'http://202.118.65.73/' +  s.content.split('url=..')[1].split('"')[0]

    s1 = requests.get(url1,headers = CB_Global.my_headers,timeout = 2,cookies = _cookies1)
    _cookies2 = s1.cookies
    s1.encoding = 'gbk'

    if(CB_Global.dwsy2_checkusr_pa.search(s1.text)):
        return CB_Global.dwsy2_LOGINERR_NOUSR
    elif(CB_Global.dwsy2_checkpswd_pa.search(s1.text)):
        return CB_Global.dwsy2_LOGINERR_NOPSWD


    url2 = 'http://202.118.65.73/student/' + s1.content.split('URL = ')[1].split('"')[0]
    s2 = requests.get(url2,
                     cookies = _cookies2.get_dict(), timeout = 2,headers = CB_Global.my_headers)


    r = requests.get('http://202.118.65.73/student/exp_list.php?course_id=1535020&course_name=%B4%F3%D1%A7%CE%EF%C0%ED%CA%B5%D1%E9%A3%A8%B6%FE%A3%A9',
                    cookies = _cookies2.get_dict(), timeout = 2, headers = CB_Global.my_headers)
    r.encoding = 'gbk'

    return r.text


log_in('','201585058')

#####################################################
#用户名 密码记录文件

#大物实验2
dwsy2_usrRecordpath = os.path.abspath(os.path.join(os.path.dirname(__file__),'dwsy2usr'))

def dwsy2_WriteRecord(usr, pswd):
    recordFile = open(dwsy2_usrRecordpath,'w')
    recordFile.write(usr + ' ' + pswd)
    recordFile.close()

def dwsy2_ReadRecord():
    t = []
    if(os.path.exists(dwsy2_usrRecordpath)):
        recordFile = open(dwsy2_usrRecordpath,'r')
        record = recordFile.read()
        recordFile.close()
        usr = record.split(' ')[0]
        pswd = record.split(' ')[1]
        t.append(usr)
        t.append(pswd)
    return t





