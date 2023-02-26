from django.shortcuts import render

from rest_framework import generics
from systems import serializers as sys_serializers
from systems import models as sys_models
from rest_framework.permissions import AllowAny

class SystemParameterListView(generics.ListAPIView):
    queryset = sys_models.SystemParameter.objects.all()
    serializer_class = sys_serializers.SystemParameterSerializer
    permission_classes = [AllowAny,]


class ListingParameterListView(generics.ListAPIView):
    queryset = sys_models.ListingParameter.objects.all()
    serializer_class = sys_serializers.ListingParameterSerializer
    permission_classes = [AllowAny,]


class CurrencyListView(generics.ListAPIView):
    queryset = sys_models.Currency.objects.all()
    serializer_class = sys_serializers.CurrencySerializer
    permission_classes = [AllowAny,]

class SystemAssetListCreateView(generics.ListCreateAPIView):
    queryset = sys_models.SystemAsset.objects.all()
    serializer_class = sys_serializers.SystemAssetSerializer
    permission_classes = [AllowAny,]