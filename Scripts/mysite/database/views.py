from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.db.models import Q, Sum
from django.http import JsonResponse, Http404
from django.urls import reverse


import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64


from .models import City, Vehicle, PowerPlant
from .utils import get_graph


class DatabasePageView(TemplateView):
    model = PowerPlant
    template_name = 'database_home.html'

class CitySearchResultsView(ListView):
    model = City
    template_name = 'city_search_results.html'
    object_list = City.objects.all()

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        object_list = City.objects.filter(
            Q(name__icontains=query) | Q(state__icontains=query) | Q(date__icontains=query)
        )
        return object_list

class VehicleSearchResultsView(ListView):
    model = Vehicle
    template_name = 'vehicle_search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q' ,'')
        object_list = Vehicle.objects.filter(
            Q(automaker__icontains=query) | Q(trim__icontains=query) | Q(model_year__icontains=query)
        )
        return object_list

class PowerPlantSearchResultsView(ListView):
    model = PowerPlant
    template_name = 'powerplant_search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q' ,'')
        object_list = PowerPlant.objects.filter(
            Q(name__icontains=query) | Q(state__icontains=query)
        )
        return object_list



def c02_graph(request):
    qs = City.objects.all();
    x = [x.name for x in qs]
    y = [y.max_c_co2 + y.min_c_co2 for y in qs]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('CO2 Conectration Per City')
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("City Name")
    plt.ylabel('CO2 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})


def pollution_concentration(request, pk):
    city = get_object_or_404(City, pk=pk)
    #city = City.objects.get(name='Lexington')[:0]
    data = [city.max_c_co + city.min_c_co, city.max_c_co2 + city.min_c_co2,
        city.max_c_hc + city.min_c_hc, city.max_c_no + city.min_c_no, city.max_pm_25 + city.min_pm_25]
    labels = "CO", "C02", "HC", "NO", "PM25"
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    plt.title('Pollution Concentration for ' + city.name)
    chart = get_graph()
    return render(request, 'graph.html', {'chart':chart})


def pm25_graph_line(request, pk):
    city = get_object_or_404(City, pk=pk)
    dates = City.objects.filter(name=city.name).order_by('date')
    x = [x.date for x in dates]
    y = [y.max_pm_25 + y.min_pm_25 for y in dates]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Pm2.5 Conectration for ' + city.name)
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel('PM2.5 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})


def pm25_wind_graph(request, pk):
    city = get_object_or_404(City, pk=pk)
    wind = City.objects.filter(name=city.name).order_by('wind_direction')
    x = [x.wind_direction for x in wind]
    y = [y.max_pm_25 + y.min_pm_25 for y in wind]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Pm2.5 Conectration by Wind Direction in ' + city.name)
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Wind Direction")
    plt.ylabel('PM2.5 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})


def c02_wind_graph(request, pk):
    city = get_object_or_404(City, pk=pk)
    wind = City.objects.filter(name=city.name).order_by('wind_direction')
    x = [x.wind_direction for x in wind]
    y = [y.max_c_co2 + y.min_c_co2 for y in wind]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('C02 Conectration by Wind Direction in ' + city.name)
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Wind Direction")
    plt.ylabel('C02 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})

def c0_wind_graph(request, pk):
    city = get_object_or_404(City, pk=pk)
    wind = City.objects.filter(name=city.name).order_by('wind_direction')
    x = [x.wind_direction for x in wind]
    y = [y.max_c_co + y.min_c_co for y in wind]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('C0 Conectration by Wind Direction in ' + city.name)
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Wind Direction")
    plt.ylabel('C0 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})

def all_pollution(request, pk):
    city = get_object_or_404(City, pk=pk)
    dates = City.objects.filter(name=city.name).order_by('date')
    plt.switch_backend('AGG')
    plt.figure(figsize=(8,5))
    plt.title('Pollution Conectration in ' + city.name)
    x1 = [x1.date for x1 in dates]
    y1 = [y1.max_c_co + y1.min_c_co for y1 in dates]
    plt.plot(x1, y1, label="CO")

    x2 = [x2.date for x2 in dates]
    y2 = [y2.max_c_co2 + y2.min_c_co2 for y2 in dates]
    plt.plot(x2, y2, label="CO2")

    x3 = [x3.date for x3 in dates]
    y3 = [y3.max_c_hc + y3.min_c_hc for y3 in dates]
    plt.plot(x3, y3, label="HC")

    x4 = [x4.date for x4 in dates]
    y4 = [y4.max_c_no + y4.min_c_no for y4 in dates]
    plt.plot(x4, y4, label="NO")

    x5 = [x5.date for x5 in dates]
    y5 = [y5.max_pm_25 + y5.min_pm_25 for y5 in dates]
    plt.plot(x5, y5, label="PM25")
    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel('Concentration (ppm)')
    plt.legend()
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})





#def box_plot(request, pk):
#    city = get_object_or_404(City, pk=pk)
#    cities = City.objects.filter(name=city.name).order_by('date')
#    x = [x.date for x in cities]
#    y = [y.]
