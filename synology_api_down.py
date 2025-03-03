import os
import requests


os.environ["http_proxy"] = "http://localhost:18888"
os.environ["https_proxy"] = "http://localhost:18888"

# 设置URL和参数
url = "http://192.168.0.102:63174/webapi/entry.cgi"
login_params = {
    "api": "SYNO.API.Auth",
    "version": "6",
    "method": "login",
    "account": "LongMarch",
    "passwd": "@Xufeiran1",
    "session": "FileStation",
    "format": "cookie"
}

# 发送 GET 请求
session = requests.Session()  # 使用 Session 来管理 Cookies
login_response = session.get(url, params=login_params)

# 打印响应信息
# print("Status Code:", login_response.status_code)
# print("Response:", login_response.text)

# 检查是否登录成功
if login_response.status_code == 200 and "success" in login_response.text:
    print("登录成功")
else:
    print("登录失败")

login_data = login_response.json()
session_id = login_data['data']['sid']
print("Session ID:", session_id)

task_payload = {
    "stop_when_error": "false",
    "mode": "\"sequential\"",
    "compound": '[{"api":"SYNO.Core.TaskScheduler","method":"run","version":2,"tasks":[{"id":6,"real_owner":"root"}]}]',
    "api": "SYNO.Entry.Request",
    "method": "request",
    "version": "1"
}
task_headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": f"_SSID=5MbosQFVbfmV0pu13vUgu1lo25mUKJ3PxLIs9Qc9Gl0; stay_login=1; did=e7UxeKiLn6Ql6HXQgF_NIZhK00UdT3cDM-0sv_fCW3dI4NZhEFTrpdJ--M87bTfTJDGyXHAYJ7QtS3QqLLmjDw; _CrPoSt=cHJvdG9jb2w9aHR0cDo7IHBvcnQ9NjMxNzQ7IHBhdGhuYW1lPS87; remember_token=eyJyYW5kb20iOiIzZTdkNmFiZjYwNGU0NGVjMjM2ZCIsInVzZXIiOiIxIn0.5ufUU1zOHrpVsJEBnJPyeL7tFvQ; token=WyGKfTwbF2FXsAoQwjc4/wFveLuV/KyZRUOV4ifLFzk=; ViewType=timeline; ViewLibrary=shared_space; id={session_id}; io=Ei_o285Xet-FSMUbAAAH"
}

task_response = session.post(url, headers=task_headers, data=task_payload)
# print("Status Code:", task_response.status_code)
print("Response:", task_response.text)
if task_response.status_code == 200 and "success" in task_response.text:
    print("任务开始")
else:
    print("任务失败")

# 注销
logout_params = {
    "api": "SYNO.API.Auth",
    "version": "6",
    "method": "logout",
}

logout_response = session.get(url, params=logout_params)
# print("Status Code:", logout_response.status_code)
# print("Response:", logout_response.text)
if logout_response.status_code == 200 and "success" in logout_response.text:
    print("注销成功")
else:
    print("注销失败")


