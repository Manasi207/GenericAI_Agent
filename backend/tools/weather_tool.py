
# ###########################################################################################################################

# backend/tools/weather_tool.py - Simple weather tool using wttr.in

# tools/weather_tool.py
import os
import requests
from urllib.parse import quote_plus

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

def weather_tool_fn(city_name: str) -> str:
    city = city_name.strip()
    if not OPENWEATHER_API_KEY:
        return "⚠️ OpenWeather API key not set in .env file."

    q = quote_plus(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        j = r.json()
        name = j.get("name")
        sys = j.get("sys", {})
        country = sys.get("country", "")
        main = j.get("main", {})
        weather_arr = j.get("weather", [{}])
        desc = weather_arr[0].get("description", "") if weather_arr else ""
        temp = main.get("temp")
        feels = main.get("feels_like")
        humidity = main.get("humidity")
        wind = j.get("wind", {}).get("speed")

        parts = []
        if name:
            parts.append(f"⛅ Weather for {name}, {country}:")
        if desc:
            parts.append(desc.capitalize())
        if temp is not None:
            parts.append(f"🌡️ Temp: {temp}°C (feels like {feels}°C)")
        if humidity is not None:
            parts.append(f"💧 Humidity: {humidity}%")
        if wind is not None:
            parts.append(f"🌪️ Wind speed: {wind} m/s")
        return " | ".join(parts)
    except Exception as e:
        return f"❌ Error fetching weather: {e}"

