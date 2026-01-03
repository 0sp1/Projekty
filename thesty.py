import requests

API_KEY = "YOUR_API_KEY"  # Get one from https://openweathermap.org/api
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        r = requests.get(BASE_URL, params=params)
        r.raise_for_status()
        data = r.json()
        if data.get("cod") != 200:
            print("City not found.")
            return
        show_weather(data)
    except requests.RequestException:
        print("Error fetching weather data.")

def show_weather(data):
    city = data["name"]
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"].capitalize()
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    print(f"\nWeather in {city}:")
    print(f"Temperature: {temp}°C")
    print(f"Condition: {desc}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind} m/s\n")

def main():
    print("=== Simple Weather App ===")
    print("Type 'exit' to quit.")
    while True:
        city = input("Enter city name: ").strip()
        if city.lower() == "exit":
            print("Goodbye!")
            break
        if city:
            get_weather(city)

if __name__ == "__main__":
    main()
import random
import string

def show_menu():
    print("🔐 Password Generator")
    print("1. Letters only")
    print("2. Letters & digits")
    print("3. Letters, digits & symbols")

def generate_password(length, charset):
    return ''.join(random.choice(charset) for _ in range(length))

def main():
    while True:
        show_menu()
        choice = input("Choose option (1/2/3): ")
        
        try:
            length = int(input("Enter password length: "))
        except ValueError:
            print("⚠️ Invalid length.")
            continue

        if choice == '1':
            chars = string.ascii_letters
        elif choice == '2':
            chars = string.ascii_letters + string.digits
        elif choice == '3':
            chars = string.ascii_letters + string.digits + string.punctuation
        else:
            print("⚠️ Invalid choice.")
            continue

        password = generate_password(length, chars)
        print(f"🔑 Your password: {password}")

        again = input("Generate another? (y/n): ").lower()
        if again != 'y':
            print("👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
