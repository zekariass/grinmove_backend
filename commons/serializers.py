from rest_framework.serializers import ModelSerializer
from commons import models as cmn_models

class CountrySerializer(ModelSerializer):
    class Meta:
        model = cmn_models.Country
        fields = "__all__"

class CountryWithReducedFieldSerializer(ModelSerializer):
    class Meta:
        model = cmn_models.Country
        fields = ("id", "name")


class RegionSerializer(ModelSerializer):
    class Meta:
        model = cmn_models.Region
        fields = "__all__"


class CitySerializer(ModelSerializer):
    class Meta:
        model = cmn_models.City
        fields = "__all__"

class AddressShortDepthSerializer(ModelSerializer):
    class Meta:
        model = cmn_models.Address
        fields = "__all__"

class AddressSerializer(ModelSerializer):
    city = CitySerializer()
    region = RegionSerializer()
    country = CountrySerializer()
    class Meta:
        model = cmn_models.Address
        fields = "__all__"


class PeriodicitySerializer(ModelSerializer):
    class Meta:
        model = cmn_models.Periodicity
        fields = "__all__"