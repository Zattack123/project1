from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=30, default="")
    state = models.CharField(max_length=30, default="")
    lat = models.CharField(max_length=30, default="")
    long = models.CharField(max_length=30, default="")
    date = models.CharField(max_length=30, default="")
    regmark = models.CharField(max_length=30, default="")
    temp = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    humidity = models.DecimalField(max_digits = 7, decimal_places=4, default=0.0)
    wind_speed = models.DecimalField(max_digits = 7, decimal_places=4, default=0.0)
    wind_direction = models.CharField(max_length=30, default="")
    speed = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    accuracy = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    max_c_co = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    min_c_co = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    max_c_co2 = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    min_c_co2 = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    max_c_hc = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    min_c_hc = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    max_c_no = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    min_c_no = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    max_pm_25 = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    min_pm_25 = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    efco = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    efhc = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)
    efno = models.DecimalField(max_digits = 7, decimal_places=2, default=0.0)



    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    engine_family = models.CharField(max_length=30)
    engine_code = models.CharField(max_length=30)
    engine_model = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=30)
    part_name = models.CharField(max_length=30)
    part_desc = models.CharField(max_length=100)
    part_num = models.CharField(max_length=30)
    automaker = models.CharField(max_length=30)
    trim = models.CharField(max_length=30)
    model_year = models.CharField(max_length=10)
    sensor = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "vehicles"

    def __str__(self):
        return self.model_year + " " + self.automaker + " " + self.trim


class PowerPlant(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=10)
    so_2 = models.DecimalField(max_digits=10, decimal_places=5)
    nox = models.DecimalField(max_digits=10, decimal_places=5)
    co2 = models.DecimalField(max_digits=10, decimal_places=5)
    hg = models.DecimalField(max_digits=10, decimal_places=5)
    lat = models.CharField(max_length=30)
    long = models.CharField(max_length=30)


    class Meta:
        verbose_name_plural = "powerplants"

    def __str__(self):
        return self.name
