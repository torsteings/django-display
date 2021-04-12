from django.shortcuts import render
from django import forms
import requests

class NameForm(forms.Form):
    place = forms.CharField(label='Velg holdeplass', max_length=100)

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            place = form.cleaned_data['place']
            air_temperature = index(place)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'name.html', {
            'place': place,
            'variable': air_temperature
            })
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'index.html', {'form': form})

def index(place):
    # tar inn navn på buss-stopp og henter koordinatene fra Entur/Ruter
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

    # henter temperaturdata fra Yr for valgte koordinater (maks fire desimaler)
    url_yr = "https://api.met.no/weatherapi/nowcast/2.0/complete?lat=" + str_lat + "&lon=" + str_lon
    headers = {"User-Agent": "torsteings torstein.skarsgard@gmail.com"}
    r = requests.get(url_yr, headers=headers)
    air_temperature = r.json()['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
    return air_temperature
