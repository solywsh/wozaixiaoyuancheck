#encoding:utf-8
import json
import requests
import time
import os
#import ast #字符转字典 user_dict = ast.literal_eval(user)


# #这里把_wozaixiaoyuan的内容换为你自己的token，自行抓包或者看https://violetwsh.com/2021/01/10/wozaixiaoyuan/#more
# wozaixiaoyuan_token = "5ae71543-56f8-40ac-b747-503d1835e3c4"
# #自己的pushplus token，在pushplus网站中可以找到 http://pushplus.hxtrip.com/
# my_pushplus_token = 'a6265a189e994e74bf6ab24587bb8891'

invalid_token = []
user_sent = []

def check(hour_now, min_now):
    import os
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = path + r"/config/"
    files = os.listdir(path)
    for file in files:
        with open(path + file,"r", encoding='utf-8') as f:
            info_dict = json.load(f)
            # if (hour_now >= 0) and (info_dict['health_check_self']):
            #     health_check_in(info_dict['WoZaiStudent_Token'], info_dict['PushPlus_token'], info_dict['receive_message'])#健康打卡
            # if hour_now >= 6 and hour_now <= 10:
            #     if info_dict['morning_check_self']:
            #         morning_check(info_dict['WoZaiStudent_Token'], info_dict['PushPlus_token'], info_dict['receive_message'])#晨检
            # if (info_dict['morning_check_class']) and ((hour_now==9)and(min_now>=40)):
            #         time_data = time.strftime("%Y%m%d")
            #         unchecked_list_morning(time_data, info_dict['WoZaiStudent_Token'], info_dict['PushPlus_token'])
            #         time.sleep(5)#暂停等待更新名单
            #         unchecked_list_morning(time_data, info_dict['WoZaiStudent_Token'], info_dict['PushPlus_token'])#检查两次，会出现第一次打卡不完整的情况
            # if hour_now >= 11 and hour_now <= 15:
            #     if info_dict['afternoom_check_self']:
            #         noon_inspection(info_dict['WoZaiStudent_Token'], info_dict['PushPlus_token'], info_dict['receive_message'])#午检
            # if (info_dict['afternoom_check_class']) and ((hour_now==14)and(min_now>=40)):
            #         time_data = time.strftime("%Y%m%d")
            #         unchecked_list_afternoon(time_data, info_dict['WoZaiStudent_Token'], info_dict['PushPlus_token'])
            #         time.sleep(5)#暂停等待更新名单
            #         unchecked_list_afternoon(time_data, info_dict['WoZaiStudent_Token'], info_dict['PushPlus_token'])
            if hour_now >= 21:
                if (hour_now == 23 and min_now <= 30) or hour_now <= 22:
                    if info_dict['night_check_self']:
                        NightCheckIn(info_dict['WoZaiStudent_Token'], info_dict['PushPlus_token'], info_dict['receive_message'])#晚检
            if (info_dict['night_check_class']) and ((hour_now==23)and(min_now>=10)):
                    time_data = time.strftime("%Y%m%d")
                    Unchecked_list_night(time_data, info_dict['WoZaiStudent_Token'], info_dict['PushPlus_token'])
                    time.sleep(5)#暂停等待更新名单
                    Unchecked_list_night(time_data, info_dict['WoZaiStudent_Token'], info_dict['PushPlus_token'])
        f.close()



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
    
def NightCheckIn(token, pushplus_token, send):
    headers = {
        'token' : token,
    }
    Mpostdata = {
        'answers' : '["0"]',
        'seq' : '3',
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
    url1 = 'https://student.wozaixiaoyuan.com/heat/getHeat.json'
    s = requests.session()
    r1 = s.post(url1, data=Mpostdata,headers=headers)
    t1 = r1.text
    dic = json.loads(t1)
    if dic['code'] == 0:
        checked = dic['data']['titles'][0]['heatOptions'][0]['select'] #是否已打卡
        if checked:
            return
        else:
            r = s.post(url, data=Mpostdata,headers=headers)
            t = r.text
            code = json.loads(t)
            if send:
                if code['code'] == '0':
                    pushplus_post("晚检打卡提醒","打卡成功",pushplus_token)
    elif dic['code'] == -1:
        if token in invalid_token:
            return
        else:
            invalid_token.append(token)
            pushplus_post("晚检打卡提醒","打卡失败，可能是token失效，请尽快重新输入。",pushplus_token)
            
def Unchecked_list_night(date, token, pushplus_token):
    headers = {
        'token' : token,
    }
    Hpostdata = {
        'seq':'3',
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
            MorningCheck_for_classmate(t['userId'], token)
            #yiban_send_msg(t['number'] , 1)
            time.sleep(2)
        #短信发送
        #sent_msg(phone_list)
        #给我发一份
        if token in user_sent:
            return
        else:
            user_sent.append(token)
            pushplus_post("晚检未打卡名单",name_list,pushplus_token)
        #给安全委员发一份
        #pushplus_post("晨检未打卡名单",name_list,safe_token)
    else:
        if token in invalid_token:
            return
        else:
            invalid_token.append(token)
            pushplus_post("晚检未打卡名单","Token失效！",pushplus_token)

# def unchecked_list_health(date):
#     headers = {
#         'token' : wozaixiaoyuan_token,
#     }
#     Hpostdata = {
#         'type' : '0',
#         'date' : date,
#     }
#     url = 'https://student.wozaixiaoyuan.com/health/getHealthUsers.json'
#     s = requests.session()
#     r = s.post(url, data=Hpostdata,headers=headers)
#     ts = json.loads(r.text)#转为字典
#     phone_list=[]
#     name_list=''
#     for t in ts['data']:
#         phone_list.append('+86'+t['phone'])
#         name_list = name_list + t['name']+' '
#         print(t['name'])
#     #短信发送
#     #sent_msg(phone_list)
#     #给我发一份
#     pushplus_post("健康打卡未打卡名单",name_list,my_pushplus_token)
#     #给安全委员发一份
#     #pushplus_post("健康打卡未打卡名单",name_list,safe_token)

def Unchecked_list_morning(date, token, pushplus_token):
    headers = {
        'token' : token,
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
            MorningCheck_for_classmate(t['userId'], token)
            #yiban_send_msg(t['number'] , 1)
            time.sleep(2)
        #短信发送
        #sent_msg(phone_list)
        #给我发一份
        if token in user_sent:
            return
        else:
            user_sent.append(token)
            pushplus_post("晨检未打卡名单",name_list,pushplus_token)
        #给安全委员发一份
        #pushplus_post("晨检未打卡名单",name_list,safe_token)
    else:
        if token in invalid_token:
            return
        else:
            invalid_token.append(token)
            pushplus_post("晨检未打卡名单","Token失效！",pushplus_token)

def Unchecked_list_afternoon(date, token, pushplus_token):
    headers = {
        'content-length' : '20',
        #'cookie' : 'SESSION=ZGEwY2FkOWYtZGU1My00Njk3LTgzMzctMjllMjRjMTM4YTY3;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : token,
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
            AfternoonCheck_for_classmate(t['userId'], token)
            time.sleep(2)
        #短信发送
        #sent_msg(phone_list)
        #给我发一份
        if token in user_sent:
            return
        else:
            user_sent.append(token)
            pushplus_post("午检未打卡名单",name_list,pushplus_token)
        #给安全委员发一份
        #pushplus_post("午检未打卡名单",name_list,safe_token)
    else:
        if token in invalid_token:
            return
        else:
            invalid_token.append(token)
            pushplus_post("午检未打卡名单","Token失效！",pushplus_token)

# def yiban_send_msg(sid,code):
#     content_key = ''
#     if code == 1:
#         content_key = '晨检'
#     if code == 2:
#         content_key = '午检'
#     if code == 0:
#         content_key = '健康打卡'
#     postdata = {
#         'key':'wsh',
#         'secret':'111',
#         'sid':sid,
#         'title':'我在校园打卡提醒',
#         'content':'你没有'+content_key,
#         'url':'www.xapi.edu.cn'
#     }
#     url = 'http://z-6ggqgne8c25875ce-1258898586.ap-shanghai.app.tcloudbase.com/sendMessage'
#     r = requests.get(url, params=postdata)
#     print(r.text)

def HealthCheckIn(token, pushplus_token, send):
    headers = {
        'token' : token,
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
    url1 = 'https://student.wozaixiaoyuan.com/health/getToday.json'
    s = requests.session()
    r1 = s.post(url1, headers=headers)
    t1 = r1.text
    dic = json.loads(t1)
    if dic['code'] == 0:
        checked = dic['data']['titles'][0]['healthOptions'][0]['select'] #是否已打卡
        if checked:
            return
        else:
            r = s.post(url, data=Hpostdata,headers=headers)
            t = r.text
            if send:
                if t[8] == '0' :
                    # print("健康打卡成功！")
                    pushplus_post("每日打卡提醒","打卡成功",pushplus_token)
    elif dic['code'] == -1:
        if token in invalid_token:
            return
        else:
            invalid_token.append(token)
            pushplus_post("每日打卡提醒","打卡失败，可能是token失效，请尽快重新输入。",pushplus_token)
    
def MorningCheck(token, pushplus_token, send):
    headers = {
        'token' : token,
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
    url1 = 'https://student.wozaixiaoyuan.com/heat/getHeat.json'
    s = requests.session()
    r1 = s.post(url1, data=Mpostdata,headers=headers)
    t1 = r1.text
    dic = json.loads(t1)
    if dic['code'] == 0:
        checked = dic['data']['titles'][0]['heatOptions'][0]['select'] #是否已打卡
        if checked:
            return
        else:
            r = s.post(url, data=Mpostdata,headers=headers)
            t = r.text
            if send:
                if t[8] == '0' :
                    # print("健康打卡成功！")
                    pushplus_post("晨检打卡提醒","打卡成功",pushplus_token)
    elif dic['code'] == -1:
        if token in invalid_token:
            return
        else:
            invalid_token.append(token)
            pushplus_post("晨检打卡提醒","打卡失败，可能是token失效，请尽快重新输入。",pushplus_token)

def NoonInspection(token, pushplus_token, send):
    headers = {
        'token' : token,
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
    url1 = 'https://student.wozaixiaoyuan.com/heat/getHeat.json'
    s = requests.session()
    r1 = s.post(url1, data=postdata,headers=headers)
    t1 = r1.text
    dic = json.loads(t1)
    #print('运行正常')
    if dic['code'] == 0:
        checked = dic['data']['titles'][0]['heatOptions'][0]['select'] #是否已打卡
        if checked:
            return
        else:
            r = s.post(url, data=postdata,headers=headers)
            t = r.text
            if send:
                if t[8] == '0' :
                    # print("健康打卡成功！")
                    pushplus_post("午检打卡提醒","打卡成功",pushplus_token)
    elif dic['code'] == -1:
        if token in invalid_token:
            return
        else:
            invalid_token.append(token)
            pushplus_post("午检打卡提醒","打卡失败，可能是token失效，请尽快重新输入。",pushplus_token)

def MorningCheck_for_classmate(userid, token):
    headers = {
        'Host' : 'student.wozaixiaoyuan.com',
        'content-type' : 'application/x-www-form-urlencoded',
        'Accept' : '*/*',
        'Accept-Language' : 'zh-cn',
        'Accept-encoding' : 'gzip, deflate, br',   
        'Cookie' : 'JWSESSION=fac47cd53709450e959c9f74347206fe; path=/;',
        'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.2(0x18000237) NetType/WIFI Language/zh_CN',
        'Referer' : 'https://servicewechat.com/wxce6d08f781975d91/166/page-frame.html',
        'token' : token,
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

def AfternoonCheck_for_classmate(userid, token):
    headers = {
        'Host' : 'student.wozaixiaoyuan.com',
        'content-type' : 'application/x-www-form-urlencoded',
        'Accept' : '*/*',
        'Accept-Language' : 'zh-cn',
        'Accept-encoding' : 'gzip, deflate, br',   
        'Cookie' : 'JWSESSION=fac47cd53709450e959c9f74347206fe; path=/;',
        'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.2(0x18000237) NetType/WIFI Language/zh_CN',
        'Referer' : 'https://servicewechat.com/wxce6d08f781975d91/166/page-frame.html',
        'token' : token,
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

if __name__ == "__main__":
    while True:
        hour_now = int(time.strftime("%H", time.localtime())) # 刷新
        min_now = int(time.strftime("%M", time.localtime()))
        time_now = time.strftime("%H:%M", time.localtime())
        time_now_with_sec = time.strftime("%H:%M:%S", time.localtime())
        if time_now_with_sec == "23:58:00" or time_now_with_sec == "23:59:00":
            invalid_token.clear()
        if time_now == "10:01" or time_now == "10:02" or time_now == "15:01" or time_now == "15:02":
            user_sent.clear()
        #print('运行正常')
        check(hour_now, min_now)
        time.sleep(2) # 停两秒