"""
Weather Service - Fetches real-time weather data from Open-Meteo API.
"""

import httpx


async def get_weather_data(latitude: float, longitude: float):
    """
    Fetch current weather and 7-day forecast from Open-Meteo.
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
    
    Returns:
        dict with current weather, forecast, and soil conditions
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Current weather + 7-day forecast
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,rain,wind_speed_10m,weather_code",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,weather_code",
                "timezone": "Asia/Kolkata",
                "forecast_days": 7
            }
            
            response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params=params
            )
            
            if response.status_code != 200:
                return _fallback_weather()
            
            data = response.json()
            
            # Parse current weather
            current = data.get("current", {})
            current_weather = {
                "temperature": current.get("temperature_2m", 25),
                "humidity": current.get("relative_humidity_2m", 65),
                "rain": current.get("rain", 0),
                "wind_speed": current.get("wind_speed_10m", 10),
                "condition": _weather_code_to_text(current.get("weather_code", 0)),
                "icon": _weather_code_to_icon(current.get("weather_code", 0)),
            }
            
            # Parse daily forecast
            daily = data.get("daily", {})
            forecast = []
            dates = daily.get("time", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            precip = daily.get("precipitation_sum", [])
            wind = daily.get("wind_speed_10m_max", [])
            codes = daily.get("weather_code", [])
            
            for i in range(min(7, len(dates))):
                forecast.append({
                    "date": dates[i] if i < len(dates) else "",
                    "temp_max": max_temps[i] if i < len(max_temps) else 30,
                    "temp_min": min_temps[i] if i < len(min_temps) else 20,
                    "precipitation": precip[i] if i < len(precip) else 0,
                    "wind_speed": wind[i] if i < len(wind) else 10,
                    "condition": _weather_code_to_text(codes[i] if i < len(codes) else 0),
                    "icon": _weather_code_to_icon(codes[i] if i < len(codes) else 0),
                })
            
            # Soil conditions estimate
            soil_conditions = {
                "moisture": "Adequate" if current_weather["rain"] > 2 else ("Dry" if current_weather["humidity"] < 40 else "Moderate"),
                "temperature": f"{current_weather['temperature'] - 2:.1f}°C",
                "status": "Good" if 20 <= current_weather["temperature"] <= 35 else "Monitor"
            }
            
            # Agronomy insight
            weather_insight = _generate_insight(current_weather, forecast)
            
            return {
                "current": current_weather,
                "forecast": forecast,
                "soil_conditions": soil_conditions,
                "insight": weather_insight,
                "source": "Open-Meteo",
                "available": True
            }
    except Exception as e:
        print(f"Weather API error: {e}")
        return _fallback_weather()


async def geocode_location(location_name: str):
    """
    Convert location name to coordinates using Open-Meteo Geocoding.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": location_name, "count": 1, "language": "en", "format": "json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if results:
                    return {
                        "latitude": results[0]["latitude"],
                        "longitude": results[0]["longitude"],
                        "name": results[0].get("name", location_name),
                        "country": results[0].get("country", "India"),
                        "found": True
                    }
    except Exception as e:
        print(f"Geocoding error: {e}")
    
    # Default to central India
    return {
        "latitude": 21.1458,
        "longitude": 79.0882,
        "name": location_name or "Nagpur",
        "country": "India",
        "found": False
    }


def _weather_code_to_text(code):
    """Convert WMO weather code to human text."""
    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Severe Thunderstorm"
    }
    return codes.get(code, "Clear")


def _weather_code_to_icon(code):
    """Convert WMO weather code to Material Symbols icon name."""
    if code == 0:
        return "sunny"
    elif code in (1, 2):
        return "partly_cloudy_day"
    elif code == 3:
        return "cloud"
    elif code in (45, 48):
        return "foggy"
    elif code in (51, 53, 55, 61, 63, 80, 81):
        return "rainy"
    elif code in (65, 82):
        return "thunderstorm"
    elif code in (71, 73, 75):
        return "weather_snowy"
    elif code in (95, 96, 99):
        return "thunderstorm"
    return "sunny"


def _generate_insight(current, forecast):
    """Generate farming-relevant insight from weather data."""
    temp = current["temperature"]
    humidity = current["humidity"]
    rain = current.get("rain", 0)
    
    insights = []
    
    if rain > 10:
        insights.append("Heavy rainfall expected. Avoid irrigation and ensure proper drainage.")
    elif rain > 2:
        insights.append("Light to moderate rain detected. Good natural watering conditions.")
    else:
        insights.append("No significant rainfall. Consider scheduled irrigation.")
    
    if temp > 40:
        insights.append("Extreme heat alert. Provide shade and extra water to crops.")
    elif temp > 35:
        insights.append("High temperatures. Monitor crops for heat stress and increase watering.")
    elif temp < 10:
        insights.append("Cold conditions. Protect sensitive crops from frost damage.")
    
    if humidity > 85:
        insights.append("High humidity increases fungal disease risk. Monitor crops closely.")
    elif humidity < 30:
        insights.append("Low humidity may cause crop dehydration. Ensure adequate irrigation.")
    
    # Check forecast for rainfall in next 3 days
    next_3_days_rain = sum(f.get("precipitation", 0) for f in forecast[:3])
    if next_3_days_rain > 20:
        insights.append("Significant rainfall expected in 3 days. Plan activities accordingly.")
    
    return " ".join(insights[:3])


def _fallback_weather():
    """Return fallback weather data when API is unavailable."""
    return {
        "current": {
            "temperature": 28,
            "humidity": 65,
            "rain": 0,
            "wind_speed": 12,
            "condition": "Partly cloudy",
            "icon": "partly_cloudy_day"
        },
        "forecast": [],
        "soil_conditions": {
            "moisture": "Moderate",
            "temperature": "26.0°C",
            "status": "Good"
        },
        "insight": "Weather data temporarily unavailable. Using estimated regional averages.",
        "source": "Estimated",
        "available": False
    }
