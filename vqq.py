# coding: utf-8
"""
@author: sy-records
@license: https://github.com/sy-records/v-checkin/blob/master/LICENSE
@contact: 52o@qq52o.cn
@desc: 腾讯视频好莱坞会员V力值签到，支持两次签到：一次正常签到，一次手机签到。
@blog: https://qq52o.me
"""

# python
import sys
import requests
import re

# 推送server酱
sckey = sys.argv[1]
ftqq_url = f"https://sctapi.ftqq.com/{sckey}.send"

# auth_refresh_key
arkey = sys.argv[2]
auth_refresh_url = f"https://access.video.qq.com/user/auth_refresh?{arkey}"

# vcookie
vcookie = sys.argv[3]
# print(vcookie)
# exit

url1 = "https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2"
url2 = "https://v.qq.com/x/bu/mobile_checkin"

login_headers = {
    "Referer": "https://v.qq.com",
    "Cookie": vcookie,
}

login = requests.get(url=auth_refresh_url, headers=login_headers)
cookie = requests.utils.dict_from_cookiejar(login.cookies)

if not cookie:
    print("auth_refresh error")
    payload = {"title": "腾讯视频V力值签到通知", "desp": "获取Cookie失败，Cookie失效"}
    requests.post(ftqq_url, params=payload)
    exit

# print(cookie)


def rmVqs(vcookie):
    return re.sub(r'\s*vqq_vusession=[^;]*;', '', vcookie)


def start():
    sign_headers = {
        "Referer": "https://m.v.qq.com",
        "Cookie": f"{rmVqs(vcookie)}vqq_vusession={cookie['vqq_vusession']};",
    }
    # print('rmc=' + sign_headers['Cookie'])

    sign1 = requests.get(url1, headers=sign_headers).text
    if "Account Verify Error" in sign1:
        print("Sign1 error,Cookie Invalid")
        status = "链接1 失败，Cookie失效"
    else:
        print("Sign1 Success")
        status = "链接1 成功，获得V力值：" + sign1[42:-14]

    sign2 = requests.get(url2, headers=sign_headers).text
    if "Unauthorized" in sign2:
        print("Sign2 error,Cookie Invalid")
        status = status + "\n\n 链接2 失败，Cookie失效"
    else:
        print("Sign2 Success")
        status = status + "\n\n 链接2 成功"

    payload = {"title": "腾讯视频V力值签到通知", "desp": status}
    # print(payload)
    requests.post(ftqq_url, params=payload)


def main_handler(event, context):
    return start()


if __name__ == "__main__":
    start()
