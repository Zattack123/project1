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

def pm25_graph(request):
    qs = City.objects.all();
    x = [x.name for x in qs]
    y = [y.max_pm_25 + y.min_pm_25 for y in qs]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Pm2.5 Conectration Per City')
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("City Name")
    plt.ylabel('PM2.5 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})


def pollution_concentration(request, pk):
    city = get_object_or_404(City, pk=pk)
    #city = City.objects.get(name='Lexington')[:0]
    data = [city.max_c_co, city.max_c_co2, city.max_c_hc, city.max_c_no]
    labels = "CO", "C02", "HC", "NO"
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    chart = get_graph()
    return render(request, 'graph.html', {'chart':chart})
