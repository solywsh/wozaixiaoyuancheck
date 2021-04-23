import requests

def NoonInspection():
    headers = {
        'content-length' : '134',
        'cookie' : 'SESSION=NGY4ZGYwNGMtZTQ3ZC00ZDRmLTg2MmEtNDRhMDYyOTZlYTAw;path=/;HttpOnly',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type' : 'application/x-www-form-urlencoded',
        'token' : 'a8865ccf-5ba4-40e8-8c33-4902e82ac7ef',
        'refer' : 'https://servicewechat.com/wxce6d08f781975d91/143/page-frame.html',
        'accept-encoding' : 'gzip, deflate, br'
    }
    postdata = {
        'answers' : '["0","36.5"]',
        'seq' : '2',
        'temperature' : '36.6',
        'userid' : '',
        'latitude' : '',
        'longitude' : '108.605084',
        'country' : '中国',
        'city' : '西安市',
        'district' : '鄠邑区',
        'province' : '陕西省',
        'township' : '',
        'street' : '东街',
        'myArea' : '',
        'areacode' : '610118'
    }
    url = 'https://student.wozaixiaoyuan.com/heat/save.json'
    s = requests.session()
    r = s.post(url, data=postdata, headers=headers)

if __name__ == "__main__":
    NoonInspection()