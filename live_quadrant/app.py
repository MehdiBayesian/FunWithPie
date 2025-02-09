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


def get_seinfeld_quote():
    # Fetch quotes from the Seinfeld API
    local_quotes = [
        {
            "quote": "Yada yada yada",
            "character": "Elaine"
        },
        {
            "quote": "It's not a lie if you believe it.",
            "character": "George Costanza"
        },
        {
            "quote": "Yeah, and you're an anti-dentite.",
            "character": "Cosmo Kramer"
        },
        {
            "quote": "The sea was angry that day my friends.",
            "character": "George Costanza"
        },
        {
            "quote": "That's a shame.",
            "character": "Jerry Seinfeld"
        },
        {
            "quote": "Serenity now!",
            "character": "Frank Costanza"
        }
    ]
    selected = random.choice(local_quotes)
    return selected

    
@app.route('/')
def dashboard():
    context = {
        'time': datetime.now().strftime('%H:%M:%S'),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'temperature': get_temperature(),
        'weather': get_weather(),
        'family_photo': get_family_photo(),
        'seinfeld': get_seinfeld_quote(),
    }
    print(context)
    return render_template('dashboard.html', **context)

@app.route('/update_photo')
def update_photo():
    return {'photo': get_family_photo()}


@app.route('/update_seinfeld_quote')
def update_seinfeld_quote():
    return {"seinfeld": get_seinfeld_quote()}


if __name__ == '__main__':
    app.run(debug=True)
