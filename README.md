# 我在校园自动打卡脚本

## 注意
- 由于Token有效期只有四天，所以每隔3天必须更换一次
- 西安石油大学我在校园自动打卡python脚本，源代码`我在校园晨签到.py`和`我在校园午签到.py`由网安协会完成，对此进行了修改合并为Check.py
 - 实现全天自动运行
 - 增加Token失效邮件提醒
 - 增加日志功能


## 使用方法

- 使用邮箱提醒
  - 下载`check.py`
- 使用微信推送(推荐)
  - 下载`Check_pushplus.py`

### 启用对应功能

默认只开启了健康打卡，由于在学校期间不需要晨检和午检，所以给注释掉了，想要打开是取消注释即可。

```diff
while True:
        time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
        if time_now == "06:30:10" or time_now == "06:30:11":#不知道是奇数还是偶数
            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            HealthCheckIn(time_send)#健康打卡
-           #MorningCheck(time_now)#晨检
+           #MorningCheck(time_now)#晨检
      
-        # if time_now == "11:20:10" or time_now == "11:20:11":
-        #     time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
-        #     NoonInspection(time_send)#午检
+        if time_now == "11:20:10" or time_now == "11:20:11":
+            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
+            NoonInspection(time_send)#午检
            
        time.sleep(2) # 停两秒
```

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

## 班长特供版本

此版本可以查到班级本天没有打卡的人，`并且给班里的同学打卡`，但是需要班长或者更高权限的人的`token`。

班长版本提醒用的微信推送（需要使用邮箱提醒自行添加），使用方法和微信推送版本并没有差别。只需要填入班长的`我在校园的token`，希望收到消息的人的`pushplus token`

```python
#这里把_wozaixiaoyuan的内容换为你自己的token，自行抓包或者看https://violetwsh.com/2021/01/10/wozaixiaoyuan/#more
wozaixiaoyuan_token = ""
#自己的pushplus token，在pushplus网站中可以找到 http://pushplus.hxtrip.com/
my_pushplus_token = ''
#安全委员的pushplus token
#safe_token = ''
```

### 给安全委员发消息

有时候，你即使收到消息可能也会忘记提醒，这时需要其他人帮你，可以是安全委员或是其他任何人。只需要填入他的`pushplus_token`。~~一般情况下关闭即可，安全委员自己一般也不打卡的。~~

```diff
#取消注释并填入token
#安全委员的pushplus token
-#safe_token = ''
+safe_token = ''
```

在`Unchecked_list_*** (date)`函数末尾把对应的给取消注释

```diff
#给安全委员发一份
-#pushplus_post("未打卡名单",list_name,safe_token)
+pushplus_post("未打卡名单",list_name,safe_token)
```

# 新增网页部署，允许多个用户打卡

> 由于性能原因，对flask做了一些限制，可通过修改一下内容进行解除。

在`flaskrun.py`里找到装饰器`@app.route('/registered', methods=['GET', 'POST'])`的`def registered()`函数，里边有两个`if判断`:

- 限制2019级计算机学院外的人进行注册

```python
if str(form.StuId.data[0:8]) != '20190707':
            flash('该网站暂不对计算机学院2019级以外的人开放注册！')
            return redirect(url_for('registered'))
```

- 限制一个班只有一个人注册

```python
flag = find(form.StuId.data)
        if flag == 0:
            flash('你们班已经有人注册！请联系管理员')
            return redirect(url_for('registered'))
```

如果要解除限制，只需要注释掉即可。

# 晚上定位签到

在`签到`文件夹中的`mian.py`文件，补完下面两个内容:

```python
# 我在校园jwsession,抓包获得
jwsession = ""
# 在pushplus网站中可以找到 http://pushplus.hxtrip.com/
pushplus_token = ''
```

在`do_sign()`函数中的

```python
post_data = {
        "signId": str(sign_message['id']),
        "city": "西安市",
        "id": str(sign_message['logId']),
        "latitude": '34.10133361816406',
        "longitude": '108.65825653076172',
        "country": "中国",
        "district": "鄠邑区",
        "township": "五竹街道",
        "province": "陕西省"
    }
```

更换为自己的地址信息。

**注意**，由于默认使用的是自己定时执行脚本，就没有使用循环，如果需要使用循环一直执行，将`mian()`函数的注释给取消掉，原来的删掉即可。

