import json
import time
import requests
import hashlib
from urllib import parse


def md5(_str):
    hl = hashlib.md5()
    hl.update(_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def send_sms(phone):
    appid = 959
    version = "1.0.0"
    country_code = 86
    time_stamp = int(round(time.time() * 1000))
    sub_cmd = 1
    gsalt = "sb2cwlYyaCSN1KUv5RHG3tmqxfEb8NKN"
    gsign = md5(f"{appid}{version}{time_stamp}36{sub_cmd}{gsalt}")
    url = "https://qapplogin.m.jd.com/cgi-bin/qapp/quick"
    header = {
        'user-agent':
            'Mozilla/5.0 (Linux; Android 10; V1838T Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.87 Mobile Safari/537.36 hap/1.9/vivo com.vivo.hybrid/1.9.6.302 com.jd.crplandroidhap/1.0.3 ({packageName:com.vivo.hybrid,type:deeplink,extra:{}})',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'accept-encoding': '',
        'cookie': '',
    }
    body = {
        'client_ver': version,
        'gsign': gsign,
        'appid': appid,
        'return_page': 'https%3A%2F%2Fcrpl.jd.com%2Fn%2Fmine%3FpartnerId%3DWBTF0KYY%26ADTAG%3Dkyy_mrqd%26token%3D',
        'cmd': 36,
        'sdk_ver': '1.0.0',
        'sub_cmd': sub_cmd,
        'qversion': version,
        'ts': time_stamp
    }
    results = requests.post(url, data=body, headers=header)
    data = json.loads(results.text)['data']

    sub_cmd = 2
    time_stamp = time.time() * 1000
    gsalt = data['gsalt']
    gsign = md5(f"{appid}{version}{time_stamp}36{sub_cmd}{gsalt}")
    sign = md5(f"{appid}{version}{country_code}{phone}4dtyyzKF3w6o54fJZnmeW3bVHl0$PbXj")
    ck = f"guid={data['guid']};lsid={data['lsid']};gsalt={data['gsalt']};rsa_modulus={data['rsa_modulus']};"
    header = {
        'user-agent':
            'Mozilla/5.0 (Linux; Android 10; V1838T Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.87 Mobile Safari/537.36 hap/1.9/vivo com.vivo.hybrid/1.9.6.302 com.jd.crplandroidhap/1.0.3 ({packageName:com.vivo.hybrid,type:deeplink,extra:{}})',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'accept-encoding': '',
        'cookie': ck,
    }
    body = {
        'country_code': country_code,
        'client_ver': version,
        'gsign': gsign,
        'appid': appid,
        'mobile': phone,
        'sign': sign,
        'cmd': 36,
        'sub_cmd': sub_cmd,
        'qversion': version,
        'ts': time_stamp
    }

    results = requests.post(url, data=body, headers=header)
    data = json.loads(results.text)
    if data['err_code'] > 0:
        return {'ok': False, 'message': '发送验证码失败：' + data['err_msg']}
    else:
        return {'ok': True, 'message': 'Success', 'data': {'ck': ck, 'gsalt': gsalt}}


def check_code(phone, code, gsalt, ck):
    appid = 959
    version = '1.0.0'
    country_code = 86
    time_stamp = int(round(time.time() * 1000))
    sub_cmd = 3
    gsign = md5(f"{appid}{version}{time_stamp}36{sub_cmd}{gsalt}")
    url = "https://qapplogin.m.jd.com/cgi-bin/qapp/quick"

    header = {
        'user-agent':
            'Mozilla/5.0 (Linux; Android 10; V1838T Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.87 Mobile Safari/537.36 hap/1.9/vivo com.vivo.hybrid/1.9.6.302 com.jd.crplandroidhap/1.0.3 ({packageName:com.vivo.hybrid,type:deeplink,extra:{}})',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'accept-encoding': '',
        'cookie': ck,
    }
    body = {
        'country_code': country_code,
        'client_ver': version,
        'gsign': gsign,
        'smscode': code,
        'appid': appid,
        'mobile': phone,
        'cmd': 36,
        'sub_cmd': sub_cmd,
        'qversion': version,
        'ts': time_stamp
    }
    results = requests.post(url, data=body, headers=header)
    results = json.loads(results.text)
    return results
