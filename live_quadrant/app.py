import os
import psutil
from flask import Flask, render_template
from datetime import datetime
import random

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
    # TODO: Replace with actual weather API call
    return {
        'condition': 'Cloudy',
        'temperature': 16
    }



def get_family_photo():
    image_folder = 'static/family_photos/'
    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    return random.choice(images) if images else 'default_photo.jpg'  # Fallback to default



@app.route('/')
def dashboard():
    context = {
        'time': datetime.now().strftime('%H:%M:%S'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'temperature': get_temperature(),
        'weather': get_weather(),
        'family_photo': get_family_photo()
    }
    return render_template('dashboard.html', **context)

@app.route('/update_photo')
def update_photo():
    return {'photo': get_family_photo()}


if __name__ == '__main__':
    app.run(debug=True)
