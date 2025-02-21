from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/run-bash', methods=['GET'])
def run_bash():
    # 这里的bash脚本路径可以根据实际情况修改
    bash_file = "/volume1/LM/bilifav_download/start_bilifavdown.sh"
    try:
        # 使用subprocess执行bash脚本
        result = subprocess.run(["bash", bash_file], capture_output=True, text=True)
        # 返回bash脚本的输出结果
        return result.stdout
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # 设置服务器监听的端口
    app.run(host='0.0.0.0', port=63172)
