#encoding:utf-8
import json
import requests
import time
#import ast #字符转字典 user_dict = ast.literal_eval(user)

#这里把_wozaixiaoyuan的内容换为你自己的token，自行抓包或者看https://violetwsh.com/2021/01/10/wozaixiaoyuan/#more
wozaixiaoyuan_token = "74c2a60f-aa33-4f2d-a4ed-880aa5363fc9"
#自己的pushplus token，在pushplus网站中可以找到 http://pushplus.hxtrip.com/
my_pushplus_token = '5097bb66-95f5-4025-94be-2be80e1329ce'
#安全委员的pushplus token
safe_token = '1394589a047b4873b314224fefcd4c7a'

def pushplus_post(title,content,token):
    url = 'http://pushplus.hxtrip.com/send'
    data = {
    "token":token,
    "title":title,
    "content":content
    }
    body=json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    requests.post(url,data=body,headers=headers)

def Unchecked_list_health(date):
    headers = {
        'content-length' : '20',
        'cookie' : 'SESSION=ZGEwY2FkOWYtZGU1My00Njk3LTgzMzctMjllMjRjMTM4YTY3;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : wozaixiaoyuan_token,
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/161/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br'
    }
    Hpostdata = {
        'type' : '0',
        'date' : date,
    }
    url = 'https://student.wozaixiaoyuan.com/health/getHealthUsers.json'
    s = requests.session()
    r = s.post(url, data=Hpostdata,headers=headers)
    ts = json.loads(r.text)#转为字典
    phone_list=[]
    name_list=''
    for t in ts['data']:
        phone_list.append('+86'+t['phone'])
        name_list = name_list + t['name']+' '
        print(t['name'])
    #短信发送
    #sent_msg(phone_list)
    #给我发一份
    pushplus_post("健康打卡未打卡名单",name_list,my_pushplus_token)
    #给安全委员发一份
    #pushplus_post("健康打卡未打卡名单",name_list,safe_token)

def Unchecked_list_morning(date):
    headers = {
        'content-length' : '20',
        'cookie' : 'SESSION=ZGEwY2FkOWYtZGU1My00Njk3LTgzMzctMjllMjRjMTM4YTY3;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : wozaixiaoyuan_token,
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/161/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br'
    }
    Hpostdata = {
        'seq':'1',
        'date':date,
        'type':'0'
    }
    url = 'https://student.wozaixiaoyuan.com/heat/getHeatUsers.json'
    s = requests.session()
    r = s.post(url, data=Hpostdata,headers=headers)

    #字符转字典的另外一种方法
    # ts = ast.literal_eval(r.text)
    # print(type(ts))

    ts = json.loads(r.text)#转为字典
    if ts['code'] != -10:
        phone_list=[]
        name_list=''
        for t in ts['data']:
            phone_list.append('+86'+t['phone'])
            name_list = name_list + t['name']+' '
            print(t['name']+':'+t['userId'])
            MorningCheck_for_classmate(t['userId'])
            #yiban_send_msg(t['number'] , 1)
            time.sleep(2)
        #短信发送
        #sent_msg(phone_list)
        #给我发一份
        pushplus_post("晨检未打卡名单",name_list,my_pushplus_token)
        #给安全委员发一份
        pushplus_post("晨检未打卡名单",name_list,safe_token)
    else:
        pushplus_post("晨检未打卡名单","Token失效！",my_pushplus_token)

def Unchecked_list_afternoon(date):
    headers = {
        'content-length' : '20',
        #'cookie' : 'SESSION=ZGEwY2FkOWYtZGU1My00Njk3LTgzMzctMjllMjRjMTM4YTY3;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : wozaixiaoyuan_token,
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/161/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br',
    }
    Hpostdata = {
        'seq':'2',
        'date':date,
        'type':'0'
    }
    url = 'https://student.wozaixiaoyuan.com/heat/getHeatUsers.json'
    s = requests.session()
    r = s.post(url, data=Hpostdata, headers=headers)
    ts = json.loads(r.text)#转为字典
    if ts['code'] != -10:
        phone_list=[]
        name_list=''
        for t in ts['data']:
            phone_list.append('+86'+t['phone'])
            name_list = name_list + t['name']+' '
            print(t['name']+':'+t['userId']+' '+t['number'])
            #yiban_send_msg(t['number'],2)
            AfternoonCheck_for_classmate(t['userId'])
            time.sleep(2)
        #短信发送
        #sent_msg(phone_list)
        #给我发一份
        pushplus_post("午检未打卡名单(已自动打卡)",name_list,my_pushplus_token)
        #给安全委员发一份
        pushplus_post("午检未打卡名单",name_list,safe_token)
    else:
        pushplus_post("午检未打卡名单","Token失效！",my_pushplus_token)

def yiban_send_msg(sid,code):
    content_key = ''
    if code == 1:
        content_key = '晨检'
    if code == 2:
        content_key = '午检'
    if code == 0:
        content_key = '健康打卡'
    postdata = {
        'key':'wsh',
        'secret':'111',
        'sid':sid,
        'title':'我在校园打卡提醒',
        'content':'你没有'+content_key,
        'url':'www.xapi.edu.cn'
    }
    url = 'http://z-6ggqgne8c25875ce-1258898586.ap-shanghai.app.tcloudbase.com/sendMessage'
    r = requests.get(url, params=postdata)
    print(r.text)


def HealthCheckIn():
    headers = {
        'content-length' : '296',
        'cookie' : 'SESSION=NGY4ZGYwNGMtZTQ3ZC00ZDRmLTg2MmEtNDRhMDYyOTZlYTAw;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : wozaixiaoyuan_token,
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/143/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br'
    }
    Hpostdata = {
        'answers' : '["0","36.5"]',
        'latitude' : '34.108216',
        'longitude' : '108.605084',
        'country' : '中国',
        'city' : '西安市',
        'district' : '鄠邑区',
        'province' : '陕西省',
        'township' : '甘亭街道',
        'street' : '东街',
        'areacode' : '610118'
    }
    url = 'https://student.wozaixiaoyuan.com/health/save.json'
    s = requests.session()
    r = s.post(url, data=Hpostdata,headers=headers)
    t = r.text
    #经过测试，t返回的字典里会有一个状态码，登陆成功为0，不成功为-10，对应的就是第8个字符。
    if t[8] == '0' :
        print("健康打卡成功！")
        #pushplus_post("每日打卡提醒","打卡成功",my_pushplus_token)
    else:
        pushplus_post("每日打卡提醒","打卡失败，可能是token失效，请尽快重新输入。",my_pushplus_token)
    
def MorningCheck():
    headers = {
        'content-length' : '306',
        'cookie' : 'SESSION=NGY4ZGYwNGMtZTQ3ZC00ZDRmLTg2MmEtNDRhMDYyOTZlYTAw;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : wozaixiaoyuan_token,
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/143/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br'
    }
    Mpostdata = {
        'answers' : '["0"]',
        'seq' : '1',
        'temperature' : '36.5',
        'userid' : '',
        'latitude' : '34.108216',
        'longitude' : '108.605084',
        'country' : '中国',
        'city' : '西安市',
        'district' : '鄠邑区',
        'province' : '陕西省',
        'township' : '甘亭街道',
        'street' : '东街',
        'myArea' : '610118'
    }
    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url, data=Mpostdata, headers=headers)

def NoonInspection():
    headers = {
        'content-length' : '134',
        'cookie' : 'SESSION=NGY4ZGYwNGMtZTQ3ZC00ZDRmLTg2MmEtNDRhMDYyOTZlYTAw;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : wozaixiaoyuan_token,
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/143/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br'
    }
    postdata = {
        'answers' : '["0","36.5"]',
        'seq' : '2',
        'temperature' : '36.6',
        'userid' : '',
        'latitude' : '34.108216',
        'longitude' : '108.605084',
        'country' : '中国',
        'city' : '西安市',
        'district' : '鄠邑区',
        'province' : '陕西省',
        'township' : '甘亭街道',
        'street' : '东街',
        'myArea' : '610118',
        'areacode' : '610118'
    }
    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url, data=postdata, headers=headers)
    t = r.text
    if t[8] == '0' :
        pushplus_post("午检打卡提醒","打卡成功",my_pushplus_token)
    else:
        pushplus_post("午检打卡提醒","可能是token失效，请尽快重新输入。",my_pushplus_token)

def MorningCheck_for_classmate(userid):
    headers = {
        'Host' : 'student.wozaixiaoyuan.com',
        'content-type' : 'application/x-www-form-urlencoded',
        'Accept' : '*/*',
        'Accept-Language' : 'zh-cn',
        'Accept-encoding' : 'gzip, deflate, br',   
        'Cookie' : 'JWSESSION=fac47cd53709450e959c9f74347206fe; path=/;',
        'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.2(0x18000237) NetType/WIFI Language/zh_CN',
        'Referer' : 'https://servicewechat.com/wxce6d08f781975d91/166/page-frame.html',
        'token' : wozaixiaoyuan_token,
        'Content-Length' : '260',
    }
    postdata = "answers=%5B%220%22%5D&seq=1&temperature=36.5&userId="+userid+"&latitude=&longitude=&country=%E4%B8%AD%E5%9B%BD&city=%E8%A5%BF%E5%AE%89%E5%B8%82&district=%E9%84%A0%E9%82%91%E5%8C%BA&province=%E9%99%95%E8%A5%BF%E7%9C%81&township=&street=&myArea=&areacode="
    
    # postdata = {
    #     'answers' : '["0"]',
    #     'seq' : '2',
    #     'temperature' : '36.5',
    #     'userid' : userid,
    #     'latitude' : '',
    #     'longitude' : '',
    #     'country' : '中国',
    #     'city' : '西安市',
    #     'district' : '鄠邑区',
    #     'province' : '陕西省',
    #     'township' : '',
    #     'street' : '',
    #     'myArea' : '',
    #     'areacode' : ''
    # }
    
    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url,data=postdata,headers=headers)
    print(r.text)

def AfternoonCheck_for_classmate(userid):
    headers = {
        'Host' : 'student.wozaixiaoyuan.com',
        'content-type' : 'application/x-www-form-urlencoded',
        'Accept' : '*/*',
        'Accept-Language' : 'zh-cn',
        'Accept-encoding' : 'gzip, deflate, br',   
        'Cookie' : 'JWSESSION=fac47cd53709450e959c9f74347206fe; path=/;',
        'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.2(0x18000237) NetType/WIFI Language/zh_CN',
        'Referer' : 'https://servicewechat.com/wxce6d08f781975d91/166/page-frame.html',
        'token' : wozaixiaoyuan_token,
        'Content-Length' : '260',
    }
    
    postdata = "answers=%5B%220%22%5D&seq=2&temperature=36.5&userId="+userid+"&latitude=&longitude=&country=%E4%B8%AD%E5%9B%BD&city=%E8%A5%BF%E5%AE%89%E5%B8%82&district=%E9%84%A0%E9%82%91%E5%8C%BA&province=%E9%99%95%E8%A5%BF%E7%9C%81&township=&street=&myArea=&areacode="

    # postdata = {
    #     'answers' : '["0"]',
    #     'seq' : '2',
    #     'temperature' : '36.5',
    #     'userid' : userid,
    #     'latitude' : '',
    #     'longitude' : '',
    #     'country' : '中国',
    #     'city' : '西安市',
    #     'district' : '鄠邑区',
    #     'province' : '陕西省',
    #     'township' : '',
    #     'street' : '',
    #     'myArea' : '',
    #     'areacode' : ''
    # }

    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url,data=postdata,headers=headers)
    print(r.text)

if __name__ == "__main__":
    while True:
        time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
        if time_now == "00:05:10" or time_now == "00:05:11":
            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            HealthCheckIn()#健康打卡
            
        time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
        if time_now == "06:30:10" or time_now == "06:30:11":
            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            MorningCheck()#晨检

        # 午检，需要打开时取消注释即可   
        if time_now == "11:05:00" or time_now == "11:05:01":
            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            NoonInspection()#午检

        # 检查健康打卡未打卡名单并提醒
        # if time_now == "14:00:00" or time_now == "14:00:01":
        #     time_data = time.strftime("%Y%m%d")
        #     Unchecked_list_health(time_data)

        #晨检未打卡名单并提醒
        if time_now == "09:50:00" or time_now == "09:50:01":
            time_data = time.strftime("%Y%m%d")
            Unchecked_list_morning(time_data)
            Unchecked_list_morning(time_data)#检查两次，会出现第一次打卡不完整的情况

        #午检未打卡名单并提醒
        if time_now == "14:50:00" or time_now == "14:50:01":
            time_data = time.strftime("%Y%m%d")
            Unchecked_list_afternoon(time_data)
            Unchecked_list_afternoon(time_data)
            
        time.sleep(2) # 停两秒