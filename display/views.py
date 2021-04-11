from django.shortcuts import render
import requests

# Create your views here.
from django.http import HttpResponse

def index(request):
    # Tar inn navn på buss-stopp og henter koordinatene fra Entur/Ruter
    endpoint_entur = "https://api.entur.io/geocoder/v1/autocomplete?text="
    bus_stop = "Storo"
    params_entur = "&size=10&lang=n"
    url_entur = endpoint_entur + bus_stop + params_entur
    r = requests.get(url_entur)

    coordinates = r.json()['features'][0]['geometry']['coordinates']

    lat = round(coordinates[1], 4)
    lon = round(coordinates[0], 4)
    str_lat = str(lat)
    str_lon = str(lon)

    # Henter temperaturdata fra Yr for valgte koordinater (maks fire desimaler)
    url_yr = "https://api.met.no/weatherapi/nowcast/2.0/complete?lat=" + str_lat + "&lon=" + str_lon
    headers = {"User-Agent": "torsteings torstein.skarsgard@gmail.com"}
    r = requests.get(url_yr, headers=headers)

    air_temperature = r.json()['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
    print("Temperaturen ved", bus_stop, "er", air_temperature, "grader celcius akkurat nå")

    return render(request, 'index.html', {'variable': air_temperature})
