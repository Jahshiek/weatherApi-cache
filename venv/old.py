from flask import Flask, jsonify, request
import json
import redis
import os
import requests  # Import requests for API calls
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
)
try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.ping()
except redis.ConnectionError:
    print("⚠️ Redis server not available! Ensure Redis is running.")

API_KEY = os.getenv('WEATHER_API_KEY')

if not API_KEY:
    print('Api Key is missing')


@app.route('/weather/<location>', methods=['GET'])
@limiter.limit("5 per minute")
def get_weather(location):
    #initialize key value pair
    cache_key = f'{location.lower()}'
    cache_weater_value = r.get(cache_key)
    #check cache
    if cache_weater_value:
        status = "Using cached data from Redis"
        print(status)
        response = json.loads(cache_weater_value)
    #fetch to api and add to cache
    else:
        api_url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=us&key={API_KEY}&contentType=json'
        res = requests.get(api_url)  # request call
        

        # response = json.loads(res.text)
        response = res.json()
        status = "fetching data from api and storing cahced data in redis data from Redis"
        r.setex(cache_key, 300, json.dumps(response)) 
        print(status)


    # return jsonify({"message": status, "data": response}), 200  


if __name__ == "__main__":
    app.run()