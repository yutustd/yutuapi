from flask import Flask, request, jsonify
import ql

app = Flask(__name__)


@app.route("/")
def hello_world():
    return jsonify({"message": "Welcome to use yutuapi!"})


@app.route("/upload_cookie", methods=["POST"])
def upload_cookie():
    assert request.path == "/upload_cookie"
    assert request.method == "POST"
    flag_ck_exist = False
    results = False
    _id = ""
    pt_key = request.json["pt_key"]
    pt_pin = request.json["pt_pin"]
    if pt_key == "" or pt_pin == "":
        return jsonify({"message": "Cookie有误！"})
    cookie = f"pt_key={pt_key};pt_pin={pt_pin};"
    remark = request.json["remark"]
    cookies = ql.get_cookies()

    for ck in cookies:
        ck_pt_pin = ck["value"].split(";")[1].split("=")[1]
        if ck_pt_pin == pt_pin:
            flag_ck_exist = True
            _id = ck['_id']
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


if __name__ == '__main__':
    app.run(debug=True)
