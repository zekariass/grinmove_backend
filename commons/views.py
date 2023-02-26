from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from commons import serializers
from commons import models as cmn_models

class RetrieveCountry(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):

        country_queryset = cmn_models.Country.objects.all()
        country_serializer = serializers.CountrySerializer(country_queryset, many=True)

        return Response(country_serializer.data)


class ListCountry(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        country_queryset = cmn_models.Country.objects.all()
        country_serializer = serializers.CountryWithReducedFieldSerializer(country_queryset, many=True)

        return Response(country_serializer.data)


class RetrieveRegion(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        region_queryset = cmn_models.Region.objects.all()
        region_serializer = serializers.RegionSerializer(region_queryset, many=True)

        return Response(region_serializer.data)


class ListRegionByCountry(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        countryId = int(request.query_params.get("countryId"))
        countryObj = cmn_models.Country.objects.get(pk=countryId)
        if countryObj is not None:
            region_queryset = cmn_models.Region.objects.filter(country=countryObj)
            if region_queryset.exists():
                region_serializer = serializers.RegionSerializer(region_queryset, many=True)
                return Response(region_serializer.data)
            else:
                return Response(data="Region does not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data="Country does not found", status=status.HTTP_404_NOT_FOUND)

class ListRegionByCountryName(generics.ListAPIView):
    queryset = cmn_models.Region.objects.all()
    serializer_class = serializers.RegionSerializer

    def get_queryset(self):
        country_name = self.request.query_params.get("country")
        try:
            country = cmn_models.Country.objects.get(name=country_name)
            regions = cmn_models.Region.objects.filter(country=country.id)
            return regions
        except ObjectDoesNotExist:
            return None #Response(data="Country is not found!", status=status.HTTP_404_NOT_FOUND)

class ListCityByRegion(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        countryId = int(request.query_params.get("regionId"))
        regionObj = cmn_models.Region.objects.get(pk=countryId)
        if regionObj is not None:
            city_queryset = cmn_models.City.objects.filter(region=regionObj)
            if city_queryset.exists():
                city_serializer = serializers.CitySerializer(city_queryset, many=True)
                return Response(city_serializer.data)
            else:
                return Response(data="City does not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data="Region does not found", status=status.HTTP_404_NOT_FOUND)


class RetrieveCity(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        city_queryset = cmn_models.City.objects.all()
        city_serializer = serializers.CitySerializer(city_queryset, many=True)

        return Response(city_serializer.data)


class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = cmn_models.Address.objects.all()
    serializer_class = serializers.AddressShortDepthSerializer
    permission_classes = [AllowAny,]


class PeriodicityListView(generics.ListAPIView):
    queryset = cmn_models.Periodicity.objects.all()
    serializer_class = serializers.PeriodicitySerializer
    permission_classes = [AllowAny,]


class PopularCityListView(generics.ListAPIView):
    queryset = cmn_models.City.objects.all()
    serializer_class = serializers.CitySerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        popular_cities = cmn_models.City.objects.filter(is_popular=True)
        return popular_cities