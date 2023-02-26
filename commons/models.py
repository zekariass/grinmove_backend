from django.conf import settings
from django.db import models
from django.utils import timezone

"""Country models for countries used in the system"""
class Country(models.Model):
    name = models.CharField(verbose_name='country name', max_length=50, unique=True, blank=False, null=False)
    code = models.CharField(verbose_name='country code', max_length=10, blank=True)
    latitute = models.CharField(verbose_name='geo latitude', max_length=20, null=True, blank=True)
    longitude = models.CharField(verbose_name='geo logitude', max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

"""Regions that a country have and used for sytem convenience"""
class Region(models.Model):
    name = models.CharField(verbose_name='region name', max_length=50, blank=False, null=False)
    country = models.ForeignKey(Country, related_name='regions', on_delete=models.CASCADE, verbose_name='country of region')
    code = models.CharField(verbose_name='region code', max_length=10, blank=True)
    latitute = models.CharField(verbose_name='geo logitude', max_length=20, null=True, blank=True)
    longitude = models.CharField(verbose_name='geo logitude', max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

"""Cities in a region"""
class City(models.Model):
    name = models.CharField(verbose_name='city name', max_length=50)
    country = models.ForeignKey(Country, related_name='country_cities', verbose_name='country of city', on_delete=models.CASCADE)
    region = models.ForeignKey(Region, related_name='region_cities', verbose_name='region of city', on_delete=models.CASCADE)
    code = models.CharField(verbose_name='city code', max_length=10, blank=True)
    latitute = models.CharField(verbose_name='geo latitued', max_length=20, null=True, blank=True)
    longitude = models.CharField(verbose_name='geo longitude', max_length=20, null=True, blank=True)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name


"""Address of a property or an agent"""
class Address(models.Model):
    country = models.ForeignKey(Country, blank=False, null=False, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, blank=False, null=False, on_delete=models.CASCADE)
    city = models.ForeignKey(City, blank=False, null=False, on_delete=models.CASCADE)
    street = models.CharField(verbose_name='street name', max_length=100, blank=False, null=False)
    post_code = models.CharField(max_length=20, blank=True, null=True)
    building_name_or_number = models.CharField(verbose_name='building name or number', max_length=50, blank=True, null=True)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.CharField(verbose_name='geo latitude', max_length=20, null=True, blank=True)
    longitude = models.CharField(verbose_name='geo longitude', max_length=20, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.street, self. post_code)

"""Periodicity is used to set a period for a specific purpose, such as daily, weekly, monthly, and annual subscriptions"""
class Periodicity(models.Model):
    period = models.CharField(verbose_name="period label or name", max_length=30, unique=True)
    num_of_days = models.IntegerField(verbose_name="number of days in this period", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.period