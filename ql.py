import os
import json
import time
import requests
import yaml

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

ql_url = config["QL_URL"]
ql_client_id = config["QL_CLIENT_ID"]
ql_client_secret = config["QL_CLIENT_SECRET"]


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
        "_id": eid,
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
