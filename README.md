# 我在校园自动打卡脚本

## 注意

- ~~由于Token有效期只有四天，所以每隔3天必须更换一次。~~现在已经换成jwsession，并且可以实现基本上不更换
- 实现全天自动运行
- 增加Token失效邮件提醒(2021年12月23日更新：在一些脚本里边还有，但是现在建议使用pushplus版本)
- ~~增加日志功能~~(2021年12月23日更新：我也不知道哪里加了)

## 使用方法

### 最新版本

> 以下版本为班长（安全委员版本）版本，2021年12月23日更新
> 新增晚上定位签到，并且对所有功能做了整合

打开`check_all.py`文件，需要填入的只有:

```python
pushplus_token = ''  # pushplus的token
jwsession = ""  # 我在校园的jwsession
```

然后在服务器运行即可

### 启用对应功能(初始版本)

> 以下版本为最初版本

- 使用邮箱提醒
  - 下载`check.py`
- 使用微信推送(推荐)
  - 下载`Check_pushplus.py`

默认只开启了健康打卡，由于在学校期间不需要晨检和午检，所以给注释掉了，想要打开是取消注释即可。

```diff
while True:
        time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
        if time_now == "06:30:10" or time_now == "06:30:11":#不知道是奇数还是偶数
            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            health_check_in(time_send)#健康打卡
-           #morning_check(time_now)#晨检
+           #morning_check(time_now)#晨检
      
-        # if time_now == "11:20:10" or time_now == "11:20:11":
-        #     time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
-        #     noon_inspection(time_send)#午检
+        if time_now == "11:20:10" or time_now == "11:20:11":
+            time_send = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
+            noon_inspection(time_send)#午检
            
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

在健康打卡`def health_check_in(time)`中精度到行政区即可

```python
Hpostdata = {
  'answers': '["0","36.5"]',
  'latitude': '34.108216',
  'longitude': '108.605084',
  'country': '中国',
  'city': '西安市',
  'district': '鄠邑区',
  'province': '陕西省',
  'areacode': '610118'
}
```

### 更换打卡时间

这里设置的事早上6:30和中午12:00

```python
if time_now == "06:30:10" or time_now == "06:30:11":  # 不知道是奇数还是偶数
  health_check_in()  # 健康打卡
  morning_check()  # 晨间
  subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 晨间打卡/健康"

if time_now == "11:20:10" or time_now == "11:20:11":
  noon_inspection()  # 午检
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





