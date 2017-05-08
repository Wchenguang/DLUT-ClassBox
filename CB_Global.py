#-*- coding: UTF-8 -*-
import sys
import re
import os
from datetime import date

#模拟浏览器登陆的http头
my_headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
}

#时间信息 根据预设信息 计算周数
_setup_year = 2017
_setup_month = 4
_setup_day = 24
_setup_weeknum = 9

#由预设信息 设定一个date类
oldtime = date(_setup_year,_setup_month,_setup_day)

#所有课程的时间节数对应时间
classtime = ['NULL','第1节\n(08:00-08:45)','第2节\n(08:50-09:35)','第3节\n(10:05-10:50)','第4节\n(10:55-11:40)',
             '第5节\n(13:30-14:15)','第6节\n(14:20-15:05)','第7节\n(15:35-16:20)','第8节\n(16:25-17:10)',
             '第9节\n(18:00-18:45)','第10节\n(18:55-19:40)','第11节\n(19:50-20:35)','第12节\n(20:45-21:30)']

#距离分钟数对应节数字典
tcarr = [
    [45 , 1],
    [50 , 1.5],
    [95  , 2],
    [125 , 2.5],
    [170 , 3],
    [175 , 3.5],
    [220 , 4],
    [330 , 4.5],
    [375 , 5],
    [380 , 5.5],
    [425 , 6],
    [455 , 6.5],
    [500 , 7],
    [505 , 7.5],
    [550 , 8],
    [600 , 8.5],
    [645 , 9],
    [655 , 9.5],
    [700 , 10],
    [710 , 10.5],
    [755 , 11],
    [765 , 11.5],
    [810 , 12]
]

#根据距离8点的分钟数 返回所在节数
def time2c(min):
    m = int(min)
    for i in tcarr:
        if (m <= i[0]):
            return i[1]


#将 24小时 如12:23 转化为其距离8:00的分钟数
def time2gaptime(atime):
    hour = int(atime.split(':')[0])
    min = int(atime.split(':')[1])
    return (hour - 8) * 60 + min




day_Chi2int = {u'一':'1',u'二':'2',u'三':'3',u'四':'4',u'五':'5',u'六':'6',u'日':'7'}

################################################################################
#正选课程 html代码 课程模块 具体信息所在</br>下标序号
zk_cm_classname = 2
zk_cm_teachername = 7
zk_cm_weeks = 10
zk_cm_weekdays = 11
zk_cm_classtime = 12
zk_cm_classlong = 13
zk_cm_classblock = 15
zk_cm_classroom = 16

#正选课程 html代码 同一课程不同时间信息模块 具体信息所在</br>下标序号
zk_tm_weeks = 0
zk_tm_weekdays = 1
zk_tm_classtime = 2
zk_tm_classlong = 3
zk_tm_classblock = 5
zk_tm_classroom = 6

#查找模块开头 可以匹配 课程模块与信息模块
zk_judge_pa = re.compile(ur'<tr class="?odd"? onMouseOut="?this.className=\'even\';"? onMouseOver="?this.className=\'evenfocus\';"?>([\S\s]*?<td[\S\s]*?</td>)')
#分辨该模块是否是 课程模块的正则 若不是 则是 上一课程的不同信息模块
zk_is_class_module_pa = re.compile(u"培养方案")
#在 课程模块中提取 18 对</td>
zk_cpa18 = re.compile(ur'<tr class="?odd"? onMouseOut="?this.className=\'even\';"? onMouseOver="?this.className=\'evenfocus\';"?>([\S\s]*?<td[\S\s]*?</td>){18}')
#在 信息模块中提取 7对</td>
zk_cpa7 = re.compile(ur'<tr class="?odd"? onMouseOut="?this.className=\'even\';"? onMouseOver="?this.className=\'evenfocus\';"?>([\S\s]*?<td[\S\s]*?</td>){7}')
#在匹配的</td>中 提取信息 (无法去掉前面的)
zk_mpa = re.compile(ur'<td[\w\W]*?>[\w\W]*?&nbsp;[\W\w]*?(?=</td>)')
#检测 正课登陆 账号存在 密码错误  ##您的密码不正确，请您重新输入！
zk_checkpswd_pa = re.compile(ur'密码不正确')
#检测正课 证件号不存在  ##你输入的证件号不存在，请您重新输入！
zk_checkusr_pa = re.compile(ur'证件号不存在')

#正选课程 登陆异常错误
#账户不存在
zk_LOGINERR_NOUSR = 0
#账户存在 密码错误
zk_LOGINERR_NOPSWD = 1

################################################################################
#大物实验2 html代码处理模块

#匹配 大物实验2 课程模块
dwsy2_cpa = re.compile(ur'<!--实训\\实验项目名称//-->[\S\s]*?<font[\S\s]*?<!--预约状态//-->[\S\s]*?</font></td>')
#匹配大物实验2 账户不存在 ##该帐号不存在，请重新登录
dwsy2_checkusr_pa = re.compile(ur'帐号不存在')
#匹配密码错误 ##密码错误，请重新输入密码
dwsy2_checkpswd_pa = re.compile(ur'密码错误')
#匹配 未选择该课程  您尚未预约!    实训\实验已完成!  实训\实验关闭中
dwsy2_is_chosen_pa = re.compile(ur'(您尚未预约)|(实验已完成)|(关闭中)')

#大物实验2 登陆异常错误
#登陆不存在
dwsy2_LOGINERR_NOUSR = 0
#账户存在 密码错误
dwsy2_LOGINERR_NOPSWD = 1

################################################################################
#考试 html处理模块

#匹配 考试 课程模块
ks_cpa = re.compile(ur'<tr class[\s\S]*?考试安排[\s\S]*?</tr>')
#检测 正课登陆 账号存在 密码错误  ##您的密码不正确，请您重新输入！
ks_checkpswd_pa = re.compile(ur'密码不正确')
#检测正课 证件号不存在  ##你输入的证件号不存在，请您重新输入！
ks_checkusr_pa = re.compile(ur'证件号不存在')

#正选课程 登陆异常错误
#账户不存在
ks_LOGINERR_NOUSR = 0
#账户存在 密码错误
ks_LOGINERR_NOPSWD = 1


#判断一门课程是否在那一周
def is_theweek(aclass,theweek):
    #部分课程无周信息
    if('' == aclass['课程周']):
        return 0
    #获取课程信息 课程周 上下限
    low = int(aclass['课程周'].split('-')[0])
    high = int(aclass['课程周'].split('-')[1].split(u'周')[0])
    if((theweek<low) or (theweek>high)):
        return 0
    return 1




