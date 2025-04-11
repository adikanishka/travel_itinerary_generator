import requests
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
# Constants
PLACES_API_KEY = os.getenv('PLACES_API_KEY')
def get_coordinates(city_name, api_key):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None

