from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from django.db.models import Q

import matplotlib.plyplot as plt
import io
import urllib, base64

from .models import City, Vehicle, PowerPlant

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


#def graphtest(request):
#    plt.plot(range(10))
#    fig = plt.gcf()
#    buf = io.BytesIO()
#    fig.savefig(buf,format='png')
#    buf.seek(0)
#    string = base64.b64encode(buf.read())
#    uri = urllib.parse.quote(string)
#    return render(request,'graph.html',{'data':uri})

# Create your views here.
