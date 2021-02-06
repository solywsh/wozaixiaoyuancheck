#encoding:utf-8
import json
import requests
import time

#这里把_wozaixiaoyuan的内容换为你自己的token，自行抓包或者看https://violetwsh.com/2021/01/10/wozaixiaoyuan/#more
wozaixiaoyuan_token = ""
#自己的pushplus token，在pushplus网站中可以找到 http://pushplus.hxtrip.com/
my_pushplus_token = ''
#安全委员的pushplus token
#safe_token = ''

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

def classList (date):
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
    t = r.text
    M = t.split(',')#先做切片
    list_name = ''
    for m in M:
        #查找带有name的列表，如"name":"张三"
        if m[1:5]=="name":
            list_name = list_name + m.replace('"name":"','"')
    #给我发一份
    pushplus_post("未打卡名单",list_name,my_pushplus_token)
    #给安全委员发一份
    #pushplus_post("未打卡名单",list_name,safe_token)

def HealthCheckIn(time):
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
        'latitude' : '28.91318',
        'longitude' : '105.43779',
        'country' : '中国',
        'city' : '泸州市市',
        'district' : '龙马潭区',
        'province' : '四川省',
        'areacode' : '510504'
    }
    url = 'https://student.wozaixiaoyuan.com/health/save.json'
    s = requests.session()
    r = s.post(url, data=Hpostdata,headers=headers)
    t = r.text
    #经过测试，t返回的字典里会有一个状态码，登陆成功为0，不成功为-10，对应的就是第8个字符。
    if t[8] == '0' :
        pushplus_post("晨检，每日打卡提醒","打卡成功",my_pushplus_token)
    else:
        pushplus_post("晨检，每日打卡提醒","打卡失败，可能是token失效，请尽快重新输入。",my_pushplus_token)
    
def MorningCheck(time):
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

def NoonInspection(time):
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

if __name__ == "__main__":
    while True:
        time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
        if time_now == "06:30:10" or time_now == "06:30:11":#不知道是奇数还是偶数
            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            HealthCheckIn(time_send)#健康打卡
            #MorningCheck(time_now)#晨检

        # 午检，需要打开时取消注释即可   
        # if time_now == "11:20:10" or time_now == "11:20:11":
        #     time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #     NoonInspection(time_send)#午检
            
        if time_now == "15:30:10" or time_now == "15:30:11":#不知道是奇数还是偶数
            time_data = time.strftime("%Y%m%d")
            classList(time_data)
            
        time.sleep(2) # 停两秒
    
