'''
Author: your name
Date: 2021-01-08 13:43:00
LastEditTime: 2021-01-08 13:44:10
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \undefinedc:\Users\A\Desktop\我在校园晨签到.py
'''
import requests

def HealthCheckIn():
    headers = {
        'content-length' : '296',
        'cookie' : 'SESSION=NGY4ZGYwNGMtZTQ3ZC00ZDRmLTg2MmEtNDRhMDYyOTZlYTAw;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : '9037a8cd-69e2-4e1e-aa8d-9b9f82c66f30',
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


def MorningCheck():
    headers = {
        'content-length' : '306',
        'cookie' : 'SESSION=NGY4ZGYwNGMtZTQ3ZC00ZDRmLTg2MmEtNDRhMDYyOTZlYTAw;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : '9037a8cd-69e2-4e1e-aa8d-9b9f82c66f30',
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

if __name__ == "__main__":
    HealthCheckIn()
    MorningCheck()
