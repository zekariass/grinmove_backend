from rest_framework import serializers
from listings import models as list_models
from commons import serializers as cmn_serializers
from agents import serializers as agent_serializers
from myhome import strings
# import properties.serializers as ser

class ListingModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.ListingMode
        fields = "__all__"

class ListingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.ListingType
        fields = "__all__"

class ListingStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.ListingState
        fields = "__all__"

#==========MAIN LISTING=========================================
class MainListingSerializer(serializers.ModelSerializer):
    address = cmn_serializers.AddressSerializer(read_only=True)
    class Meta:
        model = list_models.MainListing
        fields ="__all__"

class MainListingPublicSerializer(serializers.ModelSerializer):
    address = cmn_serializers.AddressSerializer(read_only=True)
    number_of_baths = serializers.SerializerMethodField()
    number_of_bed_rooms = serializers.SerializerMethodField()
    property_images = serializers.SerializerMethodField()
    agent = agent_serializers.AgentSerializer(read_only=True)
    is_saved = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = list_models.MainListing
        fields = ("id",
            "listing_state",
            "listing_mode",
            "property_price",
            "deposit_in_months",
            "is_approved",
            "is_expired",
            "listed_on",
            "property",
            "property_category",
            "payment",
            "listing_type",
            "listing_currency",
            "listing_term",
            "description",
            "agent",
            "address",
            "property_images",
            "number_of_baths",
            "number_of_bed_rooms",
            "is_saved",
            )
    
    # def get_property(self, obj):
    #     from properties.serializers import PropertySerializer
    #     from properties.models import Property
    #     property_instance = Property.objects.get(pk=obj.property.id)
    #     property =  PropertySerializer(property_instance)
    #     return property.data
    def get_property_images(self, obj):
        from properties.serializers import PropertyImageSerializer
        from properties.models import PropertyImage
        image_instances = PropertyImage.objects.filter(property=obj.property.id)
        images =  PropertyImageSerializer(image_instances, many=True, context=self.context)
        return images.data
    
    def get_number_of_baths(self, obj):
        cat_key = obj.property.property_category.cat_key
        if cat_key==strings.VILLA_KEY:
            return obj.property.villa.number_of_baths
        elif cat_key==strings.CONDOMINIUM_KEY:
            return obj.property.condominium.number_of_baths
        elif cat_key==strings.SHARE_HOUSE_KEY:
            return obj.property.share_house.total_number_of_baths
        elif cat_key==strings.APARTMENT_KEY:
            apartment = obj.property.apartment
            # return apartment.apartment_units.number_of_baths
            print("YOOOOOOOO: ",apartment.apartment_units)
            return None
        else:
            return None

    def get_number_of_bed_rooms(self, obj):
        cat_key = obj.property.property_category.cat_key
        if cat_key==strings.VILLA_KEY:
            return obj.property.villa.number_of_bed_rooms
        elif cat_key==strings.CONDOMINIUM_KEY:
            return obj.property.condominium.number_of_bed_rooms
        elif cat_key==strings.SHARE_HOUSE_KEY:
            return obj.property.share_house.total_number_of_bed_rooms
        # elif cat_key==strings.APARTMENT_KEY:
        #     return obj.property.apartment.apartment_units.number_of_bed_rooms
        else:
            return None

    def get_is_saved(self, obj):
        user = self.context.get("request").user
        if list_models.SavedListing.objects.filter(user=user.id, main_listing=obj.id).exists():
            return True
        else:
            return False
    

class MainListingBasicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.MainListing
        exclude = ("property","agent",)
#================================================================

class ApartmentUnitListingSerializer(serializers.ModelSerializer):
    main_listing = MainListingSerializer(read_only=True)
    class Meta:
        model = list_models.ApartmentUnitListing
        fields = "__all__"

class ApartmentUnitListingBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.ApartmentUnitListing
        fields = "__all__"

class CommercialPropertyUnitListingSerializer(serializers.ModelSerializer):
    main_listing = MainListingSerializer(read_only=True)
    class Meta:
        model = list_models.CommercialPropertyUnitListing
        fields = "__all__"

class CommercialPropertyUnitListingBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.CommercialPropertyUnitListing
        fields = "__all__"


class VillaListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.VillaListing
        fields = "__all__"

class ShareHouseListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.ShareHouseListing
        fields = "__all__"

class AllPurposePropertyListingSerializer(serializers.ModelSerializer):
    main_listing = MainListingSerializer(read_only=True)
    class Meta:
        model = list_models.AllPurposePropertyUnitListing
        fields = "__all__"

class AllPurposePropertyListingBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = list_models.AllPurposePropertyUnitListing
        fields = "__all__"


class PublicListingDtailSerializer(serializers.ModelSerializer):
    # address = cmn_serializers.AddressSerializer(read_only=True)
    # number_of_baths = serializers.SerializerMethodField()
    # number_of_bed_rooms = serializers.SerializerMethodField()
    property = serializers.SerializerMethodField()
    # agent = agent_serializers.AgentSerializer(read_only=True)
    unit_listing = serializers.SerializerMethodField(read_only=True)
    is_saved = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = list_models.MainListing
        fields = ("id",
            "listing_state",
            "listing_mode",
            "property_price",
            "deposit_in_months",
            "is_approved",
            "is_expired",
            "listed_on",
            "property",
            "property_category",
            "payment",
            "listing_type",
            "listing_currency",
            "listing_term",
            "description",
            "unit_listing",
            "is_saved",
            # "agent",
            # "address",
            # "property_images",
            # "number_of_baths",
            # "number_of_bed_rooms",
            )

    def get_property(self, obj):
        from properties.serializers import PropertySerializer
        from properties.models import Property
        property_instance = Property.objects.get(pk=obj.property.id)
        property_detail =  PropertySerializer(property_instance, context=self.context)
        return property_detail.data
    
    def get_unit_listing(self, obj):
        if hasattr(obj, "all_purpose_property_unit_listing"):
            return AllPurposePropertyListingBasicSerializer(instance=list_models.AllPurposePropertyUnitListing.objects.get(main_listing=obj.id),read_only=True).data
        if hasattr(obj, "commercial_property_unit_listing"):
            return CommercialPropertyUnitListingBasicSerializer(instance=list_models.CommercialPropertyUnitListing.objects.get(main_listing=obj.id),read_only=True).data
        if hasattr(obj, "apartment_unit_listing"):
            return ApartmentUnitListingBasicSerializer(instance=list_models.ApartmentUnitListing.objects.get(main_listing=obj.id),read_only=True).data
        return None

    def get_is_saved(self, obj):
        user = self.context.get("request").user
        if list_models.SavedListing.objects.filter(user=user.id, main_listing=obj.id).exists():
            return True
        else:
            return False

class SavedListingSerialier(serializers.ModelSerializer):
    class Meta:
        model = list_models.SavedListing
        fields = ("main_listing",)

class SavedListingListSerialier(serializers.ModelSerializer):
    main_listing = MainListingPublicSerializer(read_only=True)
    class Meta:
        model = list_models.SavedListing
        exclude = ("user",)

class FeaturePriceSerialier(serializers.ModelSerializer):
    class Meta:
        model = list_models.FeaturePrice
        fields = "__all__"


class FeaturedListingSerialier(serializers.ModelSerializer):
    class Meta:
        model = list_models.FeaturedListing
        fields = ("main_listing",)

class FeaturedListingWithMainListingDetailSerialier(serializers.ModelSerializer):
    main_listing = MainListingPublicSerializer(read_only=True)
    class Meta:
        model = list_models.FeaturedListing
        fields = ("main_listing","featured_on",)