'''
Author: your name
Date: 2021-02-03 10:26:22
LastEditTime: 2021-02-03 10:48:53
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \undefinedf:\StudyDate\python\我在校园打卡\每日健康打卡_pushplus.py
'''
# encoding:utf-8
import requests
import time
import json

#这里把_wozaixiaoyuan的内容换为你自己的token，自行抓包或者看https://violetwsh.com/2021/01/10/wozaixiaoyuan/#more
wozaixiaoyuan_token = "2da85d2e-2ab8-48de-a78f-27929a1ff2cf"  

#在pushpush网站中可以找到 http://pushplus.hxtrip.com/
pushplus_token = '你的Token'

def pushplus_post(title,content):
    url = 'http://pushplus.hxtrip.com/send'
    data = {
    "token":pushplus_token,
    "title":title,
    "content":content
    }
    body=json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    requests.post(url,data=body,headers=headers)
    
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
        pushplus_post("每日打卡提醒","打卡成功")
    else:
        pushplus_post("每日打卡提醒","打开失败，可能是token失效，请尽快重新输入。")

if __name__ == "__main__":
    while True:
        time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
        if time_now == "08:30:10" or time_now == "08:30:11":#不知道是奇数还是偶数
            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            HealthCheckIn(time_send)#健康打卡

        time.sleep(2) # 停两秒
