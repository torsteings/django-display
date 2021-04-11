from django.shortcuts import render
import requests

# Create your views here.
from django.http import HttpResponse

def index(request):
    show = "text"
    return render(request, 'index.html', {'variable': show})
