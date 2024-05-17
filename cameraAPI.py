from flask import Flask, jsonify
import random
import threading
import time
from datetime import datetime

app = Flask(__name__)

send_many_trues = False

def simulate_camera_data():
    global send_many_trues
    while True:
        camera_data = []
        for camera_id in range(1, 11):
            if send_many_trues:
                presence_detected = True 
            else:
                presence_detected = random.choice([True, False])

            data_package = {
                'camera_id': f'{camera_id:02}',
                'presence_detected': presence_detected,
                'timestamp': datetime.now().isoformat()
            }

            camera_data.append(data_package)

        print(camera_data)  

        if send_many_trues:
            send_many_trues = False  

        time.sleep(10 * 60) 

def toggle_many_trues():
    global send_many_trues
    while True:
        time.sleep(2 * 24 * 60 * 60) 
        send_many_trues = True  

@app.route('/camera-presence')
def camera_presence():
    camera_data = []
    for camera_id in range(1, 11):
        presence_detected = random.choice([True, False])

        data_package = {
            'camera_id': f'{camera_id:02}',
            'presence_detected': presence_detected,
            'timestamp': datetime.now().isoformat()
        }

        camera_data.append(data_package)

    return jsonify(camera_data)

if __name__ == '__main__':
    camera_thread = threading.Thread(target=simulate_camera_data)
    camera_thread.daemon = True
    camera_thread.start()

    high_presence_thread = threading.Thread(target=toggle_many_trues)
    high_presence_thread.daemon = True
    high_presence_thread.start()

    app.run(debug=True)
