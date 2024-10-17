import requests
import time
from datetime import datetime

# Параметры для API Ecowitt
ecowitt_application_key = "YOUR_ECOWITT_APPLICATION_KEY"  # Замените на ваш ключ приложения
ecowitt_api_key = "YOUR_ECOWITT_API_KEY"  # Замените на ваш API ключ
ecowitt_mac = "YOUR_ECOWITT_MAC"  # Замените на MAC адрес вашего устройства Ecowitt

# Ваш уникальный MAC-адрес прибора для Народного Мониторинга
narodmon_device_mac = "YOUR_NARODMON_DEVICE_MAC"  # Замените на ваш MAC-адрес

def get_ecowitt_data():
    print(f"[{datetime.now()}] Получение данных с Ecowitt API...")
    endpoint = f"https://api.ecowitt.net/api/v3/device/real_time?application_key={ecowitt_application_key}&api_key={ecowitt_api_key}&mac={ecowitt_mac}&temp_unitid=1&pressure_unitid=5&wind_speed_unitid=7&rainfall_unitid=12&solar_irradiance_unitid=16"
    try:
        response = requests.get(endpoint)
        data = response.json()
        print(f"[{datetime.now()}] Ответ от Ecowitt API: {data}")
        if data['code'] == 0:
            weather_data = data['data']
            # Извлекаем все необходимые данные
            outdoor_data = weather_data['outdoor']
            wind_data = weather_data['wind']
            pressure_data = weather_data['pressure']
            rainfall_data = weather_data['rainfall']
            solar_and_uvi_data = weather_data['solar_and_uvi']

            # Возвращаем данные в формате, который передадим на Народный Мониторинг
            return {
                'temperature': outdoor_data['temperature']['value'],  # Температура
                'humidity': outdoor_data['humidity']['value'],        # Влажность
                'pressure': pressure_data['relative']['value'],       # Давление
                'wind_speed': wind_data['wind_speed']['value'],       # Скорость ветра
                'wind_gust': wind_data['wind_gust']['value'],         # Порывы ветра
                'wind_direction': wind_data['wind_direction']['value'],  # Направление ветра
                'rain_rate': rainfall_data['rain_rate']['value'],     # Интенсивность дождя
                'solar': solar_and_uvi_data['solar']['value'],        # Солнечная радиация
                'uvi': solar_and_uvi_data['uvi']['value']             # УФ-индекс
            }
        else:
            print(f"[{datetime.now()}] Ошибка при получении данных с Ecowitt API: {data['message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Ошибка соединения с Ecowitt API: {e}")
        return None

def send_to_narodmon(data):
    print(f"[{datetime.now()}] Отправка данных на Народный Мониторинг...")
    payload = {
        'ID': narodmon_device_mac,
        'T1': data['temperature'],      # Температура
        'H1': data['humidity'],         # Влажность
        'P1': data['pressure'],         # Давление
        'W1': data['wind_speed'],       # Скорость ветра
        'G1': data['wind_gust'],        # Порывы ветра
        'D1': data['wind_direction'],   # Направление ветра
        'R1': data['rain_rate'],        # Интенсивность дождя
        'S1': data['solar'],            # Солнечная радиация
        'U1': data['uvi'],              # УФ-индекс
        # Добавьте дополнительные датчики при необходимости
    }

    try:
        response = requests.post('http://narodmon.ru/post', data=payload, timeout=5)
        if response.status_code == 200:
            print(f"[{datetime.now()}] Данные успешно отправлены на Народный Мониторинг")
            print(f"[{datetime.now()}] Ответ сервера: {response.text}")
        else:
            print(f"[{datetime.now()}] Ошибка при отправке данных: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Ошибка соединения с Народным Мониторингом: {e}")

def main():
    while True:
        print(f"[{datetime.now()}] Старт цикла обновления данных...")
        weather_data = get_ecowitt_data()
        if weather_data:
            send_to_narodmon(weather_data)
        print(f"[{datetime.now()}] Пауза на 5 минут перед следующим обновлением...")
        time.sleep(300)  # Пауза в 300 секунд (5 минут)

if __name__ == "__main__":
    main()
