from rest_framework import serializers
from properties import serializers as prop_serializers
from properties import models

class PropertyChildSerializer(serializers.RelatedField):
    def to_representation(self, value):
        related = models.Property.select_related("villa")
        if isinstance(related, models.Apartment):
            serializer  = prop_serializers.ApartmentSerializer(related)
        elif isinstance(related, models.Villa):
            serializer  = prop_serializers.VillaCreateBasicSerializer(related)

        return serializer.data