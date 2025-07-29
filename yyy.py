import requests

API_KEY = "your_api_key_here"  # Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            print(f"❌ Error: {data.get('message', 'Unknown error')}")
            return

        temp = data['main']['temp']
        desc = data['weather'][0]['description'].capitalize()
        humidity = data['main']['humidity']
        wind = data['wind']['speed']

        print(f"\n📍 Weather in {city.title()}:")
        print(f"🌡️ Temp: {temp}°C")
        print(f"🌥️ Condition: {desc}")
        print(f"💧 Humidity: {humidity}%")
        print(f"💨 Wind: {wind} m/s")

    except Exception as e:
        print("⚠️ Failed to fetch weather data:", e)

def main():
    print("🌤️ Weather Checker")
    while True:
        city = input("\nEnter city name (or 'exit' to quit): ")
        if city.lower() == 'exit':
            print("👋 Goodbye!")
            break
        get_weather(city)

if __name__ == "__main__":
    main()
