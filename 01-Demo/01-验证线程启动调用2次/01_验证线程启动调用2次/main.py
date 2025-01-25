import threading
import time
from flask import Flask
app = Flask(__name__)
lock = threading.Lock()
def update_data():
    print('开始:  update_data')
    time.sleep(60)
    print('结束: update_data')
@app.get('/hello')
def call_update_data():
    with lock:
        print('开始：接口调用')
        update_data()
        time.sleep(60)
        print('结束：接口调用')
    return 'Hello World'
def run_api():
    # app.run(debug=True, port=5000, use_reloader=False)
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
def auto_update():
    while True:
        with lock:
            print('开始：定时调用')
            update_data()
            print('结束：定时调用')
        time.sleep(1*60)
threading.Thread(target=auto_update).start()
if __name__=='__main__' :
    run_api()

