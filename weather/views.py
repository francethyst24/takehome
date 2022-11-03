from django.shortcuts import render
from django.conf import settings
import requests
import math

# Create your views here.
PARAM_CITY = 'q'

ERR_API_CITIES = 1
ERR_API_WEATHER = 2

ERR_MSG_CITIES = 'Failed to retrieve cities'
ERR_MSG_WEATHER = 'Failed to retrieve weather'


def index(request):
    context = dict()
    context['ui_txt'] = fetch_ui_text()
    context['error_msg'] = []

    if result := fetch_cities(request):
        if (result == ERR_API_CITIES):
            context['error_msg'].append(ERR_MSG_CITIES)
        else:
            context['city_data'] = result

    if result := fetch_weather(request):
        if (result == ERR_API_WEATHER):
            context['error_msg'].append(ERR_MSG_WEATHER)
        else:
            context['weather_data'] = result

    return render(request, 'weather/index.html', context)


def fetch_ui_text():
    return {
        'title_tab': 'DjangoWeather',
        'field_city': 'City not in the list? Try here',
        'label_feels_like': 'Feels like',
        'label_humidity': 'Humidity',
        'param_city': PARAM_CITY,
        'btn_search': 'Search',
        'label_empty_list': ERR_MSG_CITIES.replace('Failed', 'Unable')
    }


def fetch_cities(request):
    externalApiUrl = 'https://countriesnow.space/api/v0.1/countries/capital'
    try:
        response = requests.get(externalApiUrl)
        response.raise_for_status()
        countryList = response.json()['data']
        cityList = []
        for country in countryList:
            if country['capital']:
                cityList.append(country['capital'].strip())
        return sorted(cityList)
    except requests.RequestException as e:
        return ERR_API_CITIES


def fetch_weather(request):
    queriedCity = request.GET.get(PARAM_CITY)
    if queriedCity is None:
        return None
    try:
        externalApiUrl = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'units': 'metric',
            'APPID': settings.WEATHER_API_KEY,
            PARAM_CITY: queriedCity.strip(),
        }
        response = requests.get(externalApiUrl, params=params)
        response.raise_for_status()
        data = response.json()
        iconUrl = 'http://openweathermap.org/img/wn/ICON_CODE@2x.png'
        return {
            'city_name': f"{data['name']}, {data['sys']['country']}",
            'temp': f"{math.floor(data['main']['temp'])}°C",
            'feels_like': f"{math.floor(data['main']['feels_like'])}°C",
            'humidity': f"{data['main']['humidity']}%",
            'description': data['weather'][0]['description'],
            'icon_url': iconUrl.replace('ICON_CODE', data['weather'][0]['icon']),
        }
    except requests.RequestException as e:
        return ERR_API_WEATHER
