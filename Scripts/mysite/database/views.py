from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.db.models import Q, Sum
from django.http import JsonResponse, Http404
from django.urls import reverse


import matplotlib.pyplot as plot
import numpy as np
from io import BytesIO
import base64


from .models import City, Vehicle, PowerPlant
from .utils import get_plot


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
    y = [y.c_co2 for y in qs]
    
    chart = get_plot(x,y)
    return render(request, 'graph.html', {'chart': chart})
