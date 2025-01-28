from flask import Flask, render_template
from datetime import datetime
import requests
import psutil

app = Flask(__name__)

def get_temperature():
    # Replace this with actual temperature sensor reading for Raspberry Pi
    # For example, using a DS18B20 sensor
    try:
        # Simulate temperature reading
        return round(psutil.sensors_temperatures()['cpu_thermal'][0].current, 1)
    except:
        return 20.0  # Default value

def get_weather():
    # Replace with actual weather API call
    return {
        'condition': 'Cloudy',
        'temperature': 16
    }

@app.route('/')
def dashboard():
    context = {
        'time': datetime.now().strftime('%H:%M:%S'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'temperature': get_temperature(),
        'weather': get_weather()
    }
    return render_template('dashboard.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
