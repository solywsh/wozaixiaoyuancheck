# encoding:utf-8
import datetime
import json
import pprint
import random
import time

import requests
import hashlib
# import ast #字符转字典 user_dict = ast.literal_eval(user)


# 自己的pushplus token，在pushplus网站中可以找到 http://pushplus.hxtrip.com/
pushplus_token = ""
jwsession = ""
user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x1800103a) NetType/WIFI Language/zh_CN'


def pushplus_post(title, content):
    url = 'http://pushplus.hxtrip.com/send'
    data = {
        "token": pushplus_token,
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)


def unchecked_list_health(date):
    headers = {
        "jwsession": jwsession,
        'user-agent': user_agent
    }
    hpostdata = {
        'type': '0',
        'date': date,
    }
    url = 'https://student.wozaixiaoyuan.com/health/getHealthUsers.json'
    s = requests.session()
    r = s.post(url, data=hpostdata, headers=headers)
    ts = json.loads(r.text)  # 转为字典
    phone_list = []
    name_list = ''
    for t in ts['data']:
        phone_list.append('+86' + t['phone'])
        name_list = name_list + t['name'] + ' '
        print(t['name'])
    pushplus_post("班级健康打卡提醒", "未打卡名单:" + name_list)


def unchecked_list_morning(date):
    headers = {
        "jwsession": jwsession,
        'user-agent': user_agent
    }
    hpostdata = {
        'seq': '1',
        'date': date,
        'type': '0'
    }
    url = 'https://student.wozaixiaoyuan.com/heat/getHeatUsers.json'
    s = requests.session()
    r = s.post(url, data=hpostdata, headers=headers)

    ts = json.loads(r.text)  # 转为字典
    if ts['code'] != -10:
        phone_list = []
        name_list = ''
        for t in ts['data']:
            phone_list.append('+86' + t['phone'])
            name_list = name_list + t['name'] + ' '
            print(t['name'] + ':' + t['userId'])
            morning_check_for_classmate(t['userId'])
            time.sleep(2)
        pushplus_post("班级晨检未打卡提醒", "未打卡名单:" + name_list)
    else:
        pushplus_post("班级晨检未打卡提醒", "jwsession可能失效!")


def unchecked_list_afternoon(date):
    headers = {
        "jwsession": jwsession,
        'user-agent': user_agent
    }
    hpostdata = {
        'seq': '2',
        'date': date,
        'type': '0'
    }
    url = 'https://student.wozaixiaoyuan.com/heat/getHeatUsers.json'
    s = requests.session()
    r = s.post(url, data=hpostdata, headers=headers)
    ts = json.loads(r.text)  # 转为字典
    if ts['code'] != -10:
        phone_list = []
        name_list = ''
        for t in ts['data']:
            phone_list.append('+86' + t['phone'])
            name_list = name_list + t['name'] + ' '
            print(t['name'] + ':' + t['userId'] + ' ' + t['number'])
            afternoon_check_for_classmate(t['userId'])
            time.sleep(2)
        pushplus_post("班级午检未打卡提醒", "未打卡名单:" + name_list)
    else:
        pushplus_post("班级午检未打卡提醒", "jwsession可能失效!")


def health_check_in():
    headers = {
        "jwsession": jwsession,
        'user-agent': user_agent
    }
    sign_time = int(round(time.time() * 1000))  # 13位
    content = f"陕西省_{sign_time}_西安市"
    signatureHeader = hashlib.sha256(content.encode('utf-8')).hexdigest()

    hpostdata = {
        'answers': '["0"]',
        'seq': '1',
        'temperature': '36.5',
        'userid': '',
        'latitude': '34.108216',
        'longitude': '108.605084',
        'country': '中国',
        'city': '西安市',
        'district': '鄠邑区',
        'province': '陕西省',
        'township': '甘亭街道',
        'street': '东街',
        'myArea': '610118',
        'timestampHeader': str(sign_time),
        'signatureHeader': signatureHeader
    }
    url = 'https://student.wozaixiaoyuan.com/health/save.json'
    s = requests.session()
    r = s.post(url, data=hpostdata, headers=headers)
    r_json = json.loads(r.text)
    if r_json['code'] == 0:
        pushplus_post("个人健康打卡打卡提醒", "打卡成功")
    else:
        pushplus_post("个人健康打卡打卡提醒", "打卡失败,返回信息为:{0}".format(str(r_json)))


def morning_check():
    headers = {
        "jwsession": jwsession,
        'user-agent': user_agent
    }
    hpostdata = {
        'answers': '["0"]',
        'seq': '1',
        'temperature': '36.5',
        'userid': '',
        'latitude': '34.108216',
        'longitude': '108.605084',
        'country': '中国',
        'city': '西安市',
        'district': '鄠邑区',
        'province': '陕西省',
        'township': '甘亭街道',
        'street': '东街',
        'myArea': '610118',
        "timestampHeader": str(int(time.time() * 1000))
    }
    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url, data=hpostdata, headers=headers)
    # 经过测试，t返回的字典里会有一个状态码，登陆成功为0，不成功为-10，对应的就是第8个字符。
    r_json = json.loads(r.text)
    if r_json['code'] == 0:
        pushplus_post("个人晨检提醒", "打卡成功")
    else:
        pushplus_post("个人晨检提醒", "打卡失败,返回信息为:" + str(r_json))


def noon_inspection():
    headers = {
        "jwsession": jwsession,
        'user-agent': user_agent
    }
    sign_time = int(round(time.time() * 1000))  # 13位
    content = f"陕西省_{sign_time}_西安市"
    signatureHeader = hashlib.sha256(content.encode('utf-8')).hexdigest()

    hpostdata = {
        'answers': '["0"]',
        'seq': '2',
        'temperature': '36.5',
        'userid': '',
        'latitude': '34.108216',
        'longitude': '108.605084',
        'country': '中国',
        'city': '西安市',
        'district': '鄠邑区',
        'province': '陕西省',
        'township': '甘亭街道',
        'street': '东街',
        'myArea': '610118',
        'timestampHeader': str(sign_time),
        'signatureHeader': signatureHeader
    }
    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url, data=hpostdata, headers=headers)
    r_json = json.loads(r.text)
    if r_json['code'] == 0:
        pushplus_post("个人午检打卡提醒", "打卡成功")
    else:
        pushplus_post("个人午检打卡提醒", "打卡失败,返回信息为:" + str(r_json))


def morning_check_for_classmate(userid):
    sign_time = int(round(time.time() * 1000))  # 13位
    content = f"陕西省_{sign_time}_西安市"
    signatureHeader = hashlib.sha256(content.encode('utf-8')).hexdigest()
    headers = {
        "jwsession": jwsession,
        'user-agent': user_agent
    }
    hpostdata = "answers=%5B%220%22%5D&seq=1&temperature=36.0&userId=" + str(
        userid) + "&latitude=&longitude=&country=&city=&district=&province=&township=&street=&areacode=&timestampHeader=" + str(
        sign_time) + "&signatureHeader=" + signatureHeader

    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url, data=hpostdata, headers=headers)
    print(r.text)


def afternoon_check_for_classmate(userid):
    sign_time = int(round(time.time() * 1000))  # 13位
    content = f"陕西省_{sign_time}_西安市"
    signatureHeader = hashlib.sha256(content.encode('utf-8')).hexdigest()
    headers = {
        "jwsession": jwsession,
        'user-agent': user_agent
    }
    hpostdata = "answers=%5B%220%22%5D&seq=2&temperature=36.0&userId=" + str(
        userid) + "&latitude=&longitude=&country=&city=&district=&province=&township=&street=&areacode=&timestampHeader=" + str(
        sign_time) + "&signatureHeader=" + signatureHeader

    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url, data=hpostdata, headers=headers)
    print(r.text)


##############################################################
# 晚上定位签到
def get_sign_message():
    headers = {
        "jwsession": jwsession
    }
    post_data = {
        "page": 1,
        "size": 5
    }
    url = "https://student.wozaixiaoyuan.com/sign/getSignMessage.json"
    s = requests.session()
    r = s.post(url, data=post_data, headers=headers)
    r_json = json.loads(r.text)
    if r_json['code'] == 0:
        return r_json['data'][0]
    else:
        pushplus_post("签到提醒", "jwsession失效!")
        return 404


def do_sign(sign_message):
    if sign_message == 404:
        return 404
    headers = {
        "jwsession": jwsession
    }
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

    url = "https://student.wozaixiaoyuan.com/sign/doSign.json"
    s = requests.session()
    r = s.post(url, data=json.dumps(post_data), headers=headers)
    r_json = json.loads(r.text)
    if r_json['code'] == 0:
        pushplus_post("签到提醒", "签到成功")
    else:
        pushplus_post("签到提醒", "签到失败,返回信息为:" + str(r_json))


def contrast_date(sign_message):
    # 得到签到的日期和时间
    sign_date_str = str(sign_message['start']).split(" ")[0]
    sign_time_str_start = str(sign_message['start']).split(" ")[1]
    sign_time_str_end = str(sign_message['end']).split(" ")[1]

    # 得到系统的日期和时间
    sys_time_info = datetime.datetime.now()
    sys_date_now = sys_time_info.date()
    sys_time_now = time.strftime("%H:%M", time.localtime())

    # 判断打卡的日期和今天的日期是否相同
    if str(sys_date_now) == sign_date_str:
        # 判断系统时间是否在打卡时间区间
        if sign_time_str_start <= sys_time_now <= sign_time_str_end:
            return 0
        elif sys_time_now <= sign_time_str_start:
            return -2
        elif sys_time_now >= sign_time_str_end:
            return -3
    else:
        return -1


##################################
# 班级晚上定位签到

# 得到签到列表（此列表为没有）
def get_list():
    headers = {
        "jwsession": jwsession
    }
    post_data = {
        "keyword": "",
        "page": 1
    }
    url = "https://student.wozaixiaoyuan.com/gradeManage/sign/getList.json"
    s = requests.session()
    r = s.post(url, data=post_data, headers=headers)
    r_json = json.loads(r.text)
    if r_json['code'] == 0:
        # pprint.pprint(r_json)
        return r_json['data'][0]
    else:
        return 404


# 对比签到时间
def contrast_date_class(sign_message):
    # 得到签到的日期和时间
    if sign_message == 404:
        return 404, 0

    sign_date_str = str(sign_message['start']).split(" ")[0]
    sign_time_str_start = str(sign_message['start']).split(" ")[1]
    sign_time_str_end = str(sign_message['end']).split(" ")[1]

    # 得到系统的日期和时间
    sys_time_info = datetime.datetime.now()
    sys_date_now = sys_time_info.date()
    sys_time_now = time.strftime("%H:%M", time.localtime())

    # 判断打卡的日期和今天的日期是否相同
    if str(sys_date_now) == sign_date_str:
        # 判断系统时间是否在打卡时间区间
        if sign_time_str_start <= sys_time_now <= sign_time_str_end:
            return 0, sign_message['id']
        elif sys_time_now <= sign_time_str_start:
            return -2, 0
        elif sys_time_now >= sign_time_str_end:
            return -3, 0
    else:
        return -1, 0


# 返回未签到名单
def get_sign_result(sign_id):
    headers = {
        "jwsession": jwsession
    }
    post_data = {
        "id": sign_id
    }
    url = "https://student.wozaixiaoyuan.com/gradeManage/sign/getSignResult.json"
    s = requests.session()
    r = s.post(url, data=post_data, headers=headers)
    r_json = json.loads(r.text)
    if r_json['code'] == 0:
        pprint.pprint(r_json['data']["notSign"])
        return r_json['data']["notSign"]
    else:
        return 404


def do_sign_class(stu_sign_id):
    headers = {
        "jwsession": jwsession
    }
    post_data = {
        "id": stu_sign_id,
        "type": 1
    }
    url = "https://student.wozaixiaoyuan.com/gradeManage/sign/leaderSign.json"
    s = requests.session()
    r = s.post(url, data=post_data, headers=headers)
    r_json = json.loads(r.text)
    if r_json['code'] == 0:
        return 0
    else:
        return 404


def leader_sign(not_sign_list, flag=1):
    # 设立标志位用于区分周末，如果周末就不打卡，只是返回名单
    name_list = []
    for not_sign in not_sign_list:
        if flag == 1:
            do_sign_class(not_sign['id'])
        name_list.append(not_sign['name'])
    return name_list


# 打卡事件操作
def operate_event(flag=1):
    # 设立标志位用于区分周末，如果周末就不打卡，只是返回名单
    while True:
        res, sign_id = contrast_date_class(get_list())
        if res == 0:
            not_sign_list = get_sign_result(sign_id)
            if not_sign_list != 404:
                not_sign_name = leader_sign(not_sign_list, flag)
                if len(not_sign_name) != 0:
                    name_str = ""
                    for name in not_sign_name:
                        name_str = name_str + name + " "
                    pushplus_post("今日班级打卡情况", "未打卡名单:" + name_str)
                else:
                    pushplus_post("今日班级打卡情况", "已经全部打卡")
                time.sleep(10)
                break
        # 签到是今天但是签到没有开始，静默等待
        elif res == -2:
            time.sleep(10)
        elif res == -3:
            pushplus_post("今日班级打卡情况", "已过签到时间")
            break
        elif res == -1:
            pushplus_post("今日班级打卡情况", "签到未发布或今天没有签到")
            break


def main():
    week_day_flag = -1
    morning_check_time = ""
    _morning_check_time = ""
    afternoon_check_time = ""
    _afternoon_check_time = ""
    evening_check_time = ""
    _evening_check_time = ""
    while True:
        week_day_now = time.strftime("%w", time.localtime())
        # 新的一天重新生成随机时间
        if week_day_now != week_day_flag:
            time_sec = random.randrange(1, 8, 2)
            morning_check_time = "07:{}{}:{}".format(str(random.randint(0, 5)), str(random.randint(0, 9)),
                                                     str(random.randint(0, 5)))
            _morning_check_time = morning_check_time + str(time_sec + 1)
            morning_check_time = morning_check_time + str(time_sec)
            print(morning_check_time, _morning_check_time)

            time_sec = random.randrange(1, 8, 2)  # 重新生成秒数
            afternoon_check_time = "11:{}{}:{}".format(str(random.randint(3, 5)), str(random.randint(0, 9)),
                                                       str(random.randint(0, 5)))
            _afternoon_check_time = afternoon_check_time + str(time_sec + 1)
            afternoon_check_time = afternoon_check_time + str(time_sec)
            print(afternoon_check_time, _afternoon_check_time)

            time_sec = random.randrange(1, 8, 2)
            evening_check_time = "21:{}{}:{}".format(str(random.randint(4, 5)), str(random.randint(0, 9)),
                                                     str(random.randint(0, 5)))
            _evening_check_time = evening_check_time + str(time_sec + 1)
            evening_check_time = evening_check_time + str(time_sec)
            print(evening_check_time, _evening_check_time)
            print(week_day_flag, week_day_now)
            week_day_flag = week_day_now
            # 刷新时间
        time_now = time.strftime("%H:%M:%S", time.localtime())
        # 晨检
        if time_now == morning_check_time or time_now == _morning_check_time:
            morning_check()
            time.sleep(10)
        # 午检
        if time_now == afternoon_check_time or time_now == _afternoon_check_time:
            noon_inspection()
            time.sleep(10)
        # # 晨检未打卡名单并提醒
        # if time_now == "09:50:00" or time_now == "09:50:01":
        #     time_data = time.strftime("%Y%m%d")
        #     unchecked_list_morning(time_data)
        #     unchecked_list_morning(time_data)  # 检查两次，会出现第一次打卡不完整的情况
        #
        # # 午检未打卡名单并提醒
        # if time_now == "14:50:00" or time_now == "14:50:01":
        #     time_data = time.strftime("%Y%m%d")
        #     unchecked_list_afternoon(time_data)
        #     unchecked_list_afternoon(time_data)

        # 晚上定位签到
        if time_now == evening_check_time or time_now == _evening_check_time:
            # 得到最新的签到信息
            sign_info = get_sign_message()
            if sign_info == 404:
                time.sleep(4)
                continue
            # 比对签到信息
            time_code = contrast_date(sign_info)
            if time_code == 0:
                do_sign(sign_info)
                time.sleep(10)
            elif time_code == -2:
                # 签到是今天但是签到没有开始，静默等待
                while time_code == 0:
                    time.sleep(10)
                    time_code = contrast_date(sign_info)
                # 时间开始之后执行签到
                do_sign(sign_info)
                time.sleep(10)
            elif time_code == -3:
                pushplus_post("签到提醒", "已过签到时间")
            elif time_code == -1:
                pushplus_post("签到提醒", "签到未发布或今天没有签到")

        # 班级晚上定位签到
        # # 排除星期天
        # if week_day_now != "0":
        #     time_now = time.strftime("%H:%M:%S", time.localtime())
        #     if time_now == "22:40:00" or time_now == "22:40:01":
        #         operate_event()  # 打卡
        # # 星期天的情况下
        # else:
        #     time_now = time.strftime("%H:%M:%S", time.localtime())
        #     if time_now == "22:40:00" or time_now == "22:40:01":
        #         operate_event(2)  # 返回名单不打卡
        time.sleep(2)  # 停两秒


if __name__ == "__main__":
    main()
