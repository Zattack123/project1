from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.db.models import Q, Sum
from django.http import JsonResponse, Http404, HttpResponse
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
        ).order_by("date")
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
    plt.title('CO2 Concentration Per City')
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("City Name")
    plt.ylabel('CO2 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})



def vehicle_pm25_graph(request):
    qs = Vehicle.objects.all();
    x = [x.model_year + x.automaker + x.trim for x in qs]
    y = [y.max_pm_25 + y.min_pm_25 for y in qs]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('PM25 Concentration Per Vehicle')
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Vehicle")
    plt.ylabel('PM25 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})


def pollution_concentration_pie(request, pk):
    city = get_object_or_404(City, pk=pk)
    data = [city.max_c_co + city.min_c_co, city.max_c_co2 + city.min_c_co2,
        city.max_c_hc + city.min_c_hc, city.max_c_no + city.min_c_no, city.max_pm_25 + city.min_pm_25]
    labels = "CO", "C02", "HC", "NO", "PM25"
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    plt.title('Particulate Concentration for ' + city.name + ' on ' + city.date)
    chart = get_graph()
    return render(request, 'graph.html', {'chart':chart})

def bar_graph(request, pk):
    city = get_object_or_404(City, pk=pk)
    dates = City.objects.filter(name=city.name).order_by('date')
    datesList = [z.date for z in dates]
    width = .1
    c0 = [x1.max_c_co + x1.min_c_co for x1 in dates]
    c02 = [x2.max_c_co2 + x2.min_c_co2 for x2 in dates]
    hc = [x3.max_c_hc + x3.min_c_hc for x3 in dates]
    no = [x4.max_c_no + x4.min_c_no for x4 in dates]
    pm25 = [x5.max_pm_25 + x5.min_pm_25 for x5 in dates]

    labels = 'C0', 'C02', 'HC', 'NO', 'PM25'
    y1 = np.arange(len(c0))
    y2 = [x + width for x in y1]
    y3 = [x + width for x in y2]
    y4 = [x + width for x in y3]
    y5 = [x + width for x in y4]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.bar(y1, c0, width=width, edgecolor='white', label='CO')
    plt.bar(y2, c02, width=width, edgecolor='white',label='CO2')
    plt.bar(y3, hc, width=width, edgecolor='white', label='HC')
    plt.bar(y4, no, width=width, edgecolor='white', label='NO')
    plt.bar(y5, pm25, width=width, edgecolor='white', label='PM25')

    plt.xlabel('Time')
    plt.xticks([r + width*2 for r in range(len(c0))], datesList)

    plt.title('Particulate concentration by date')
    plt.tight_layout();
    plt.legend()
    chart = get_graph()
    return render(request, 'graph.html', {'chart':chart})


def pm25_graph_line(request, pk):
    city = get_object_or_404(City, pk=pk)
    dates = City.objects.filter(name=city.name).order_by('date')
    x = [x.date for x in dates]
    y = [y.max_pm_25 + y.min_pm_25 for y in dates]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Pm2.5 Concentration for ' + city.name)
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel('PM2.5 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})

def c0_graph_line(request, pk):
    city = get_object_or_404(City, pk=pk)
    dates = City.objects.filter(name=city.name).order_by('date')
    x = [x.date for x in dates]
    y = [y.max_c_co + y.min_c_co for y in dates]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('C0 Concentration for ' + city.name)
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel('C0 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})

def c02_graph_line(request, pk):
    city = get_object_or_404(City, pk=pk)
    dates = City.objects.filter(name=city.name).order_by('date')
    x = [x.date for x in dates]
    y = [y.max_c_co2 + y.min_c_co2 for y in dates]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('C02 Concentration for ' + city.name)
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel('C02 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})

def hc_graph_line(request, pk):
    city = get_object_or_404(City, pk=pk)
    dates = City.objects.filter(name=city.name).order_by('date')
    x = [x.date for x in dates]
    y = [y.max_c_hc + y.min_c_hc for y in dates]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('HC Concentration for ' + city.name)
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel('HC (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})

def no_graph_line(request, pk):
    city = get_object_or_404(City, pk=pk)
    dates = City.objects.filter(name=city.name).order_by('date')
    x = [x.date for x in dates]
    y = [y.max_c_no + y.min_c_no for y in dates]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('NO Concentration for ' + city.name)
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel('NO (ppm)')
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
    plt.title('Pm2.5 Concentration by Wind Direction in ' + city.name)
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
    plt.title('C02 Concentration by Wind Direction in ' + city.name)
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Wind Direction")
    plt.ylabel('C02 (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})


def hc_wind_graph(request, pk):
    city = get_object_or_404(City, pk=pk)
    wind = City.objects.filter(name=city.name).order_by('wind_direction')
    x = [x.wind_direction for x in wind]
    y = [y.max_c_hc + y.min_c_hc for y in wind]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('HC Concentration by Wind Direction in ' + city.name)
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Wind Direction")
    plt.ylabel('HC (ppm)')
    plt.tight_layout();
    chart = get_graph()
    return render(request, 'graph.html', {'chart': chart})


def no_wind_graph(request, pk):
    city = get_object_or_404(City, pk=pk)
    wind = City.objects.filter(name=city.name).order_by('wind_direction')
    x = [x.wind_direction for x in wind]
    y = [y.max_c_no + y.min_c_no for y in wind]
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('NO Concentration by Wind Direction in ' + city.name)
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel("Wind Direction")
    plt.ylabel('NO (ppm)')
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
    plt.title('C0 Concentration by Wind Direction in ' + city.name)
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
    plt.title('Pollution Concentration in ' + city.name)
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

@login_required
def db_upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Successful")
            #redirect('db_upload')
    return HttpResponse("Failed")

def handle_uploaded_file(file, filename):
    for s in file.read().split(','):
        myobject = MyModel(fileData=s)
        myobject.save()



#def box_plot(request, pk):
#    city = get_object_or_404(City, pk=pk)
#    cities = City.objects.filter(name=city.name).order_by('date')
#    x = [x.date for x in cities]
#    y = [y.]
