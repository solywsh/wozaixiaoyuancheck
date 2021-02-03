# 我在校园自动打卡脚本

## 注意
- 由于Token有效期只有四天，所以每隔3天必须更换一次
- 西安石油大学我在校园自动打卡python脚本，源代码'我在校园晨签到.py'和'我在校园午签到.py'由网安协会完成，对此进行了修改合并为Check.py
 - 实现全天自动运行
 - 增加Token失效邮件提醒
 - 增加日志功能


## 使用方法

- 使用邮箱提醒
  - 下载`check.py`(晨检，午检，每日打卡一起)或者`每日健康打卡.py`(只有每日健康打卡)。
- 使用微信推送(推荐)
  - 下载`Check_pushplus.py`(晨检，午检，每日打卡一起)或者`每日健康打卡_pushplus.py`(只有每日健康打卡)。

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
### 微信推送

在 [push+](http://pushplus.hxtrip.com/)登陆后得到一个Token，在`Check_pushplus.py`或者`每日健康打卡_pushplus.py`中替换自己的token

```python
pushplus_token = '你的Token'
```



### 更换我在校园的token

将Token更换为自己的即可。后面几个函数自动统一更换。

```python 
wozaixiaoyuan_token = "93235013-73be-40c2-b2e7-2a0542d912bb"  #这里把token_code的内容换为你自己的token
```
### 更换地址

我在校园定位调用的腾讯地图的api，`https://apis.map.qq.com`。

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
在健康打卡`def HealthCheckIn(time)`中精度到行政区即可

```python
Hpostdata = {
        'answers' : '["0","36.5"]',
        'latitude' : '34.108216',
        'longitude' : '108.605084',
        'country' : '中国',
        'city' : '西安市',
        'district' : '鄠邑区',
        'province' : '陕西省',
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


