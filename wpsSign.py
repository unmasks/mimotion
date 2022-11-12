# !/usr/bin/env python
# coding=utf-8
import requests
import json
import pytz
import datetime
from io import StringIO
import time
import os

# 初始化信息
# '*********复制SERVER酱的SCKEY进来*************(保留引号)'
SCKEY = os.environ.get('SCKEY')
data = {
    "wps_invite": [
        {
            "name": "unmask",
            # "*********复制手机WPS个人信息中的用户ID进来，类似括号内容(191641526)*************(不保留双引号)",
            "uid": os.environ.get('UID'),
            # network获取wps_sid
            "sid": os.environ.get('SID')
        }
    ]
}
# 初始化日志

sio = StringIO('WPS签到日志\n\n')
sio.seek(0, 2)  # 将读写位置移动到结尾
s = requests.session()
tz = pytz.timezone('Asia/Shanghai')
nowtime = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
sio.write("-" + nowtime + "-\n\n")


# APP
def pushWechat(desp, nowtime):
    ssckey = SCKEY
    send_url = 'https://sctapi.ftqq.com/' + ssckey + '.send'
    if '失败' in desp:
        params = {
            'title': 'WPS小程序邀请失败提醒' + nowtime,
            'desp': desp
        }
    else:
        params = {
            'title': 'WPS小程序邀请成功' + nowtime,
            'desp': desp
        }
    requests.post(send_url, params=params)


# 主函数
def main():
    wps_inv = data['wps_invite']
    # 这13个账号被邀请
    invite_sids = [
        "V02StVuaNcoKrZ3BuvJQ1FcFS_xnG2k00af250d4002664c02f",
        "V02SWIvKWYijG6Rggo4m0xvDKj1m7ew00a8e26d3002508b828",
        "V02Sr3nJ9IicoHWfeyQLiXgvrRpje6E00a240b890023270f97",
        "V02SBsNOf4sJZNFo4jOHdgHg7-2Tn1s00a338776000b669579",
        "V02ScVbtm2pQD49ArcgGLv360iqQFLs014c8062e000b6c37b6",
        "V02S2oI49T-Jp0_zJKZ5U38dIUSIl8Q00aa679530026780e96",
        "V02ShotJqqiWyubCX0VWTlcbgcHqtSQ00a45564e002678124c",
        "V02SFiqdXRGnH5oAV2FmDDulZyGDL3M00a61660c0026781be1",
        "V02S7tldy5ltYcikCzJ8PJQDSy_ElEs00a327c3c0026782526",
        "V02SPoOluAnWda0dTBYTXpdetS97tyI00a16135e002684bb5c",
        "V02Sb8gxW2inr6IDYrdHK_ywJnayd6s00ab7472b0026849b17",
        "V02SwV15KQ_8n6brU98_2kLnnFUDUOw00adf3fda0026934a7f",
        "V02SC1mOHS0RiUBxeoA8NTliH2h2NGc00a803c35002693584d"

    ]
    sio.write("\n\n==========wps邀请==========\n\n")
    for item in wps_inv:
        sio.write("为{}邀请---↓\n\n".format(item['name']))
        if type(item['uid']) == int:
            wps_invite(invite_sids, item['uid'])
        else:
            sio.write(
                "邀请失败：用户ID错误，请重新复制手机WPS个人信息中的用户ID并修改'uid'项,注意不保留双引号\n\n")
    desp = sio.getvalue()
    pushWechat(desp, nowtime)
    print(desp)
    return desp


# wps接受邀请
def wps_invite(sids: list, uid: int) -> None:
    invite_url = 'http://zt.wps.cn/2018/clock_in/api/invite'
    for i, sid in enumerate(sids):
        headers = {
            'sid': sid
        }
        time.sleep(10)
        r = s.post(invite_url, headers=headers, data={'invite_userid': uid})
        # sio.write("ID={}, 状态码: {}, \n\n ".format(str(index + 1).zfill(2), r.status_code))


# wps签到
def wps_clockin(sid: str):
    if len(sid) == 0:
        sio.write("签到失败：用户sid为空，请重新输入\n\n")
        return 0
    elif "*" in sid or sid[0] != "V":
        sio.write("签到失败：用户sid错误，请重新输入\n\n")
        return 0
    # 打卡签到
    clockin_url = 'http://zt.wps.cn/2018/clock_in/api/clock_in?member=wps'
    r = s.get(clockin_url, headers={'sid': sid})
    if len(r.history) != 0:
        if r.history[0].status_code == 302:
            sio.write("签到失败：用户sid错误，请重新输入\n\n")
            return 0
    rsp = json.loads(r.text)
    # 判断是否已打卡
    if rsp['msg'] == '已打卡':
        sio.write("签到信息: {}\n\n".format(r.text))
        return 1
    # 判断是否绑定手机
    elif rsp['msg'] == '未绑定手机':
        sio.write('签到失败: 未绑定手机，请绑定手机后重新运行签到\n\n')
        return 0
    # 判断是否重新报名
    elif rsp['msg'] == '前一天未报名':
        sio.write('前一天未报名\n\n')
        signup_url = 'http://zt.wps.cn/2018/clock_in/api/sign_up'
        r = s.get(signup_url, headers={'sid': sid})
        rsp = json.loads(r.text)
        if rsp['result'] == 'ok':
            sio.write('报名信息: 已自动报名，报名后第二天签到\n\n')
            return 1
        else:
            sio.write('报名失败: 请手动报名，报名后第二天签到\n\n')
            return 0
    # 打卡签到需要参加活动
    elif rsp['msg'] == '答题未通过':
        getquestion_url = 'http://zt.wps.cn/2018/clock_in/api/get_question?member=wps'
        r = s.get(getquestion_url, headers={'sid': sid})
        '''
        {
            "result": "ok",
            "data": {
                "multi_select": 1,
                "options": [
                    "30天文档分享链接有效期",
                    "远程下载助手",
                    "输出长图片去水印",
                    "PDF转图片"
                ],
                "title": "以下哪些特权是WPS会员和超级会员共同拥有的？"
            },
            "msg": ""
        }
        '''
        answer_set = {
            'WPS会员全文检索',
            '100G',
            'WPS会员数据恢复',
            'WPS会员PDF转doc',
            'WPS会员PDF转图片',
            'WPS图片转PDF插件',
            '金山PDF转WORD',
            'WPS会员拍照转文字',
            '使用WPS会员修复',
            'WPS全文检索功能',
            '有，且无限次',
            '文档修复'
        }
        rsp = json.loads(r.text)
        # sio.write(resp['data']['multi_select'])
        # 只做单选题 multi_select==1表示多选题
        while rsp['data']['multi_select'] == 1:
            r = s.get(getquestion_url, headers={'sid': sid})
            rsp = json.loads(r.text)
            # sio.write('选择题类型: {}'.format(resp['data']['multi_select']))
        answer_id = 3
        for i in range(4):
            opt = rsp['data']['options'][i]
            if opt in answer_set:
                answer_id = i+1
                break
        sio.write("选项: {}\n\n".format(rsp['data']['options']))
        sio.write("选择答案: {}\n\n".format(answer_id))
        # 提交答案
        answer_url = 'http://zt.wps.cn/2018/clock_in/api/answer?member=wps'
        r = s.post(answer_url, headers={
                   'sid': sid}, data={'answer': answer_id})
        rsp = json.loads(r.text)
        # 答案错误
        if rsp['msg'] == 'wrong answer':
            sio.write("答案不对，挨个尝试\n\n")
            for i in range(4):
                r = s.post(answer_url, headers={
                           'sid': sid}, data={'answer': i+1})
                rsp = json.loads(r.text)
                sio.write(i+1)
                if rsp['result'] == 'ok':
                    sio.write(r.text)
                    break
        # 打卡签到
        clockin_url = 'http://zt.wps.cn/2018/clock_in/api/clock_in?member=wps'
        r = s.get(clockin_url, headers={'sid': sid})
        sio.write("签到信息: {}\n\n".format(r.text))
        return 1
    # 判断是否不在签到时间内
    elif rsp['msg'] == '不在打卡时间内':
        sio.write('签到失败: 不在打卡时间内\n\n')
        signup_url = 'http://zt.wps.cn/2018/clock_in/api/sign_up'
        r = s.get(signup_url, headers={'sid': sid})
        rsp = json.loads(r.text)
        if rsp['result'] == 'ok':
            sio.write('已自动报名，报名后请设置在规定时间内签到\n\n')
            return 1
        else:
            sio.write('报名失败: 请手动报名，报名后第二天签到\n\n')
            return 0
    # 其他错误
    elif rsp['result'] == 'error':
        sio.write('签到失败信息: {}\n\n'.format(r.text))
        signup_url = 'http://zt.wps.cn/2018/clock_in/api/sign_up'
        r = s.get(signup_url, headers={'sid': sid})
        rsp = json.loads(r.text)
        if rsp['result'] == 'ok':
            sio.write('已自动报名，报名后请设置在规定时间内签到\n\n')
            return 1
        else:
            sio.write('报名失败: 请手动报名，报名后第二天签到\n\n')
            return 0


def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()
