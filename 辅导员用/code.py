# encoding:utf-8
import datetime
import json
import time
import random
import requests


def daily_check(date, config_info, seq):
    page = 1
    headers = {
        "jwsession": config_info['jwsession'],
        'user-agent': config_info['user_agent']
    }
    new_sign_list = []
    unsign_name_list = []
    while True:
        hpostdata = {
            'seq': str(seq),
            'date': date,
            'type': '0',
            'page': page,
            'size': '20'
        }
        url = 'https://teacher.wozaixiaoyuan.com/heat/getHeatUsers.json'
        s = requests.session()
        r = s.post(url, data=hpostdata, headers=headers)
        # print(r.text)
        ts = json.loads(r.text)  # 转为字典
        if ts['code'] != -10:
            if len(ts['data']) == 0:
                if page == 1:
                    print("没有信息，已经全部打卡或者打卡未开始")
                    return
                break
            for t in ts['data']:
                print(t['name'], t['userId'], t['number'], t['phone'])
                new_sign_list.append(t['userId'])
                unsign_name_list.append(t['name'])
            page += 1
            time.sleep(0.5)
        else:
            print("失败,jwsession可能失效!")
            break
    random.shuffle(new_sign_list)  # 随机打乱
    sign_num = len(new_sign_list) - config_info["unsign_num"]
    flag_num = 0
    if sign_num > 0:
        print("开始执行打卡...")
        for stu_id in new_sign_list:
            if flag_num < sign_num:
                # print(stu_id)
                print(stu_id, flag_num)
                check_for_classmate(userid=stu_id, _seq=seq, jwsession=config_info['jwsession'],
                                    user_agent=config_info['user_agent'])
                flag_num += 1
                time.sleep(0.5)
            else:
                break
    else:
        print("设置的未打卡人数超出了现未打卡的人数!")


def check_for_classmate(userid, _seq, jwsession, user_agent):
    headers = {
        "jwsession": jwsession,
        'user-agent': user_agent
    }
    hpostdata = "answers=%5B%220%22%5D&seq=" + str(_seq) + "&temperature=36.0&userId=" + str(
        userid) + "&latitude=&longitude=&country=&city=&district=&province=&township=&street=&areacode=&timestampHeader=" + str(int(time.time() * 1000))
    url = 'https://teacher.wozaixiaoyuan.com/heat/save.json?' + hpostdata
    s = requests.session()
    r = s.get(url, headers=headers)
    print(r.text)


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


# 得到签到列表（此列表为没有）
def get_list(jwsession):
    headers = {
        "jwsession": jwsession
    }
    post_data = {
        "state": 0,
        "keyword": "",
        "page": 1
    }
    url = "https://teacher.wozaixiaoyuan.com/signManage/getList.json"
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
def get_sign_result(sign_id, jwsession):
    unsign_list = []
    headers = {
        "jwsession": jwsession
    }
    page = 1
    while True:
        post_data = {
            "id": sign_id,
            "page": page,
            "type": 0,
            "size": 20,
            "targetId": ""
        }
        url = "https://teacher.wozaixiaoyuan.com/signManage/getSignLogs.json"
        s = requests.session()
        r = s.post(url, data=post_data, headers=headers)
        r_json = json.loads(r.text)
        # print(r.text)
        if r_json['code'] == 0:
            if len(r_json['data']) == 0:
                break
            # pprint.pprint(r_json['data'])
            unsign_list.append(r_json['data'])
            # return r_json['data']
        else:
            return 404, r_json
        page += 1
    return 0, unsign_list


def do_sign_class(stu_sign_id, jwsession):
    headers = {
        "jwsession": jwsession
    }
    post_data = {
        "id": stu_sign_id,
        "type": 1
    }
    url = "https://teacher.wozaixiaoyuan.com/signManage/adminSign.json"
    s = requests.session()
    r = s.post(url, data=post_data, headers=headers)
    r_json = json.loads(r.text)
    print(r_json)
    time.sleep(1)
    if r_json['code'] == 0:
        return 0
    else:
        return 404


def leader_sign(not_sign_list, jwsession, flag=1, unsign_num=0):
    # 设立标志位用于区分周末，如果周末就不打卡，只是返回名单
    name_list = []
    random.shuffle(not_sign_list)  # 随机打乱
    sign_num = len(not_sign_list) - unsign_num
    num_flag = 0
    if sign_num >= 0:
        print("开始打卡...")
        for not_sign in not_sign_list:
            if flag == 1 and num_flag < sign_num:
                print(not_sign['name'], num_flag)
                do_sign_class(not_sign['id'], jwsession)
            name_list.append(not_sign['name'])
            num_flag += 1
            time.sleep(0.5)
        return name_list
    else:
        print("设置的未打卡人数超出了现未打卡的人数!")
        for not_sign in not_sign_list:
            name_list.append(not_sign['name'])
        return name_list


# 打卡事件操作
def operate_event(config_info, flag=1):
    # 设立标志位用于区分周末，如果周末就不打卡，只是返回名单
    res, sign_id = contrast_date_class(get_list(config_info['jwsession']))
    if res == 0:
        net_code, not_sign_list = get_sign_result(sign_id, config_info['jwsession'])
        new_unsign_list = []
        if net_code != 404:
            # 将多个页数(列表)合并为一个列表重新转换
            for page_stu in not_sign_list:
                for stu in page_stu:
                    # print(stu['name'])
                    new_unsign_list.append(stu)
            not_sign_name = leader_sign(new_unsign_list, config_info['jwsession'], flag, config_info['unsign_num'])
            if len(not_sign_name) != 0:
                name_str = ""
                for name in not_sign_name:
                    name_str = name_str + name + " "
                print("未打卡名单:", name_str)
            else:
                print("已经全部打了")
            return
        else:
            print("检查名单失败,返回状态码:", not_sign_list)
    # 签到是今天但是签到没有开始，静默等待
    elif res == -2:
        print("签到可能还没开始!")
        return
    elif res == -3:
        print("已过签到时间!")
        # pushplus_post("今日班级打卡情况", "已过签到时间")
        return
    elif res == -1:
        print("签到未发布或者今天没有签到")
        # pushplus_post("今日班级打卡情况", "签到未发布或今天没有签到")
        return


def main():
    choose = '0'
    while True:
        info = get_config()
        print("学生一键签到脚本")
        print("1.晨检")
        print("2.午检")
        print("3.签到")
        print("4.退出")
        choose = input("请输入你的选择:")
        if choose == '1':
            daily_check(time.strftime("%Y%m%d"), info, 1)
        elif choose == '2':
            daily_check(time.strftime("%Y%m%d"), info, 2)
        elif choose == '3':
            operate_event(info, flag=1)
        elif choose == '4':
            return
        else:
            print("请输入正确的参数!")
        choose = '0'


def write_config(config_dict, path=r"./config.json"):
    with open(path, 'w', encoding='utf-8') as file_object:
        file_object.write(json.dumps(config_dict, indent=4, ensure_ascii=False))
    file_object.close()


def get_config(path="./config.json"):
    info_dict = {}
    with open(path, "r", encoding="utf-8") as f:
        info_dict = json.load(f)
    f.close()
    return info_dict


if __name__ == "__main__":
    main()