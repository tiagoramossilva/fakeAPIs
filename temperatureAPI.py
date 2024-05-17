from flask import Flask, jsonify
import random
import threading
import time
from datetime import datetime

app = Flask(__name__)

send_high_temp = False

def send_temperature_data():
    global send_high_temp
    while True:
        temperature_data = []
        for sensor_id in range(1, 10):
            if send_high_temp:
                temperature = 100  
            else:
                temperature = random.uniform(15, 25)
                temperature = int(temperature)

            data_package = {
                'sensor_id': f'{sensor_id:02}',
                'temperature': temperature,
                'timestamp': datetime.now().isoformat()
            }

            temperature_data.append(data_package)

        print(temperature_data)  

        if send_high_temp:
            send_high_temp = False  
        time.sleep(10 * 60)  

def toggle_high_temperature():
    global send_high_temp
    while True:
        time.sleep(2 * 24 * 60 * 60)  
        send_high_temp = True  

@app.route('/send-temperature')
def send_temperature():
    temperature_data = []
    for sensor_id in range(1, 10):
        temperature = random.uniform(15, 25)
        temperature = int(temperature)

        data_package = {
            'sensor_id': f'{sensor_id:02}',
            'temperature': temperature,
            'timestamp': datetime.now().isoformat()
        }

        temperature_data.append(data_package)

    return jsonify(temperature_data)

if __name__ == '__main__':
    temperature_thread = threading.Thread(target=send_temperature_data)
    temperature_thread.daemon = True
    temperature_thread.start()

    high_temp_thread = threading.Thread(target=toggle_high_temperature)
    high_temp_thread.daemon = True
    high_temp_thread.start()

    app.run(debug=True)
