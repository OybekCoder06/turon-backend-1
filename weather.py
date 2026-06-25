import requests
from datetime import datetime

# 1. Model - Ma'lumotlarni saqlovchi klass
class Weather:
    def __init__(self, city_name, temperature, humidity, description):
        self.city_name = city_name
        self.temperature = temperature
        self.humidity = humidity
        self.description = description
        # Hozirgi vaqtni olish va formatlash
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def show_info(self):
        print(f"\n[{self.time}] {self.city_name} shahri ob-havosi:")
        print(f"Harorat: {self.temperature}°C")
        print(f"Namlik: {self.humidity}%")
        print(f"Holat: {self.description.capitalize()}")
        print("-" * 30)

# 2. Client - API bilan ishlovchi klass
class WeatherClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def fetch_weather(self, city):
        # API uchun kerakli parametrlar
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'  # Haroratni Selsiyda olish uchun
        }
        
        try:
            # Serverga GET so'rov yuborish
            response = requests.get(self.base_url, params=params)
            
            # Agar javob muvaffaqiyatli bo'lsa (200 OK)
            if response.status_code == 200:
                data = response.json()  # JSON formatni lug'atga (dictionary) o'tkazish
                
                # JSON ichidan o'zimizga kerakli ma'lumotlarni tortib olamiz
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                desc = data['weather'][0]['description']
                
                # Weather obyektini yaratib, uni qaytaramiz
                return Weather(city, temp, humidity, desc)
            else:
                print(f"Xatolik: {city} shahri topilmadi yoki API kalit xato.")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Tarmoqda xatolik yuz berdi: {e}")
            return None

# 3. Dasturni ishga tushirish qismi
if __name__ == "__main__":
    # DIQQAT: O'zingizning OpenWeatherMap API kalitingizni shu yerga yozing!
    MY_API_KEY = "52842cfb691c0309214d3e218917f245"
    
    # Client obyektini yaratamiz
    client = WeatherClient(MY_API_KEY)
    
    while True:
        shahar = input("Shahar nomini kiriting (chiqish uchun 'q' bosing): ")
        if shahar.lower() == 'q':
            print("Dastur to'xtadi.")
            break
            
        # Client orqali ob-havo ma'lumotini (Weather obyektini) olamiz
        weather_info = client.fetch_weather(shahar)
        
        # Agar ma'lumot muvaffaqiyatli kelsa, ekranga chiqaramiz
        if weather_info:
            weather_info.show_info()
