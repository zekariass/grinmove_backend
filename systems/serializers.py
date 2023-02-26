from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from systems import models as sys_models

class SystemParameterSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemParameter
        fields = "__all__"


class SystemParameterSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemParameter
        fields = "__all__"


class ListingParameterSerializer(ModelSerializer):
    class Meta:
        model = sys_models.ListingParameter
        fields = "__all__"

class CurrencySerializer(ModelSerializer):
    class Meta:
        model = sys_models.Currency
        fields = "__all__"

class SystemAssetOwnerSerializer(ModelSerializer):
    class Meta:
        model = sys_models.SystemAssetOwner
        fields = "__all__"

class SystemAssetSerializer(ModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field="name")
    class Meta:
        model = sys_models.SystemAsset
        fields = "__all__"