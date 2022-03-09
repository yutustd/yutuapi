import re
from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import *
import ql
import jd

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def hello_world():
    return render_template('index.html')
    # return jsonify({"message": "Welcome to use yutuapi!"})


@app.route("/upload_cookie", methods=["POST"])
def upload_cookie():
    assert request.path == "/upload_cookie"
    assert request.method == "POST"
    flag_ck_exist = False
    results = False
    _id = ""
    pt_key = request.json["pt_key"]
    pt_pin = request.json["pt_pin"]
    remark = request.json["remark"]
    if pt_key == "" or pt_pin == "":
        return jsonify({"message": "Cookie有误！"})
    if remark == "":
        return jsonify({"message": "请添加备注信息！"})
    cookie = f"pt_key={pt_key};pt_pin={pt_pin};"
    cookies = ql.get_cookies()

    for ck in cookies:
        ck_pt_pin = ck["value"].split(";")[1].split("=")[1]
        if ck_pt_pin == pt_pin:
            flag_ck_exist = True
            _id = ck['id']
    if flag_ck_exist:
        results = ql.update_cookie(cookie, _id, remark)
    else:
        results = ql.add_cookie(cookie, remark)
    if results:
        ql.send("Yutu 通知", f"{remark}上传啦！")
        return jsonify({"message": f"欢迎回来，{remark}"})
    else:
        return jsonify({"message": "上传失败啦！"})


@app.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    assert request.path == "/delete_cookie"
    assert request.method == "POST"
    flag_ck_exist = False
    results = False
    _id = ""
    _remark = ""
    pt_key = request.json["pt_key"]
    pt_pin = request.json["pt_pin"]
    cookie = f"pt_key={pt_key};pt_pin={pt_pin};"
    cookies = ql.get_cookies()
    for ck in cookies:
        if ck["value"] == cookie:
            flag_ck_exist = True
            _id = ck['_id']
            _remark = ck["name"]
    if flag_ck_exist:
        results = ql.del_cookie(_id)
        if results:
            ql.send("Yutu 通知", f"{_remark}跑路啦！")
            return jsonify({"message": f"再见喽，{_remark}"})
        else:
            return jsonify({"message": "删除失败啦，请稍后再试！"})
    else:
        return jsonify({"message": "都没你的 ck， 删什么删！"})


@app.route("/send_sms", methods=["GET"])
def send_sms():
    assert request.path == "/send_sms"
    assert request.method == "GET"
    phone = request.args.get("phone")
    if not re.match('\\d{11}', phone):
        return jsonify({'ok': False, 'message': '手机号格式错误'})
    else:
        try:
            data = jd.send_sms(phone=phone)
            print(data)
            return jsonify(data)
        except Exception as e:
            print(e)
            return jsonify({'ok': False, 'message': '错误'})


@app.route("/check_code", methods=["POST"])
def check_code():
    assert request.path == "/check_code"
    assert request.method == "POST"
    phone = request.args.get("phone")
    if not re.match('\\d{11}', phone):
        return jsonify({'ok': False, 'message': '手机号格式错误'})
    code = request.args.get("code")
    if not re.match('\\d{6}', code):
        return jsonify({'ok': False, 'message': '验证码格式错误'})
    gsalt = request.json['gsalt']
    ck = request.json['ck']
    print(gsalt, ck)
    data = jd.check_code(phone, code, gsalt, ck)
    if data['err_code'] > 0:
        return jsonify({'ok': False, 'message': data['err_msg']})
    else:
        pt_key = data['data']['pt_key']
        pt_pin = data['data']['pt_pin']
        cookie = f'pt_key={pt_key};pt_pin={pt_pin};'
        return jsonify({'ok': True, 'message': '获取 CK 成功', 'data': {'ck': cookie}})


if __name__ == '__main__':
    app.run(debug=True)
