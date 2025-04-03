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