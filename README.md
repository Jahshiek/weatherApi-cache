# 🌦️ Weather API with Flask, Redis & Rate Limiting  

This project is a simple **Weather API** built using **Flask**. It fetches weather data from an external API (e.g., [Visual Crossing](https://www.visualcrossing.com/)), caches results in **Redis**, and implements **rate limiting** to prevent abuse.  

## 🚀 Features  
✅ Fetches real-time weather data from an external API  
✅ **In-memory caching** with Redis to improve performance  
✅ **Rate limiting** (10 requests per minute per user) to prevent API abuse  
✅ Uses **environment variables** for security (API keys, Redis credentials)  
✅ Returns JSON-formatted responses  

## 📌 How It Works  
1. A user makes a **GET request** to `/weather/<location>` (e.g., `/weather/new-york`).  
2. The API checks **Redis** for cached data:  
   - **If found** → Returns cached weather data.  
   - **If not found** → Calls the external weather API, stores the result in Redis (with expiration), and returns it.  
3. Limits users to **10 requests per minute**.  
4. If the weather API is down, the system handles errors gracefully.  

## 🛠️ Setup Instructions  
### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/your-username/weather-api.git
cd weather-api
```

### 2️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables  
Create a `.env` file in the root directory and add:  
```ini
WEATHER_API_KEY=your_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
```

### 4️⃣ Run Redis Server  
If you don’t have Redis installed, you can run it via Docker:  
```bash
docker run -d --name redis-server -p 6379:6379 redis
```

### 5️⃣ Start the Flask API  
```bash
python app.py
```

## 🔥 API Endpoints  
### ✅ **Get Weather Data**  
```http
GET /weather/<location>
```
#### **Example Request:**  
```bash
curl http://127.0.0.1:8080/weather/new-york
```
#### **Example Response:**  
```json
{
    "source": "API",
    "message": "Weather data fetched",
    "data": {
        "temperature": 75,
        "condition": "Sunny"
    }
}
```
- The **first request** fetches from the API and caches it in Redis.  
- Subsequent requests **within 12 hours** return cached data (`"source": "cache"`).  

### ❌ **Rate Limit Exceeded**  
If a user exceeds 10 requests per minute:  
```json
{
    "error": "Too many requests"
}
```

## 💡 Best Practices & Tips  
✅ **Use environment variables** for API keys and sensitive credentials.  
✅ **Implement proper error handling** (e.g., handling API failures).  
✅ **Use Redis for caching** to reduce external API calls.  
✅ **Set cache expiration** to avoid serving outdated weather data.  
✅ **Implement rate limiting** using `flask-limiter` to prevent excessive usage.  

## 📚 Additional Resources  
🔗 [Visual Crossing Weather API (FREE)](https://www.visualcrossing.com/)  
🔗 [Redis In-Memory Caching](https://redis.io/)  
🔗 [Rate Limiting in Flask](https://flask-limiter.readthedocs.io/)  
🔗 [Project Roadmap](https://roadmap.sh/projects/weather-api-wrapper-service)  
