import os
import re
import json
import time
import requests
import yaml

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

ql_url = config["QL_URL"]
ql_client_id = config["QL_CLIENT_ID"]
ql_client_secret = config["QL_CLIENT_SECRET"]
wecom_am = config["QYWX_AM"]


def get_token():
    url = f"{ql_url}/open/auth/token"
    params = {
        "client_id": ql_client_id,
        "client_secret": ql_client_secret
    }
    results = requests.get(url, params=params)
    results = json.loads(results.text)
    return results["data"]["token"]


def get_cookies():
    token = get_token()
    url = f"{ql_url}/open/envs"
    params = {
        "searchValue": "JD_COOKIE",
        "t": int(round(time.time() * 1000))
    }
    header = {
        "Accept": "application/json",
        "authorization": f"Bearer {token}"
    }
    results = requests.get(url, params=params, headers=header)
    return json.loads(results.text)["data"]


def get_cookies_count():
    data = get_cookies()
    return len(data)


def add_cookie(ck, remark):
    token = get_token()
    url = f"{ql_url}/open/envs"
    params = {
        "t": int(round(time.time() * 1000))
    }
    data = [{
        "name": "JD_COOKIE",
        "value": ck,
        "remarks": remark
    }]
    header = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json;charset=UTF-8"
    }
    results = requests.post(url, params=params, json=data, headers=header)
    print(results.text)
    if results.status_code == 200:
        return True
    else:
        return False


def update_cookie(ck, eid, remark):
    token = get_token()
    url = f"{ql_url}/open/envs"
    params = {
        "t": int(round(time.time() * 1000))
    }
    data = {
        "name": "JD_COOKIE",
        "value": ck,
        "id": eid,
        "remarks": remark
    }
    header = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json;charset=UTF-8"
    }
    results = requests.put(url, params=params, json=data, headers=header)
    if results.status_code == 200:
        return True
    else:
        return False


def del_cookie(eid):
    token = get_token()
    url = f"{ql_url}/open/envs"
    params = {
        "t": int(round(time.time() * 1000))
    }
    header = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json;charset=UTF-8"
    }
    data = json.dumps([eid])
    results = requests.delete(url, params=params, data=data, headers=header)
    print(results.text)
    if results.status_code == 200:
        return True
    else:
        return False


def send(title: str, content: str) -> None:
    """
    通过 企业微信 APP 推送消息。
    """
    if not wecom_am:
        print("QYWX_AM 未设置!!\n取消推送")
        return
    wecom_am_arr = re.split(",", wecom_am)
    if 4 < len(wecom_am_arr) > 5:
        print("QYWX_AM 设置错误!!\n取消推送")
        return
    print("企业微信 APP 服务启动")

    corp_id = wecom_am_arr[0]
    corp_secret = wecom_am_arr[1]
    touser = wecom_am_arr[2]
    agent_id = wecom_am_arr[3]
    try:
        media_id = wecom_am_arr[4]
    except IndexError:
        media_id = ""
    wx = WeCom(corp_id, corp_secret, agent_id)
    # 如果没有配置 media_id 默认就以 text 方式发送
    if not media_id:
        message = title + "\n\n" + content
        response = wx.send_text(message, touser)
    else:
        response = wx.send_mpnews(title, content, media_id, touser)

    if response == "ok":
        print("企业微信推送成功！")
    else:
        print("企业微信推送失败！错误信息如下：\n", response)


class WeCom:
    def __init__(self, corp_id, corp_secret, agent_id):
        self.CORPID = corp_id
        self.CORPSECRET = corp_secret
        self.AGENTID = agent_id

    def get_access_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        values = {
            "corpid": self.CORPID,
            "corpsecret": self.CORPSECRET,
        }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_text(self, message, touser="@all"):
        send_url = (
                "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
                + self.get_access_token()
        )
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {"content": message},
            "safe": "0",
        }
        send_msges = bytes(json.dumps(send_values), "utf-8")
        response = requests.post(send_url, send_msges)
        response = response.json()
        return response["errmsg"]

    def send_mpnews(self, title, message, media_id, touser="@all"):
        send_url = (
                "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
                + self.get_access_token()
        )
        send_values = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.AGENTID,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": media_id,
                        "author": "Author",
                        "content_source_url": "",
                        "content": message.replace("\n", "<br/>"),
                        "digest": message,
                    }
                ]
            },
        }
        send_msges = bytes(json.dumps(send_values), "utf-8")
        response = requests.post(send_url, send_msges)
        response = response.json()
        return response["errmsg"]
