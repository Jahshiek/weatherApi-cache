from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_limiter import Limiter
import os
import json
import requests 
import redis
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)

redis_password = os.getenv('REDIS_PASSWORD')
redis_host = os.getenv('REDIS_HOST')
redis_port = int(os.getenv('REDIS_PORT', 6379))


try:
    redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    redis_client.ping()
except redis.ConnectionError:
    print("⚠️ Redis server not available! Ensure Redis is running.")



limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50 per day"],
    storage_uri=f"redis://:{redis_password}@{redis_host}:{redis_port}/0" 
)


API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/', methods=['GET'])
def home():
    return 'This is the <h1>HOME PAGE</h1>'


@app.route('/weather/<location>', methods=['GET'])
@limiter.limit("10 per minute")
def get_weather(location):
    cached_weather = redis_client.get(location)

    if cached_weather:
        return jsonify({"source": "cache", "data": json.loads(cached_weather)})
    
    else:
        api_url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=us&key={API_KEY}&contentType=json'
        response = requests.get(api_url)
        weather_data = response.json()
        if response.status_code == 200:
            redis_client.setex(location, 3600, json.dumps(weather_data))
            return jsonify({"source": "API", "message": "Weather data fetched", "data":weather_data}), 200

        else:
            return jsonify({"error": "Failed to fetch weather"}), 500




if __name__ == '__main__':
    app.run(debug=True, port=8080)
