import requests
import re
import base64
import json
# 导入第三方库:pip install pycryptodome
from Crypto.Cipher import AES

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def handleHtml(url):
    # requests得到html文件内容
    content = requests.get(url, headers=header).text
    content = str(content).replace('\n', ' ')

    # 获取nextUrl
    nextUrl = re.findall("var nextUrl = '(.*?)';", content)[0]
    # 获取lesInfo
    lesInfo = re.findall("var lesInfo = ({.*?});", content)[0]
    lesInfo = json.loads(lesInfo)
    # 获取key
    key = re.findall("var lesInfo = .*?\".*?_key\":\"([^\"]*)\"", content)[0]
    # 获取m3u8url FIXME
    id = lesInfo['id']
    m3u8url = f'https://*****&id={id}&******'
    # 下载m3u8文件
    if m3u8WithKey(m3u8url, key, lesInfo['title']):
        # 成功的话，继续处理nextUrl
        if len(nextUrl) > 0:
            handleHtml(nextUrl)


def m3u8WithKey(url, key, fileName):
    # requests得到m3u8文件内容
    content = requests.get(url, headers=header).text
    if "#EXTM3U" not in content:
        print("这不是一个m3u8的视频链接！")
        return False
    if "EXT-X-KEY" not in content:
        print("没有加密")
        return False

    # base64 key
    key = base64.b64encode(key.encode()).decode()
    # 同时更改m3u8里面的key（就是上面var lesInfo的*****_key）
    # URI="https://****"变成URI="base64:NTFmOGQ0MmM5NDMyMWIzZQ=="


    # 得到每一个ts视频链接
    tslist = re.findall('EXTINF:(.*),\n(.*)\n#', content)
    newlist = []
    for i in tslist:
        newlist.append(i[1])

    # 先获取URL/后的后缀，再替换为空
    urlkey = url.split('/')[-1]
    url2 = url.replace(urlkey, '')  # 这里为得到url地址的前面部分，为后面key的链接和视频链接拼接使用

    # 得到key的链接并请求得到加密的key值
    keyurl = url2+key[0]
    keycontent = requests.get(keyurl, headers=header).text

    # 得到每一个完整视频的链接地址
    tslisturl = []
    for i in newlist:
        tsurl = url2+i
        tslisturl.append(tsurl)

    # 得到解密方法，这里要导入第三方库  pycrypto
    cryptor = AES.new(keycontent, AES.MODE_CBC, keycontent)

    # for循环获取视频文件
    for i in tslisturl:
        res = requests.get(i, header)
        # 使用解密方法解密得到的视频文件
        cont = cryptor.decrypt(res.content)
        # 以追加的形式保存为mp4文件
        with open(fileName + '.mp4', 'ab+') as f:
            f.write(cont)
    return True


if __name__ == '__main__':
    # 处理第一个网页  FIXME
    handleHtml("https://**/**/***")


