from rest_framework import serializers
from properties import models as prop_models
from commons import serializers as cmn_serializers
from agents import serializers as agnt_serializers
from systems import serializers as sys_serializers
from listings import serializers as list_serializers
from django.core.exceptions import ObjectDoesNotExist

#===========HOUSE TYPE=====================================================================
class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.HouseType
        fields = "__all__"
#===========BUILDING TYPE==================================================================
class BuildingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.BuildingType
        fields = "__all__"
#===============================================================================================
class PropSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Property
        fields = "__all__"
#===========APARTMENT UNIT======================================================================
class ApartmentUnitCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.ApartmentUnit
        exclude = ("apartment",)
#===========APARTMENT======================================================================

class ApartmentSerializer(serializers.ModelSerializer):
    # apartment_units = ApartmentUnitCreateBasicSerializer(read_only=True, many=True)
    # property = PropSerializer(read_only=True)

    class Meta:
        model = prop_models.Apartment
        fields = ("id", "cat_key", "floors","is_new","is_multi_unit","property", "agent")

class ApartmentCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Apartment
        exclude = ("property",)

class ApartmentUnitSerializer(serializers.ModelSerializer):
    property = serializers.IntegerField(read_only=True, source="apartment.property.id")
    class Meta:
        model = prop_models.ApartmentUnit
        fields = ("id",
                "cat_key",
                "apartment",
                "number_of_rooms",
                "number_of_bed_rooms",
                "number_of_baths",
                "floor",
                "area",
                "is_furnished",
                "is_available",
                "property")


#===========CONDOMINIUM====================================================================
class CondominiumCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Condominium
        exclude = ("property",)

class CondominiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Condominium
        # exclude = ("agent",)
        fields = ("id",
                "cat_key",
                "property",
                "number_of_rooms",
                "number_of_bed_rooms",
                "floor",
                "number_of_baths",
                "area",
                "is_furnished",
                "is_new",
                "agent")
#===========VILLA==========================================================================
class VillaCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Villa
        exclude = ("property",)

class VillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Villa
        # exclude = ("agent",)
        fields = (
            "id",
            "cat_key",
            "number_of_rooms",
            "number_of_bed_rooms",
            "floor",
            "number_of_baths",
            "total_compound_area",
            "housing_area",
            "is_furnished",
            "is_new",
            "property"
            )
#===========TRADITIONAL HOUSE==============================================================
class TraditionalHouseCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.TraditionalHouse
        exclude = ("property",)

class TraditionalHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.TraditionalHouse
        # exclude = ("agent",)
        fields = ("id",
                "cat_key",
                "number_of_rooms",
                "number_of_bed_rooms",
                "floor",
                "number_of_baths",
                "area",
                "is_furnished",
                "is_new",
                "agent",
                "property")
#===========SHARE HOUSE====================================================================
class ShareHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.ShareHouse
        # exclude = ("agent",)
        fields = ("id",
                "cat_key",
                "property",
                "house_type",
                "total_number_of_rooms",
                "number_of_rooms_to_share",
                "total_number_of_bed_rooms",
                "number_of_bed_rooms_to_share",
                "total_number_of_baths",
                "number_of_baths_to_share",
                "floor",
                "area",
                "is_furnished",
                "is_new",
                "agent")

class ShareHouseCreateBasicSerializer(serializers.ModelSerializer):
    house_type = HouseTypeSerializer(read_only=True)
    class Meta:
        model = prop_models.ShareHouse
        exclude = ("property",)

class ShareHouseCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.ShareHouse
        exclude = ("property",)
#===========COMMERCIAL PROPERTY============================================================
class CommercialPropertyCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.CommercialProperty
        exclude = ("property",)

class CommercialPropertyWithBuildingTypeSerializer(serializers.ModelSerializer):
    building_type = BuildingTypeSerializer(read_only=True)
    class Meta:
        model = prop_models.CommercialProperty
        exclude = ("property",)

class CommercialPropertySerializer(serializers.ModelSerializer):
    # building_type = BuildingTypeSerializer(read_only=True)
    class Meta:
        model = prop_models.CommercialProperty
        # exclude = ("agent",)
        fields = ("id",
                "cat_key",
                "property",
                "building_type",
                "floors",
                "is_new",
                "has_parking_space",
                "is_multi_unit",
                "agent")


class CommercialPropertyUnitSerializer(serializers.ModelSerializer):
    property = serializers.IntegerField(read_only=True, source="commercial_property.property.id")
    class Meta:
        model = prop_models.CommercialPropertyUnit
        fields = ("id",
                "cat_key",
                "commercial_property",
                "number_of_rooms",
                "area",
                "floor",
                "com_prop_unit_description",
                "property")

class CommercialPropertyUnitCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.CommercialPropertyUnit
        exclude = ("commercial_property",)
#===========LAND===========================================================================
class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Land
        # exclude = ("agent",)
        fields = ("id",
                "cat_key",
                "property",
                "area",
                "length",
                "width",
                "has_plan",
                "has_debt",
                "agent")

class LandCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Land
        exclude = ("property",)
#===========ALL PURPOSE PROPERTY===========================================================
class AllPurposePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.AllPurposeProperty
        # exclude = ("agent",)
        fields = ("id",
                "cat_key",
                "property",
                "building_type",
                "floors",
                "best_for",
                "all_purpose_property_description",
                "has_parking_space",
                "is_multi_unit",
                "agent")

class AllPurposePropertyWithBuildingTypeSerializer(serializers.ModelSerializer):
    building_type = BuildingTypeSerializer(read_only=True)
    class Meta:
        model = prop_models.AllPurposeProperty
        exclude = ("property",)

class AllPurposePropertyCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.AllPurposeProperty
        exclude = ("property",)

class AllPurposePropertyUnitSerializer(serializers.ModelSerializer):
    property = serializers.IntegerField(read_only=True, source="all_purpose_property.property.id")
    class Meta:
        model = prop_models.AllPurposePropertyUnit
        fields = ("id",
                "cat_key",
                "all_purpose_property",
                "floor",
                "number_of_rooms",
                "area",
                "all_purpose_property_unit_description",
                "property")

class AllPurposePropertyUnitCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.AllPurposePropertyUnit
        exclude = ("all_purpose_property",)
#===========HALL===========================================================================
class HallCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Hall
        exclude = ("property",)

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Hall
        # exclude = ("agent",)
        fields = ("id",
                "cat_key",
                "property",
                "floor",
                "number_of_seats",
                "total_capacity",
                "has_parking_space",
                "number_of_parking_spaces",
                "hall_description",
                "agent")
#===========OFFICE=========================================================================
class OfficeCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Office
        exclude = ("property",)

class OfficeWithBuildingTypeSerializer(serializers.ModelSerializer):
    building_type = BuildingTypeSerializer(read_only=True)
    class Meta:
        model = prop_models.Office
        exclude = ("property",)

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.Office
        # exclude = ("agent",)
        fields = ("id",
                "cat_key",
                "building_type",
                "floor",
                "number_of_rooms",
                "area",
                "is_furnished",
                "is_new",
                "has_parking_space",
                "agent",
                "property")
#===========EDUCATION FACILITY LEVEL=============================================================
class EdufaLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.EdufaLevel
        fields = "__all__"
#===========EDUCATION FACILITY=============================================================
class EducationFacilitySerializer(serializers.ModelSerializer):
    edufa_level = EdufaLevelSerializer()
    near_by_properties = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = prop_models.EducationFacility
        fields = "__all__"
        # fields = ("id","edufa_level","name","ownership","distance_from_property","distance_unit","description","added_on", "property")

class EducationFacilityBasicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.EducationFacility
        fields = "__all__"
#===========TRANSPORT FACILITY========================================================
class TransFaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.TransFaCategory
        fields = "__all__"

class TransportFacilitySerializer(serializers.ModelSerializer):
    trans_fa_category = TransFaCategorySerializer()
    near_by_properties = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = prop_models.TransportFacility
        fields = "__all__"

class TransportFacilityBasicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.TransportFacility
        fields = "__all__"
#===========POINT OF INTEREST =====================================================
class POICategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.POICategory
        fields = "__all__"

class PointOfInterestSerializer(serializers.ModelSerializer):
    poi_category = POICategorySerializer()
    near_by_properties = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = prop_models.PointOfInterest
        fields = "__all__"

class POIBasicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PointOfInterest
        fields = "__all__"

#=========================================================================================
class AmenityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.AmenityCategory
        fields = "__all__"

class AmenitySerializer(serializers.ModelSerializer):
    category = AmenityCategorySerializer()
    class Meta:
        model = prop_models.Amenity
        fields = "__all__"

#===========Rule===========================================================================
class RuleSerializer(serializers.ModelSerializer):
    # property = PropertyCreateBasicSerializer()
    class Meta:
        model = prop_models.Rule
        exclude = ("property",)

#===========LISTING DISCOUNT BY CATEGORY==================================================================
class ListingDiscountByCategorySerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()
    listing_param = sys_serializers.ListingParameterSerializer(read_only=True)
    class Meta:
        model = prop_models.ListingDiscountByCategory
        fields = "__all__"

#===========LISTING PRICE BY CATEGORY==================================================================
class ListingPriceByCategorySerializer(serializers.ModelSerializer):
    currency = sys_serializers.CurrencySerializer(read_only=True)
    listing_type = list_serializers.ListingTypeSerializer(read_only=True)
    class Meta:
        model = prop_models.ListingPriceByCategory
        fields = "__all__"

#===========PROPERTY=======================================================================
# class PropertyFileLabelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = prop_models.PropertyFileLabel
#         fields = "__all__"

class PropertyImageSerializer(serializers.ModelSerializer):
    label_name = serializers.CharField(source="label", read_only=True)
    class Meta:
        model = prop_models.PropertyImage
        # exclude = ("property",)
        fields = (
            "id",
            # "property",
            "image",
            "label",
            "uploaded_on",
            "label_name"
            )

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyVideo
        exclude = ("property",)

class PropertyVirtualTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyVirtualTour
        exclude = ("property",)

class PropertyCategorySerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(read_only=True, many=True)
    # category_discount = ListingDiscountByCategorySerializer(read_only=True, many=True)
    # listing_price = ListingPriceByCategorySerializer(read_only=True, many=True)
    class Meta:
        model = prop_models.PropertyCategory
        fields = "__all__"

class PropertyCategorySlugSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(read_only=True, many=True)
    class Meta:
        model = prop_models.PropertyCategory
        fields = "__all__"
        lookup_field = "cat_key"


# class PropertyCategoryWithPriceAndDiscountInfoSlugSerializer(serializers.ModelSerializer):
#     # amenities = AmenitySerializer(read_only=True, many=True)
#     class Meta:
#         model = prop_models.PropertyCategory
#         fields = "__all__"
#         lookup_field = "cat_key"


class PropertyCreateBasicSerializer(serializers.ModelSerializer):
    images_count = serializers.SerializerMethodField(read_only=True)
    videos_count = serializers.SerializerMethodField(read_only=True)
    virtual_tours_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = prop_models.Property
        fields = ["id","is_residential","description", "added_on","images_count", "videos_count","virtual_tours_count"]
        extra_kwargs = {'added_on': {'read_only': True}, "id":{"read_only":True}}

    def get_images_count(self, property):
        return property.images.count()

    def get_videos_count(self, instance):
        return instance.videos.count()

    def get_virtual_tours_count(self, instance):
        return instance.virtual_tours.count()

class PropertySerializer(serializers.ModelSerializer):
    property_category = PropertyCategorySerializer()
    address = cmn_serializers.AddressSerializer(read_only=True)
    # agent = agnt_serializers.AgentSerializer(read_only=True)
    agent = agnt_serializers.AgentFullDataSerializer(read_only=True)
    education_facility = EducationFacilitySerializer(many=True,read_only=True)
    transport_facility = TransportFacilitySerializer(many=True,read_only=True)
    point_of_interest = PointOfInterestSerializer(many=True,read_only=True)
    amenity = AmenitySerializer(many=True,read_only=True)
    rules = RuleSerializer(read_only=True, many=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    images_count = serializers.SerializerMethodField(read_only=True)
    videos = PropertyVideoSerializer(many=True, read_only=True)
    videos_count = serializers.SerializerMethodField(read_only=True)
    virtual_tours = PropertyVirtualTourSerializer(many=True, read_only=True)
    virtual_tours_count = serializers.SerializerMethodField(read_only=True)
    # villa = VillaSerializer(read_only=True)
    related_property = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = prop_models.Property
        fields = ["id","property_category","agent","address","is_residential","description", "agent",\
            "added_on","education_facility","transport_facility","point_of_interest","amenity", "rules",\
            "images","videos","virtual_tours", "images_count","videos_count","virtual_tours_count", "related_property"]
            # "villa","apartment","condominium","traditional_house","share_house","commercial_property",\
            # "all_purpose_property","office","hall","land"]

        extra_kwargs = {'added_on': {'read_only': True}}

    def get_images_count(self, instance):
        return instance.images.count()
    
    def get_videos_count(self, instance):
        return instance.videos.count()

    def get_virtual_tours_count(self, instance):
        return instance.virtual_tours.count()

    def get_related_property(self, instance):
        if hasattr(instance, "villa"):
            return VillaCreateBasicSerializer(instance=prop_models.Villa.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "apartment"):
            return ApartmentCreateBasicSerializer(instance=prop_models.Apartment.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "condominium"):
            return CondominiumCreateBasicSerializer(instance=prop_models.Condominium.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "traditional_house"):
            return TraditionalHouseCreateBasicSerializer(instance=prop_models.TraditionalHouse.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "share_house"):
            return ShareHouseCreateBasicSerializer(instance=prop_models.ShareHouse.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "commercial_property"):
            return CommercialPropertyWithBuildingTypeSerializer(instance=prop_models.CommercialProperty.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "all_purpose_property"):
            return AllPurposePropertyWithBuildingTypeSerializer(instance=prop_models.AllPurposeProperty.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "office"):
            return OfficeWithBuildingTypeSerializer(instance=prop_models.Office.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "hall"):
            return HallCreateBasicSerializer(instance=prop_models.Hall.objects.get(property=instance.id),read_only=True).data
        elif hasattr(instance, "land"):
            return LandCreateBasicSerializer(instance=prop_models.Land.objects.get(property=instance.id),read_only=True).data
        else: return None

class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyVideo
        exclude = ("property",)

class PropertyFileLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = prop_models.PropertyFileLabel
        fields = "__all__"


