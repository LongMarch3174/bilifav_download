import base64
import json
import requests
from re import findall
from flask import Flask, render_template, jsonify, session
from time import sleep
from io import BytesIO
from PIL import Image
from qrcode import QRCode
from http.cookiejar import LWPCookieJar

app = Flask(__name__)

# 设置 Flask 密钥
app.secret_key = 'your_secret_key'  # 用于加密 session

# 设置 Cookie 存储路径
temp_cookie_file = 'bz-cookie.txt'

headers = {
    'authority': 'api.vc.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://message.bilibili.com',
    'referer': 'https://message.bilibili.com/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81',
}


def is_login(session):
    try:
        session.cookies = LWPCookieJar(filename=temp_cookie_file)
        session.cookies.load(ignore_discard=True)
    except Exception as e:
        print(e)
    login_url = session.get("https://api.bilibili.com/x/web-interface/nav", verify=False, headers=headers).json()
    if login_url['code'] == 0:
        return True, login_url['data']['face'], login_url['data']['uname']
    else:
        return False, None, None


def scan_code(session2):
    global bili_jct
    get_login = session2.get('https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header',
                             headers=headers).json()
    qrcode_key = get_login['data']['qrcode_key']

    # 将 qrcode_key 存储在 Flask session 中
    session['qrcode_key'] = qrcode_key

    qr = QRCode()
    qr.add_data(get_login['data']['url'])
    img = qr.make_image()
    pil_image_change = img.resize((200, 200), resample=Image.BICUBIC)
    img_byte = BytesIO()
    pil_image_change.save(img_byte)
    img_byte.seek(0)
    token_url = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}&source=main-fe-header'
    while 1:
        qrcode_data = session2.get(token_url, headers=headers).json()
        if qrcode_data['data']['code'] == 0:
            session2.get(qrcode_data['data']['url'], headers=headers)
            break
        sleep(1)
    session2.cookies.save()
    with open(temp_cookie_file, 'r', encoding='utf-8') as f:
        bzcookie = f.read()
    bili_jct = findall(r'bili_jct=(.*?);', bzcookie)[0]


@app.route('/')
def index():
    session2 = requests.Session()
    # 检查是否已经登录
    is_logged_in, user_face, user_name = is_login(session2)

    if is_logged_in:
        # 如果已经登录，显示头像并更新说明
        img_data = requests.get(user_face).content
        img_base64 = base64.b64encode(img_data).decode('utf-8')  # 转换为 Base64 编码字符串

        return render_template('index.html', logged_in=True, img_data=img_base64, user_name=user_name)
    else:
        # 如果未登录，生成二维码
        get_login = session2.get('https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header',
                                 headers=headers).json()
        qrcode_key = get_login['data']['qrcode_key']
        session['qrcode_key'] = qrcode_key

        qr = QRCode()
        qr.add_data(get_login['data']['url'])
        img = qr.make_image()
        pil_image_change = img.resize((200, 200), resample=Image.BICUBIC)
        img_byte = BytesIO()
        pil_image_change.save(img_byte, format='PNG')
        img_byte.seek(0)
        # 将二维码图像数据转换为 Base64 编码
        img_base64 = base64.b64encode(img_byte.getvalue()).decode('utf-8')

        return render_template('index.html', logged_in=False, img_data=img_base64)


@app.route('/scan_status')
def scan_status():
    # 从 session 中获取 qrcode_key
    qrcode_key = session.get('qrcode_key')

    if not qrcode_key:
        return jsonify({'status': 'failed', 'message': '二维码 key 丢失'})

    session2 = requests.Session()
    token_url = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}&source=main-fe-header'

    # 创建一个 LWPCookieJar 实例用于保存 cookies
    cookie_jar = LWPCookieJar(temp_cookie_file)
    session2.cookies = cookie_jar

    # 轮询直到扫码成功
    while 1:
        qrcode_data = session2.get(token_url, headers=headers).json()
        if qrcode_data['data']['code'] == 0:
            # 执行登录成功后的操作
            session2.get(qrcode_data['data']['url'], headers=headers)

            # 获取登录后的 cookie 数据
            session2.cookies.save()  # 保存 cookies 到文件

            # 可以在这里提取并保存需要的 cookie 数据
            with open(temp_cookie_file, 'r', encoding='utf-8') as f:
                bzcookie = f.read()

            # 提取并保存需要的 cookie 值
            bili_jct = findall(r'bili_jct=(.*?);', bzcookie)[0]
            SESSDATA = findall(r'SESSDATA="(.*?);', bzcookie)[0]
            DedeUserID = findall(r'DedeUserID=(.*?);', bzcookie)[0]

            cookies_data = {
                "cookies": f'SESSDATA="{SESSDATA}; DedeUserID={DedeUserID}; bili_jct={bili_jct}',
                "save_path": "./bili_videos",
                "ffmpeg_path": "ffmpeg",
                "request_interval": 1.5,
                "max_retries": 3
            }

            # Save the cookies data into a JSON file
            with open('config.json', 'w', encoding='utf-8') as json_file:
                json.dump(cookies_data, json_file, ensure_ascii=False, indent=4)

            return jsonify({'status': 'success', 'message': '登录成功'})
        sleep(1)

    return jsonify({'status': 'failed', 'message': '扫码失败'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=61234)
