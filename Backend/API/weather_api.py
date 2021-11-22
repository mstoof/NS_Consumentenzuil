import json
import requests
import datetime


def weather_api(city):
    app_id = 'f1eebb9a2860f4d87087f1bfe7e95979'

    if city == 'Utrecht':
        lat = '52.091824'
        lon = '5.119281'
    url2 = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={app_id}&units=metric'

    response = requests.get(url2)
    data = json.loads(response.text)
    temperatures = {}
    date = datetime.datetime.now()

    temperatures.update({'today': {
        'temperature': data['current']['temp'],
        'feels_like': data['current']['feels_like'],
        'humidity': data['current']['humidity'],
        'type_of_weather': data['current']['weather'][0]['main'],
        'weather_description': data['current']['weather'][0]['description']
    }})
    for index, variable in enumerate(data['daily']):
        new_date = date + datetime.timedelta(days=index + 1)
        short_date = new_date.strftime('%a')
        temp_min = variable['temp']['min']
        temp_max = variable['temp']['max']
        type_of_weather = variable['weather'][0]['main']

        temperatures.update({short_date: {
            'temperature_max': temp_max,
            'temperature_min': temp_min,
            'type_of_weather': type_of_weather
        }})

    return temperatures


if __name__ == '__main__':
    print(weather_api('Utrecht'))
