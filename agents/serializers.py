from calendar import c
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse
from agents import models as agnt_models
from commons import serializers as cmn_serializers

class AgentLogoSerializer(ModelSerializer):
    class Meta:
        model = agnt_models.AgentLogo
        fields = "__all__"

    # def create(self, validated_data):


class AgentSerializer(ModelSerializer):
    class Meta:
        model = agnt_models.Agent
        fields = "__all__"


class AgentFullDataSerializer(ModelSerializer):
    # logo_url = serializers.SerializerMethodField()
    logo = AgentLogoSerializer()
    address = cmn_serializers.AddressSerializer(read_only=True)
    class Meta:
        model = agnt_models.Agent
        fields = "__all__"
        # depth = 1
