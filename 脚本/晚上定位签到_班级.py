import datetime
import json
import pprint
import time
import requests

# 我在校园jwsession,抓包获得
jwsession = ""
# 在pushplus网站中可以找到 http://pushplus.hxtrip.com/
pushplus_token = ''


def pushplus_post(content, title="今日班级打卡情况"):
    url = 'http://pushplus.hxtrip.com/send'
    data = {
        "token": pushplus_token,
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)


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
                    pushplus_post("未打卡名单:" + name_str)
                else:
                    pushplus_post("已经全部打卡")
                time.sleep(10)
                break
        # 签到是今天但是签到没有开始，静默等待
        elif res == -2:
            time.sleep(10)
        elif res == -3:
            pushplus_post("已过签到时间")
            break
        elif res == -1:
            pushplus_post("签到未发布或今天没有签到")
            break


def main():
    while True:
        week_day_now = time.strftime("%w", time.localtime())
        # 排除星期天
        if week_day_now != "0":
            time_now = time.strftime("%H:%M:%S", time.localtime())
            if time_now == "22:40:00" or time_now == "22:40:01":
                operate_event()  # 打卡
        # 星期天的情况下
        else:
            time_now = time.strftime("%H:%M:%S", time.localtime())
            if time_now == "22:40:00" or time_now == "22:40:01":
                operate_event(2)  # 返回名单不打卡
        time.sleep(2)


if __name__ == "__main__":
    main()
