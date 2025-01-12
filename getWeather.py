import requests
import argparse
from datetime import datetime



def get_forecast(latitude=37.554169, longitude=-122.313057, name=None):
    """
    Fetches the weather forecast for a specific location from the Open-Meteo API.
    
    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        name (str): City name (optional)
        Default: San Mateo, CA
    
    Returns:
        dict: Forecast data for the 3 days.
    """
    base_url = "https://api.open-meteo.com/v1/forecast"
    # API webpage examples and request url generator
    # https://open-meteo.com/en/docs#hourly=temperature_2m,precipitation_probability&timezone=America%2FLos_Angeles&forecast_days=1
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation_probability",
        "timezone": "America/Los_Angeles",  # Set timezone to Pacific Time
        "forecast_days": 3,
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract today's date
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Filter forecast data for today
        forecast = {
            "morning": {"temperature": None, "precipitation_probability": None},
            "afternoon": {"temperature": None, "precipitation_probability": None},
            "evening": {"temperature": None, "precipitation_probability": None}
        }
        
        for time, temp, precip in zip(data['hourly']['time'], data['hourly']['temperature_2m'], data['hourly']['precipitation_probability']):
            if today in time:
                hour = int(time.split('T')[1].split(':')[0])
                if 0 <= hour < 12:
                    forecast['morning'] = {"temperature": temp, "precipitation_probability": precip}
                elif 12 <= hour < 18:
                    forecast['afternoon'] = {"temperature": temp, "precipitation_probability": precip}
                elif 18 <= hour < 24:
                    forecast['evening'] = {"temperature": temp, "precipitation_probability": precip}
        
        return forecast
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_city_coordinates(city_name):
    """
    Returns the latitude and longitude for a given city in California.
    Args:
        city_name (str): Name of the city.
    
    Returns:
        dict: Dictionary with 'latitude' and 'longitude' keys or None if not found.
    """
    # TODO: A comprehensive CSV file (or API call)
    cityname_key = city_name.lower().replace(" ", "_").strip()
    cities = {
        "san_francisco": { "name": "San Francisco", "latitude": 37.7749, "longitude": -122.4194 },
        "san_mateo": {"name": "San Mateo", "latitude":37.554169, "longitude": -122.313057},
        "los_angeles": {"name": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437},
        "san_mateo": {"name": "San Mateo", "latitude": 32.7157, "longitude": -117.1611},
        "seattle": {"name": "Seattle", "latitude": 47.60621, "longitude": -122.33207}
    }
    return cities.get(cityname_key)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get weather forecast for a city.")
    parser.add_argument(
            "--city",
            type=str,
            default="San Mateo",  # Default city
            help="Name of the city (e.g., 'San Francisco', 'Los Angeles', 'San Diego'). Default is 'San Mateo'."
    )
    
    args = parser.parse_args()
    city_name = args.city
    coords = get_city_coordinates(city_name)
    
    if coords:
        print(f"Forecast for {city_name}:")
        forecast = get_forecast(coords['latitude'], coords['longitude'], name=city_name)
        if forecast:
            print(f"\t  Morning - Temperature: {forecast['morning']['temperature']}°C, Precipitation: {forecast['morning']['precipitation_probability']} %")        
            print(f"\t  Afternoon - Temperature: {forecast['afternoon']['temperature']}°C, Precipitation: {forecast['afternoon']['precipitation_probability']} %")
            print(f"\t  Evening - Temperature: {forecast['evening']['temperature']}°C, Precipitation: {forecast['evening']['precipitation_probability']} %")
    else:
        print(f"City '{city_name}' not found in the database. Please use 'San Francisco', 'Los Angeles', or 'San Diego'.")
