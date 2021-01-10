# 我在校园自动打卡脚本

## 注意
- 由于Token有效期只有四天，所以每隔3天必须更换一次
- 西安石油大学我在校园自动打卡python脚本，源代码'我在校园晨签到.py'和'我在校园午签到.py'由网安协会完成，对此进行了修改合并为Check.py
 - 实现全天自动运行
 - 增加Token失效邮件提醒
 - 增加日志功能


## 使用方法

- 只需下载check.py即可

### 邮箱部分

邮箱使用的网易的SMTP

```python 
mail_host = "smtp.163.com"        # SMTP服务器
mail_user = "@163.com" # 用户名为邮箱
mail_pass = ""    # 授权密码，非登录密码 
sender = '@163.com'    # 发件人邮箱
receivers = ['@outlook.com']  # 接收邮件
title = '我在校园自动打卡提醒'  # 邮件主题
```
### 更换token
将Token更换即可，总共需要更换三处，分别为晨检，午检，每日健康打卡
```python 
def HealthCheckIn():
    headers = {
        'content-length' : '296',
        'cookie' : 'SESSION=NGY4ZGYwNGMtZTQ3ZC00ZDRmLTg2MmEtNDRhMDYyOTZlYTAw;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : '这里换为你的Token',
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/143/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br'
    }
```
### 更换地址
```python 
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
```
### 更换打卡时间
这里设置的事早上6:30和中午12:00
```python
if time_now == "06:30:10" or time_now == "06:30:11":#不知道是奇数还是偶数
            HealthCheckIn()#健康打卡
            MorningCheck()#晨间
            subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 晨间打卡/健康"
            
        
if time_now == "11:20:10" or time_now == "11:20:11":
            NoonInspection()#午检
            subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 午检打卡"
```


