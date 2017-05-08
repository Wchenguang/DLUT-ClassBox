#-*- coding: UTF-8 -*-
import sys
import os
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import CB_Global

#####################################################################################
#主课程 zk 管理模块

#由 用户名 与 密码 获取课程 返回课程信息列表
def get_classes(name,pswd):
    r = log_in(name,pswd)
    if ((CB_Global.ks_LOGINERR_NOUSR == r) or (CB_Global.ks_LOGINERR_NOPSWD == r)):
        return r
    classes = []
    cmodules = CB_Global.ks_cpa.findall(r)
    for i in cmodules:
        classes.append(deal_with_aclass(i))
    return classes

def deal_with_aclass(cmoudule):
    result = {}
    result['课程周'] = "".join(cmoudule.split(u'周')[0].split(u'第')[1].split())
    result['课程周'] = result['课程周'] + '-' + result['课程周']
    result['课程楼'] = "".join(cmoudule.split('</td>')[2].split('<td>')[1].split())
    result['课程室'] = "".join(cmoudule.split('</td>')[3].split('<td>')[1].split())
    result['课程名'] = "".join(cmoudule.split('</td>')[4].split('<td>')[1].split('&nbsp')[0].split())
    result['教师名'] = u"考试"
    result['课程日'] = "".join(cmoudule.split('</td>')[6].split('<td>')[1].split())

    starttime = "".join(cmoudule.split('</td>')[7].split('">')[1].split('-')[0].split())
    startc = CB_Global.time2c(CB_Global.time2gaptime(starttime))
    if(0 != startc%1):
        startc += 0.5
    result['课程节'] = str(int(startc))

    endtime = "".join(cmoudule.split('</td>')[7].split('">')[1].split('-')[1].split())
    endc = CB_Global.time2c(CB_Global.time2gaptime(endtime))
    if(0 != endc%1):
        endc -= 0.5
    gapc = int(endc) - int(result['课程节']) + 1
    result['课程长'] = str(gapc)

    return result 
    #print result['课程周'],result['课程楼'],result['课程室'],result['课程名'],result['课程日'],result['课程节'],result['课程长']

#登陆教务网 并且返回网页代码
def log_in(name,pswd):
    mydata = {
        'zjh':name,
        'mm':pswd
    }
    s = requests.post("http://zhjw.dlut.edu.cn//loginAction.do", timeout=2, headers=CB_Global.my_headers, data=mydata)
    s.encoding = 'gbk'

    #检查 账户名存在 与密码正误
    if (CB_Global.ks_checkusr_pa.search(s.text)):
        return CB_Global.ks_LOGINERR_NOUSR
    if (CB_Global.ks_checkpswd_pa.search(s.text)):
        return CB_Global.ks_LOGINERR_NOPSWD
    _cookies = s.cookies
    r = requests.get('http://zhjw.dlut.edu.cn/ksApCxAction.do?oper=getKsapXx',timeout=2, cookies=_cookies, )
    r.encoding = 'gbk'

    return r.text


#####################################################
#用户名 密码记录文件

#k考试
ks_usrRecordpath = os.path.abspath(os.path.join(os.path.dirname(__file__),'ksusr'))

def ks_WriteRecord(usr, pswd):
    recordFile = open(ks_usrRecordpath,'w')
    recordFile.write(usr + ' ' + pswd)
    recordFile.close()

def ks_ReadRecord():
    t = []
    if(os.path.exists(ks_usrRecordpath)):
        recordFile = open(ks_usrRecordpath,'r')
        record = recordFile.read()
        recordFile.close()
        usr = record.split(' ')[0]
        pswd = record.split(' ')[1]
        t.append(usr)
        t.append(pswd)
    return t

