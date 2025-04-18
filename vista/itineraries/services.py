import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

def generate(source, destination, start_date, end_date, no_of_days,travel_mode, budget):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"Create a detailed travel itinerary for a trip from {source} to {destination} starting on {start_date} and ending on {end_date}, for {no_of_days} days, with a budget of {budget} rupees via {travel_mode}. Include daily activities, recommendations for places to visit, where to eat, and tips for transportation."
                ),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )
    itinerary = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        itinerary += chunk.text
    return itinerary

#generate()

import requests

load_dotenv()  # Loads .env file

def get_weather(city, start_date, end_date):

    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    print("🌍 City requested:", city)
    print("📅 Start Date:", start_date)
    print("📅 End Date:", end_date)

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{start_date}/{end_date}?unitGroup=metric&key={WEATHER_API_KEY}&include=days"

    print("🌐 Requesting URL:", url)

    response = requests.get(url)
    print("📥 Raw Response Text:", response.text)  # <-- Debug this!

    try:
        data = response.json()
    except Exception as e:
        print("❌ Failed to decode JSON:", str(e))
        return None

    if 'days' in data:
        forecast = [
            {
                'datetime': day['datetime'],
                'tempmax': day['tempmax'],
                'tempmin': day['tempmin'],
                'humidity': day['humidity'],
                'description': day.get('description', 'No description')
            }
            for day in data['days']
        ]
        return forecast
    else:
        print("⚠️ 'days' not found in data")
        return None
import os
import requests
from dotenv import load_dotenv

load_dotenv()
PLACES_API_KEY = os.getenv("PLACES_API_KEY")

def get_places(lat, lng, place_type='restaurant', api_key=PLACES_API_KEY):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f'{lat},{lng}',
        'radius': 10000,
        'type': place_type,
        'key': api_key
    }
    response = requests.get(url, params=params)
    print("🔍 Places API Response:", response.text)
    return response.json().get('results', [])

   
