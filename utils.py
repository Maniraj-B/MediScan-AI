import requests
import json

def calculate_risk(symptom_count):
    if symptom_count == 0:
        return "Low"
    elif symptom_count <= 3:
        return "Medium"
    else:
        return "High"

def get_advice(risk, disease=None):
    base_advice = {
        "Low": "Maintain a healthy lifestyle, stay hydrated, and get adequate sleep.",
        "Medium": "Rest well, monitor symptoms, take OTC medication if needed, consult doctor if persists.",
        "High": "Consult a doctor immediately. Avoid self-medication and seek professional help."
    }
    
    disease_specific = {
        "Influenza": " Rest and antivirals may help. Stay isolated to prevent spread.",
        "COVID-19": " Isolate immediately, test, and follow health guidelines.",
        "Migraine": " Rest in dark room, avoid triggers, consider pain relievers.",
        "Gastroenteritis": " Stay hydrated with ORS, bland diet, avoid dairy."
    }
    
    advice = base_advice.get(risk, base_advice["Medium"])
    if disease and disease in disease_specific:
        advice += disease_specific[disease]
    
    return advice

def future_persona(risk):
    if risk == "High":
        return {
            "bad": "⚠️ Condition may worsen significantly. Risk of complications increases without treatment.",
            "good": "✅ With proper medical care, recovery expected within 3-5 days. Follow doctor's advice."
        }
    elif risk == "Medium":
        return {
            "bad": "⚠️ Symptoms may persist and affect daily activities for several days.",
            "good": "✅ Rest and proper care can lead to recovery within 2-3 days."
        }
    else:
        return {
            "bad": "⚠️ Minor health issues may develop if preventive measures are ignored.",
            "good": "✅ Maintain current healthy habits to stay fit and prevent future illnesses."
        }

def mental_health_response(mood):
    responses = {
        "good": "🌟 Great to hear! Keep up the positive mindset. Try gratitude journaling to maintain it.",
        "stressed": "😌 Take a deep breath. Try the 5-4-3-2-1 grounding technique or a 5-min meditation.",
        "low": "💙 You're not alone. Consider talking to a friend or professional. Try a small walk or your favorite music.",
        "overwhelmed": "🤗 It's okay to feel this way. Break tasks into small steps. Reach out to a helpline if needed."
    }
    return responses.get(mood, "💚 Take care of your mental health. Even 5 minutes of self-care helps.")

def get_weather_health_advice():
    """Fetch weather data based on IP location and return health advice"""
    try:
        # Get location from IP
        ip_response = requests.get('https://ipapi.co/json/', timeout=5)
        if ip_response.status_code == 200:
            location = ip_response.json()
            city = location.get('city', 'your area')
            lat = location.get('latitude')
            lon = location.get('longitude')
            
            if lat and lon:
                # Get weather from Open-Meteo (no API key required)
                weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
                weather_resp = requests.get(weather_url, timeout=5)
                if weather_resp.status_code == 200:
                    weather = weather_resp.json()['current_weather']
                    temp = weather['temperature']
                    
                    advice = f"🌡️ In {city}, it's {temp}°C. "
                    if temp < 10:
                        advice += "Cold weather: Dress warmly to avoid respiratory issues."
                    elif temp > 30:
                        advice += "Hot weather: Stay hydrated and avoid peak sun hours."
                    else:
                        advice += "Pleasant weather for outdoor activities. Maintain regular exercise."
                    return advice
        return "🌤️ Check local weather for personalized health tips. Stay active and hydrated!"
    except:
        return "🌍 Unable to fetch weather. General advice: maintain hygiene and stay active."

def get_health_news():
    """Fetch health news from RSS feed (optional external API)"""
    try:
        # Using rss2json free service
        url = "https://api.rss2json.com/v1/api.json?rss_url=https://www.who.int/feeds/entity/news-room/feature-stories/en/rss.xml"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('items', [])[:3]
            return [{'title': item['title'], 'link': item['link']} for item in articles]
    except:
        pass
    return []