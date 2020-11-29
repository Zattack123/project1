from django.contrib import admin
from .models import City, Vehicle, PowerPlant #PollutionData

class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "lat", "long", "date", "regmark", "temp", "humidity", "wind_speed", "wind_direction", "speed", "accuracy", "c_co", "c_co2", "c_hc", "c_no", "efco", "efhc", "efno")

class VehicleAdmin(admin.ModelAdmin):
    list_display = ("engine_family", "engine_code", "engine_model", "manufacturer", "part_name", "part_desc", "part_num", "automaker", "trim", "model_year", "sensor")

class PowerPlantAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "so_2", "nox", "co2", "hg", "lat", "long")

admin.site.register(City)
admin.site.register(Vehicle)
admin.site.register(PowerPlant)
#admin.site.register(PollutionData)
# Register your models here.
