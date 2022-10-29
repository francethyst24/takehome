from django.shortcuts import render
from django.conf import settings
import requests
import json

# Create your views here.


def index(request):
    context = dict()
    context['city_list'] = fetch_cities(request)
    context['city_field'] = 'City not in list? Try here'
    return render(request, 'weather/index.html', context)


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
