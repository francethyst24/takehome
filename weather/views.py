from django.shortcuts import render
from django.conf import settings
import requests

# Create your views here.


def index(request):
    context = dict()
    return render(request, 'weather/index.html', context)
