from django.shortcuts import render
from django.conf import settings
import requests
import json
import math

# Create your views here.
PARAM_CITY = 'q'


def index(request):
    context = dict()
    context['ui_txt'] = fetch_ui_text()
    context['city_data'] = fetch_cities(request)
    context['weather_data'] = fetch_weather(request)
    return render(request, 'weather/index.html', context)


def fetch_ui_text():
    return {
        'title_tab': 'Current Weather',
        'field_city': 'City not in the list? Try here',
        'label_feels_like': 'Feels like',
        'label_humidity': 'Humidity',
        'param_city': PARAM_CITY,
        'btn_search': 'Search'
    }


def fetch_cities(request):
    response = requests.get(
        'https://countriesnow.space/api/v0.1/countries/capital'
    )
    countryList = json.loads(response.content.decode())['data']
    cityList = []
    for country in countryList:
        if country['capital']:
            cityList.append(country['capital'].strip())
    return sorted(cityList)


def fetch_weather(request):
    query = request.GET.get(PARAM_CITY)
    if not query:
        return
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': query.strip(),
        'APPID': settings.WEATHER_API_KEY,
        'units': 'metric',
    }
    response = requests.get(url, params=params)
    data = json.loads(response.content.decode())
    imgLibUrl = 'http://openweathermap.org/img/wn'
    return {
        'city_name': f"{data['name']}, {data['sys']['country']}",
        'temp': f"{math.floor(data['main']['temp'])}°C",
        'feels_like': f"{math.floor(data['main']['feels_like'])}°C",
        'humidity': f"{data['main']['humidity']}%",
        'description': data['weather'][0]['description'],
        'icon_url': f"{imgLibUrl}/{data['weather'][0]['icon']}@2x.png",
    }
