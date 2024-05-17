from flask import Flask, jsonify
import random
import threading
import time
from datetime import datetime

app = Flask(__name__)

send_high_pressure = False

def send_pressure_data():
    global send_high_pressure
    while True:
        pressure_data = []
        for sensor_id in range(1, 10):
            if send_high_pressure:
                pressure = 200  
            else:
                pressure = random.uniform(90, 110)
                pressure = int(pressure)

            data_package = {
                'sensor_id': f'{sensor_id:02}',
                'pressure': pressure,
                'timestamp': datetime.now().isoformat()
            }

            pressure_data.append(data_package)

        print(pressure_data)  

        if send_high_pressure:
            send_high_pressure = False  

        time.sleep(10 * 60)  

def toggle_high_pressure():
    global send_high_pressure
    while True:
        time.sleep(2 * 24 * 60 * 60)  
        send_high_pressure = True  

@app.route('/send-pressure')
def send_pressure():
    pressure_data = []
    for sensor_id in range(1, 10):
        pressure = random.uniform(90, 110)
        pressure = int(pressure)

        data_package = {
            'sensor_id': f'{sensor_id:02}',
            'pressure': pressure,
            'timestamp': datetime.now().isoformat()
        }

        pressure_data.append(data_package)

    return jsonify(pressure_data)

if __name__ == '__main__':
    pressure_thread = threading.Thread(target=send_pressure_data)
    pressure_thread.daemon = True
    pressure_thread.start()

    high_pressure_thread = threading.Thread(target=toggle_high_pressure)
    high_pressure_thread.daemon = True
    high_pressure_thread.start()

    app.run(debug=True)
