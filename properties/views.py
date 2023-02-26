from rest_framework import generics
from properties import serializers as prop_serializers
from properties import models as prop_models
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import filters

from commons import models as cmn_models
from commons import serializers as cmn_serializers

from agents import models as agnt_models
from agents import serializers as agnt_serializers

class PropertyCategoryListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.PropertyCategorySerializer
    permission_classes = [AllowAny,]

class PropertyCategorySlugRetrieveView(generics.RetrieveAPIView):
    queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.PropertyCategorySerializer
    lookup_field = "cat_key"
    # permission_classes = [IsAuthenticated,]

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.PropertySerializer
    permission_classes = [IsAuthenticated,]
    # ordering_fields = ['description']

    def post(self, request, format=None):
        print(request.data)
        property_address = request.data.pop("address")
        unresolved_sub_property_data = request.data.pop("category")

        property_address_serializer = cmn_serializers.AddressShortDepthSerializer(data=property_address)

        if property_address_serializer.is_valid():
            property_address_instance = property_address_serializer.save()

            if property_address_instance is not None:
                try:
                    property_category_id = request.data.pop("property_category")
                    property_category_instance = prop_models.PropertyCategory.objects.get(pk=property_category_id)
                
                except ObjectDoesNotExist:
                    print("Property category is not found!")
                    return Response(data="Property category is not found!", status=status.HTTP_404_NOT_FOUND)
                
                try:
                    agent_id = request.data.pop("agent")
                    agent_instance = agnt_models.Agent.objects.get(pk=agent_id)

                except ObjectDoesNotExist:
                    print("Agent is not found!")
                    return Response(data="Agent is not found!", status=status.HTTP_404_NOT_FOUND)

                prop_cat_key = property_category_instance.cat_key

                # apartment = condominium = traditional_house = villa = commercial_property = hall = office = \
                # land = share_house = all_purpose_property = None

                units = units_serializer = resolved_sub_property_serializer = None


                if prop_cat_key == "CAT001":
                    apartment = unresolved_sub_property_data.pop("apartment")
                    units = apartment.pop("units")
                    resolved_sub_property_serializer = prop_serializers.ApartmentCreateBasicSerializer(data=apartment)
                    units_serializer = prop_serializers.ApartmentUnitCreateBasicSerializer(data=units, many=True)
                elif prop_cat_key == "CAT002":
                    condominium = unresolved_sub_property_data.pop("condominium")
                    resolved_sub_property_serializer = prop_serializers.CondominiumCreateBasicSerializer(data=condominium)
                elif prop_cat_key == "CAT003":
                    traditional_house = unresolved_sub_property_data.pop("traditional_house")
                    resolved_sub_property_serializer = prop_serializers.TraditionalHouseCreateBasicSerializer(data=traditional_house)
                elif prop_cat_key == "CAT004":
                    villa = unresolved_sub_property_data.pop("villa")
                    resolved_sub_property_serializer = prop_serializers.VillaCreateBasicSerializer(data=villa)
                elif prop_cat_key == "CAT005":
                    share_house = unresolved_sub_property_data.pop("share_house")
                    resolved_sub_property_serializer = prop_serializers.ShareHouseCreateBasicSerializer(data=share_house)
                elif prop_cat_key == "CAT006":
                    commercial_property = unresolved_sub_property_data.pop("commercial_property")
                    units = commercial_property.pop("units")
                    resolved_sub_property_serializer = prop_serializers.CommercialPropertyCreateBasicSerializer(data=commercial_property)
                    units_serializer = prop_serializers.CommercialPropertyUnitCreateBasicSerializer(data=units, many=True)
                elif prop_cat_key == "CAT007":
                    office = unresolved_sub_property_data.pop("office")
                    resolved_sub_property_serializer = prop_serializers.OfficeCreateBasicSerializer(data=office)
                elif prop_cat_key == "CAT008":
                    hall = unresolved_sub_property_data.pop("hall")
                    resolved_sub_property_serializer = prop_serializers.HallCreateBasicSerializer(data=hall)
                elif prop_cat_key == "CAT009":
                    land = unresolved_sub_property_data.pop("land")
                    resolved_sub_property_serializer = prop_serializers.LandCreateBasicSerializer(data=land)
                elif prop_cat_key == "CAT010":
                    all_purpose_property = unresolved_sub_property_data.pop("all_purpose_property")
                    units = all_purpose_property.pop("units")
                    resolved_sub_property_serializer = prop_serializers.AllPurposePropertyCreateBasicSerializer(data=all_purpose_property)
                    units_serializer = prop_serializers.AllPurposePropertyUnitCreateBasicSerializer(data=units, many=True)

                parent_property_serializer = prop_serializers.PropertyCreateBasicSerializer(data=request.data)

                if parent_property_serializer.is_valid():
                    # print("HEYYYY! PROP IS VALID!")
                    property_instance = parent_property_serializer.save(agent=agent_instance, address=property_address_instance, property_category=property_category_instance)
                    # print("HEYYYY! PROP IS STILL VALID!")

                    if resolved_sub_property_serializer is not None:
                        # print("apartment_units: ", apartment)
                        # apartment_units = apartment.pop("units")

                        # apartment_serializer = prop_serializers.ApartmentCreatBasicSerializer(data=apartment)

                        if resolved_sub_property_serializer.is_valid():
                            # print("HEYYYY! APARTMENT IS VALID!")
                            sub_property_instance = resolved_sub_property_serializer.save(property=property_instance)
                            
                            print("apartment_units: ", units)

                            if units_serializer is not None:
                                
                                # units_serializer = prop_serializers.ApartmentUnitCreateBasicSerializer(data=apartment_units, many=True)
                                if units_serializer.is_valid():
                                    print("AFTER UNIT SERIALIZER IS VALID")
                                    if prop_cat_key == "CAT001":
                                        units_serializer.save(apartment=sub_property_instance)
                                    elif prop_cat_key == "CAT006":
                                        units_serializer.save(commercial_property=sub_property_instance)
                                    elif prop_cat_key == "CAT010":
                                        units_serializer.save(all_purpose_property=sub_property_instance)

                                    return Response(data=parent_property_serializer.data, status=status.HTTP_201_CREATED)
                                else:
                                    print("UNIT: ", units_serializer.data)
                                    print("Bad property unit data!")
                                    return Response(data="Bad property unit data!", status=status.HTTP_400_BAD_REQUEST)  
                            return Response(data=parent_property_serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            print("Bad sub-property data!")
                            return Response(data="Bad sub-property data!", status=status.HTTP_400_BAD_REQUEST)
                else: 
                    print("Bad property data!")
                    return Response(data="Bad property data!", status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Something wrong when saving Address!")
                return Response(data="Something wrong when saving Address!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Bad property address data!")
            return Response(data="Bad address data!", status=status.HTTP_400_BAD_REQUEST)


class PropertyListByAgentView(generics.ListAPIView):
    # queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.PropertySerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
        except ObjectDoesNotExist:
            return None
        
        properties = prop_models.Property.objects.filter(agent=currentAgentAdmin.agent)
        return properties

class PropertyRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = prop_models.Property.objects.all()
    serializer_class = prop_serializers.PropertySerializer
    permission_classes = [IsAuthenticated,]

class PropertyUpdateAPIView(generics.UpdateAPIView):
    queryset = prop_models.Property.objects.all()
    serializer_class = prop_serializers.PropertyCreateBasicSerializer
    permission_classes = [IsAuthenticated,]

#=============== LAND =============================================================

class LandListByAgentView(generics.ListAPIView):
    serializer_class = prop_serializers.LandSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
        except ObjectDoesNotExist:
            return None
        
        lands = prop_models.Land.objects.filter(agent=currentAgentAdmin.agent.id)

        return lands


class LandRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Land.objects.all()
    serializer_class = prop_serializers.LandSerializer
    permission_classes = [IsAuthenticated,]

#=============== SHARE HOUSE=======================================================
class ShareHouseListByAgentView(generics.ListAPIView):
    serializer_class = prop_serializers.ShareHouseSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
        except ObjectDoesNotExist:
            return None
        
        share_house = prop_models.ShareHouse.objects.filter(agent=currentAgentAdmin.agent.id)

        return share_house


class ShareHouseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.ShareHouse.objects.all()
    serializer_class = prop_serializers.ShareHouseSerializer
    permission_classes = [IsAuthenticated,]

#============= APARTMENT =======================================================
class ApartmentListByAgentView(generics.ListAPIView):
    # queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.ApartmentSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
            # print(currentAgentAdmin.agent.id)
        except ObjectDoesNotExist:
            return None
        
        apartments = prop_models.Apartment.objects.filter(agent=currentAgentAdmin.agent.id)

        return apartments

class ApartmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Apartment.objects.all()
    serializer_class = prop_serializers.ApartmentSerializer
    permission_classes = [IsAuthenticated,]


class ApartmentUnitByApartmentView(generics.ListAPIView):
    queryset = prop_models.ApartmentUnit.objects.all()
    serializer_class = prop_serializers.ApartmentUnitSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, **kwargs):
        apartmentId = request.query_params.get("apartment")

        apartment_units = prop_models.ApartmentUnit.objects.filter(apartment=apartmentId)

        if apartment_units.exists():
            apartment_unit_serializer = self.get_serializer(apartment_units, many=True)
        
        else:
            return Response(data="Apartment unit does not exist for this apartment!", status=status.HTTP_404_NOT_FOUND)

        return Response(data=apartment_unit_serializer.data, status=status.HTTP_200_OK)


class ApartmentUnitCreateView(generics.CreateAPIView):
    queryset = prop_models.ApartmentUnit.objects.all()
    serializer_class = prop_serializers.ApartmentUnitCreateBasicSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, **kwargs):

        apartment_id = request.data.get("apartment")
        apartment_unit = request.data.get("unit")

        try:
            apartment_instance = prop_models.Apartment.objects.get(pk=apartment_id)

        except ObjectDoesNotExist:
            print(f"Apartment {apartment_id} is not found!")
            return Response(data=f"Apartment {apartment_id} is not found!", status=status.HTTP_404_NOT_FOUND)

        apartment_unit_serializer = self.get_serializer(data=apartment_unit)

        if apartment_unit_serializer.is_valid():
            try:
                apartment_unit_serializer.save(apartment=apartment_instance)
                return Response(data=apartment_unit_serializer.data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                print("Something went wrong when saving apartment unit!")
                return Response(data="Something went wrong when saving apartment unit!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        else:
            print("Apartment unit data is not valid!")
            return Response(data="Apartment unit data is not valid!", status=status.HTTP_400_BAD_REQUEST)
    

class ApartmentUnitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.ApartmentUnit.objects.all()
    serializer_class = prop_serializers.ApartmentUnitSerializer
    permission_classes = [IsAuthenticated,]


#============= VILLA ============================================================
class VillaListByAgentView(generics.ListAPIView):
    # queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.VillaSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
            # print(currentAgentAdmin.agent.id)
        except ObjectDoesNotExist:
            return None
        
        villas = prop_models.Villa.objects.filter(agent=currentAgentAdmin.agent.id)

        return villas

class VillaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Villa.objects.all()
    serializer_class = prop_serializers.VillaSerializer
    permission_classes = [IsAuthenticated,]


#============= CONDOMINIUM ========================================================
class CondominiumListByAgentView(generics.ListAPIView):
    # queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.CondominiumSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
            # print(currentAgentAdmin.agent.id)
        except ObjectDoesNotExist:
            return None
        
        condominiums = prop_models.Condominium.objects.filter(agent=currentAgentAdmin.agent.id)

        return condominiums

class CondominiumRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Condominium.objects.all()
    serializer_class = prop_serializers.CondominiumSerializer
    permission_classes = [IsAuthenticated,]


#============= TRADITIONAL HOUSE ===================================================
class TraditionalHouseListByAgentView(generics.ListAPIView):
    # queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.TraditionalHouseSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
            # print(currentAgentAdmin.agent.id)
        except ObjectDoesNotExist:
            return None
        
        traditional_house = prop_models.TraditionalHouse.objects.filter(agent=currentAgentAdmin.agent.id)

        return traditional_house

class TraditionalHouseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.TraditionalHouse.objects.all()
    serializer_class = prop_serializers.TraditionalHouseSerializer
    permission_classes = [IsAuthenticated,]


#============= COMMERCIAL PROPERTY =======================================================
class CommercialPropertyListByAgentView(generics.ListAPIView):
    serializer_class = prop_serializers.CommercialPropertySerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
            # print(currentAgentAdmin.agent.id)
        except ObjectDoesNotExist:
            return None
        
        commericial_property = prop_models.CommercialProperty.objects.filter(agent=currentAgentAdmin.agent.id)

        return commericial_property

class CommercialPropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.CommercialProperty.objects.all()
    serializer_class = prop_serializers.CommercialPropertySerializer
    permission_classes = [IsAuthenticated,]


class CommercialPropertyUnitByCommercialPropertyView(generics.ListAPIView):
    queryset = prop_models.CommercialPropertyUnit.objects.all()
    serializer_class = prop_serializers.CommercialPropertyUnitSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, **kwargs):
        commercial_property_Id = request.query_params.get("commercial_property")

        commercial_property_units = prop_models.CommercialPropertyUnit.objects.filter(commercial_property=commercial_property_Id)
        # print("commercial_property_units: ",commercial_property_units)
        if commercial_property_units.exists():
            commercial_property_unit_serializer = self.get_serializer(commercial_property_units, many=True)
        
        else:
            return Response(data="Commercial Property Unit does not exist for this Commercial Property!", status=status.HTTP_404_NOT_FOUND)

        return Response(data=commercial_property_unit_serializer.data, status=status.HTTP_200_OK)


class CommercialPropertyUnitCreateView(generics.CreateAPIView):
    queryset = prop_models.CommercialPropertyUnit.objects.all()
    serializer_class = prop_serializers.CommercialPropertyUnitCreateBasicSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, **kwargs):

        commercial_property_id = request.data.get("commercial_property")
        commercial_property_unit = request.data.get("unit")

        try:
            commercial_property_instance = prop_models.CommercialProperty.objects.get(pk=commercial_property_id)

        except ObjectDoesNotExist:
            print(f"Commercial Property {commercial_property_id} is not found!")
            return Response(data=f"Commercial Property {commercial_property_id} is not found!", status=status.HTTP_404_NOT_FOUND)

        commercial_property_unit_serializer = self.get_serializer(data=commercial_property_unit)

        if commercial_property_unit_serializer.is_valid():
            try:
                commercial_property_unit_serializer.save(commercial_property=commercial_property_instance)
                return Response(data=commercial_property_unit_serializer.data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                print("Something went wrong when saving commercial property unit!")
                return Response(data="Something went wrong when saving commercial property unit!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        else:
            print("Commercial property unit data is not valid!")
            return Response(data="Commercial property unit data is not valid!", status=status.HTTP_400_BAD_REQUEST)
    

class CommercialPropertyUnitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.CommercialPropertyUnit.objects.all()
    serializer_class = prop_serializers.CommercialPropertyUnitSerializer
    permission_classes = [IsAuthenticated,]

#=============== OFFICE =======================================================
class OfficeListByAgentView(generics.ListAPIView):
    serializer_class = prop_serializers.OfficeSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
        except ObjectDoesNotExist:
            return None
        
        offices = prop_models.Office.objects.filter(agent=currentAgentAdmin.agent.id)

        return offices


class OfficeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Office.objects.all()
    serializer_class = prop_serializers.OfficeSerializer
    permission_classes = [IsAuthenticated,]

#=============== HALL =======================================================
class HallListByAgentView(generics.ListAPIView):
    serializer_class = prop_serializers.HallSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
        except ObjectDoesNotExist:
            return None
        
        halls = prop_models.Hall.objects.filter(agent=currentAgentAdmin.agent.id)

        return halls


class HallRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Hall.objects.all()
    serializer_class = prop_serializers.HallSerializer
    permission_classes = [IsAuthenticated,]


#============= ALL PURPOSE PROPERTY =======================================================
class AllPurposePropertyListByAgentView(generics.ListAPIView):
    serializer_class = prop_serializers.AllPurposePropertySerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return None
        try:
            currentAgentAdmin = agnt_models.AgentAdmin.objects.get(admin=user)
            # print(currentAgentAdmin.agent.id)
        except ObjectDoesNotExist:
            return None
        
        all_purpose_propertys = prop_models.AllPurposeProperty.objects.filter(agent=currentAgentAdmin.agent.id)

        return all_purpose_propertys

class AllPurposePropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.AllPurposeProperty.objects.all()
    serializer_class = prop_serializers.AllPurposePropertySerializer
    permission_classes = [IsAuthenticated,]


class AllPurposePropertyUnitByAllPurposePropertyView(generics.ListAPIView):
    queryset = prop_models.AllPurposePropertyUnit.objects.all()
    serializer_class = prop_serializers.AllPurposePropertyUnitSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request, **kwargs):
        all_purpose_property_Id = request.query_params.get("all_purpose_property")

        all_purpose_property_units = prop_models.AllPurposePropertyUnit.objects.filter(all_purpose_property=all_purpose_property_Id)
        # print("all_purpose_property_units: ",all_purpose_property_units)
        if all_purpose_property_units.exists():
            all_purpose_property_unit_serializer = self.get_serializer(all_purpose_property_units, many=True)
        
        else:
            return Response(data="All Purpose Property Unit does not exist for this All Purpose Property!", status=status.HTTP_404_NOT_FOUND)

        return Response(data=all_purpose_property_unit_serializer.data, status=status.HTTP_200_OK)


class AllPurposePropertyUnitCreateView(generics.CreateAPIView):
    queryset = prop_models.AllPurposePropertyUnit.objects.all()
    serializer_class = prop_serializers.AllPurposePropertyUnitCreateBasicSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, **kwargs):

        all_purpose_property_id = request.data.get("all_purpose_property")
        all_purpose_property_unit = request.data.get("unit")

        try:
            all_purpose_property_instance = prop_models.AllPurposeProperty.objects.get(pk=all_purpose_property_id)

        except ObjectDoesNotExist:
            print(f"All Purpose Property {all_purpose_property_id} is not found!")
            return Response(data=f"All Purpose Property {all_purpose_property_id} is not found!", status=status.HTTP_404_NOT_FOUND)

        all_purpose_property_unit_serializer = self.get_serializer(data=all_purpose_property_unit)

        if all_purpose_property_unit_serializer.is_valid():
            try:
                all_purpose_property_unit_serializer.save(all_purpose_property=all_purpose_property_instance)
                return Response(data=all_purpose_property_unit_serializer.data, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                print("Something went wrong when saving All Purpose property unit!")
                return Response(data="Something went wrong when saving All Purpose property unit!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        else:
            print("All Purpose property unit data is not valid!")
            return Response(data="All Purpose property unit data is not valid!", status=status.HTTP_400_BAD_REQUEST)
    

class AllPurposePropertyUnitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.AllPurposePropertyUnit.objects.all()
    serializer_class = prop_serializers.AllPurposePropertyUnitSerializer
    permission_classes = [IsAuthenticated,]

#================================================================================

class HouseTypeListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.HouseType.objects.all()
    serializer_class = prop_serializers.HouseTypeSerializer
    permission_classes = [AllowAny,]


class BuildingTypeListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.BuildingType.objects.all()
    serializer_class = prop_serializers.HouseTypeSerializer
    permission_classes = [AllowAny,]

class PropertyImageListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyImage.objects.all()
    serializer_class = prop_serializers.PropertyImageSerializer
    parser_clasess = [MultiPartParser, FormParser]
    permission_classes = [AllowAny,]

    # def get_queryset(self):
    #     return prop_models.PropertyImage.objects.all()
    
    def post(self, request, format=None):
        # print("======REQUEST=====: ",request.data)
        imageData = request.data
        propertyId = imageData.pop("property")
        # print("======PROPID=====: ", propertyId)
        try:
            property_instance = prop_models.Property.objects.get(pk=propertyId[0])
        except ObjectDoesNotExist:
            print("Property is not found!")
            return Response(data="Property is not found!", status=status.HTTP_404_NOT_FOUND)

        
        property_image_serializer = prop_serializers.PropertyImageSerializer(data=imageData, context={"request": request})

        if property_image_serializer.is_valid():
            property_image_instance = property_image_serializer.save(property=property_instance)
            print("CREATED!!!!!!!!!!!!!!")
            return Response(data=property_image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Property Image is not valid!")
            return Response(data="Property Image is not valid!", status=status.HTTP_400_BAD_REQUEST)


class PropertyVideoListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyVideo.objects.all()
    serializer_class = prop_serializers.PropertyVideoSerializer
    parser_clasess = [MultiPartParser, FormParser]
    permission_classes = [AllowAny,]

    # def get_queryset(self):
    #     return prop_models.PropertyImage.objects.all()
    
    def post(self, request, format=None):
        # print("======REQUEST=====: ",request.data)
        VideoData = request.data
        propertyId = VideoData.pop("property")
        # print("======PROPID=====: ", propertyId)
        try:
            property_instance = prop_models.Property.objects.get(pk=propertyId[0])
        except ObjectDoesNotExist:
            print("Property is not found!")
            return Response(data="Property is not found!", status=status.HTTP_404_NOT_FOUND)

        
        property_video_serializer = self.get_serializer(data=VideoData, context={"request": request})

        if property_video_serializer.is_valid():
            property_video_instance = property_video_serializer.save(property=property_instance)
            print("CREATED!!!!!!!!!!!!!!")
            return Response(data=property_video_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Property Video is not valid!")
            return Response(data="Property Video is not valid!", status=status.HTTP_400_BAD_REQUEST)

#=====================================================================================================================
class PropertyImageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PropertyImage.objects.all()
    serializer_class = prop_serializers.PropertyImageSerializer
    permission_classes = [AllowAny,]

class PropertyVideoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PropertyVideo.objects.all()
    serializer_class = prop_serializers.PropertyVideoSerializer
    permission_classes = [AllowAny,]


#====================EDUCATION FACILITIES==============================================================================
class PropertyFileLabelListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyFileLabel.objects.all()
    serializer_class = prop_serializers.PropertyFileLabelSerializer
    permission_classes = [AllowAny,]

#=====================================================================================================================
class EduFaLevelListView(generics.ListAPIView):
    queryset = prop_models.EdufaLevel.objects.all()
    serializer_class = prop_serializers.EdufaLevelSerializer
    permission_classes = [AllowAny,]

class EducationFacilityListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.EducationFacility.objects.all()
    serializer_class = prop_serializers.EducationFacilityBasicCreateSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, **kwargs):

        propertyId = request.data.pop("property")
        # print(request.data)

        try:
            property_instance = prop_models.Property.objects.get(pk=propertyId)
        except ObjectDoesNotExist:
            return Response(data="Property is not found!", status=status.HTTP_404_NOT_FOUND)

        edufa_serializer = self.get_serializer(data=request.data)

        if edufa_serializer.is_valid():
            edufa_instance = edufa_serializer.save()

            if edufa_instance:
                prop_models.PropertyEduFacility.objects.create(education_facility=edufa_instance, property=property_instance)
                return Response(data=edufa_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Wrong when saving education facility!")
                return Response(data="Wrong when saving education facility!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            print("Bad Edufa data!")
            return Response(data="Bad Edufa data!", status=status.HTTP_400_BAD_REQUEST)


class EducationFacilityCreateFromSearchView(generics.CreateAPIView):
    queryset = prop_models.EducationFacility.objects.all()
    serializer_class = prop_serializers.EducationFacilityBasicCreateSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, **kwargs):
         print(request.data)
         
         property_id = request.data.get("property")
         edufa_id = request.data.get("edufa")
        #  print("property_id ",property_id)

         try:
             property_instance = prop_models.Property.objects.get(pk=property_id)
         except ObjectDoesNotExist:
             print(f"Property {property_id} is not found!")
             return Response(data=f"Property {property_id} is not found!", status=status.HTTP_404_NOT_FOUND)
         try:
             edufa_instance = prop_models.EducationFacility.objects.get(pk=edufa_id)
         except ObjectDoesNotExist:
             print(f"Education facility {edufa_id} is not found!")
             return Response(data=f"Education facility {edufa_id} is not found!", status=status.HTTP_404_NOT_FOUND)

         prop_edufa_instance = prop_models.PropertyEduFacility.objects.create(property=property_instance, education_facility=edufa_instance)
         
         if prop_edufa_instance:
             return Response(data="Cretaed!", status=status.HTTP_201_CREATED)
         else:
            print("Wrong when saving property education facility!")
            return Response(data="Wrong when saving property education facility!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EducationFacilitySearchView(generics.ListAPIView):
    search_fields = ["name", "description"]
    filter_backends = (filters.SearchFilter,)
    queryset = prop_models.EducationFacility.objects.all()
    serializer_class = prop_serializers.EducationFacilitySerializer
    # permission_classes = [IsAuthenticated,]

class EducationFacilityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.EducationFacility.objects.all()
    serializer_class = prop_serializers.EducationFacilitySerializer
    permission_classes = [IsAuthenticated,]

    def delete(self, request, **kwargs):
        property_id = request.query_params.get("property")
        edufa_id = request.query_params.get("edufa")

        property_edufa_instance = prop_models.PropertyEduFacility.objects.filter(property=property_id, education_facility=edufa_id)
        
        if property_edufa_instance.exists():
            try:
                property_edufa_instance.delete()
                return Response(data="Deleted!", status=status.HTTP_204_NO_CONTENT)
            except:
                print("Something wrong when deleting property education facility!")
                return Response(data="Something wrong when deleting property education facility!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            print("Property Education Facility is not found!")
            return Response(data="Property Education Facility is not found!", status=status.HTTP_404_NOT_FOUND)

#====================PROPERTY FILE LABEL==============================================================================
class PropertyFileLabelListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PropertyFileLabel.objects.all()
    serializer_class = prop_serializers.PropertyFileLabelSerializer
    permission_classes = [AllowAny,]

#===================TRANSPORT FACILITY================================================================================
class TranfaCategoryListView(generics.ListAPIView):
    queryset = prop_models.TransFaCategory.objects.all()
    serializer_class = prop_serializers.TransFaCategorySerializer
    permission_classes = [AllowAny,]

class TransportFacilityListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.TransportFacility.objects.all()
    serializer_class = prop_serializers.TransportFacilityBasicCreateSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, **kwargs):

        # print(request.data)
        propertyId = request.data.pop("property")
        # print(request.data)

        try:
            property_instance = prop_models.Property.objects.get(pk=propertyId)
        except ObjectDoesNotExist:
            return Response(data="Property is not found!", status=status.HTTP_404_NOT_FOUND)

        tranfa_serializer = self.get_serializer(data=request.data)

        if tranfa_serializer.is_valid():
            tranfa_instance = tranfa_serializer.save()

            if tranfa_instance:
                prop_models.PropertyTransFacility.objects.create(transport_facility=tranfa_instance, property=property_instance)
                return Response(data=tranfa_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Wrong when saving transport facility!")
                return Response(data="Wrong when saving transport facility!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            print("Bad transport facility data!")
            return Response(data="Bad transport facility data!", status=status.HTTP_400_BAD_REQUEST)


class TransportFacilityCreateFromSearchView(generics.CreateAPIView):
    queryset = prop_models.TransportFacility.objects.all()
    serializer_class = prop_serializers.TransportFacilityBasicCreateSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, **kwargs):
         print(request.data)
         
         property_id = request.data.get("property")
         tranfa_id = request.data.get("tranfa")
        #  print("property_id ",property_id)

         try:
             property_instance = prop_models.Property.objects.get(pk=property_id)
         except ObjectDoesNotExist:
             print(f"Property {property_id} is not found!")
             return Response(data=f"Property {property_id} is not found!", status=status.HTTP_404_NOT_FOUND)
         try:
             tranfa_instance = prop_models.TransportFacility.objects.get(pk=tranfa_id)
         except ObjectDoesNotExist:
             print(f"Transport facility {tranfa_id} is not found!")
             return Response(data=f"Transport facility {tranfa_id} is not found!", status=status.HTTP_404_NOT_FOUND)

         prop_tranfa_instance = prop_models.PropertyTransFacility.objects.create(property=property_instance, transport_facility=tranfa_instance)
         
         if prop_tranfa_instance:
             return Response(data="Cretaed!", status=status.HTTP_201_CREATED)
         else:
            print("Wrong when saving property transport facility!")
            return Response(data="Wrong when saving property transport facility!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransportFacilitySearchView(generics.ListAPIView):
    search_fields = ["name", "description"]
    filter_backends = (filters.SearchFilter,)
    queryset = prop_models.TransportFacility.objects.all()
    serializer_class = prop_serializers.TransportFacilitySerializer
    # permission_classes = [IsAuthenticated,]

class TransportFacilityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.TransportFacility.objects.all()
    serializer_class = prop_serializers.TransportFacilitySerializer
    permission_classes = [IsAuthenticated,]

    def delete(self, request, **kwargs):
        property_id = request.query_params.get("property")
        edufa_id = request.query_params.get("tranfa")
        print(property_id, edufa_id)
        property_tranfa_instance = prop_models.PropertyTransFacility.objects.filter(property=property_id, transport_facility=edufa_id)
            
        if property_tranfa_instance.exists():
            try:
                property_tranfa_instance.delete()
                return Response(data="Deleted!", status=status.HTTP_204_NO_CONTENT)
            except:
                print("Something wrong when deleting property transport facility!")
                return Response(data="Something wrong when deleting property transport facility!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Property Transport Facility is not found!")
            return Response(data="Property Transport Facility is not found!", status=status.HTTP_404_NOT_FOUND)

#===================POINT OF INTEREST================================================================================
class POICategoryListView(generics.ListAPIView):
    queryset = prop_models.POICategory.objects.all()
    serializer_class = prop_serializers.POICategorySerializer
    permission_classes = [AllowAny,]

class POIListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.PointOfInterest.objects.all()
    serializer_class = prop_serializers.POIBasicCreateSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, **kwargs):

        # print(request.data)
        propertyId = request.data.pop("property")
        # print(request.data)

        try:
            property_instance = prop_models.Property.objects.get(pk=propertyId)
        except ObjectDoesNotExist:
            return Response(data="Property is not found!", status=status.HTTP_404_NOT_FOUND)

        poi_serializer = self.get_serializer(data=request.data)

        if poi_serializer.is_valid():
            poi_instance = poi_serializer.save()

            if poi_instance:
                prop_models.PropertyPOI.objects.create(point_of_interest=poi_instance, property=property_instance)
                return Response(data=poi_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Wrong when saving point of interest!")
                return Response(data="Wrong when saving point of interest!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            print("Bad point of interest data!")
            return Response(data="Bad point of interest data!", status=status.HTTP_400_BAD_REQUEST)


class POICreateFromSearchView(generics.CreateAPIView):
    queryset = prop_models.PointOfInterest.objects.all()
    serializer_class = prop_serializers.POIBasicCreateSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, **kwargs):
         print(request.data)
         
         property_id = request.data.get("property")
         poi_id = request.data.get("poi")
        #  print("property_id ",property_id)

         try:
             property_instance = prop_models.Property.objects.get(pk=property_id)
         except ObjectDoesNotExist:
             print(f"Property {property_id} is not found!")
             return Response(data=f"Property {property_id} is not found!", status=status.HTTP_404_NOT_FOUND)
         try:
             poi_instance = prop_models.PointOfInterest.objects.get(pk=poi_id)
         except ObjectDoesNotExist:
             print(f"Point of Interest {poi_id} is not found!")
             return Response(data=f"Point of Interest {poi_id} is not found!", status=status.HTTP_404_NOT_FOUND)
         try:
            prop_poi_instance = prop_models.PropertyPOI.objects.create(property=property_instance, point_of_interest=poi_instance)
            if prop_poi_instance:
                return Response(data="Cretaed!", status=status.HTTP_201_CREATED)
            else:
                print("Wrong when saving property Point of Interest!")
                return Response(data="Wrong when saving property Point of Interest!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         except:
            print("Wrong when saving property Point of Interest!")
            return Response(data="Wrong when saving property Point of Interest!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class POISearchView(generics.ListAPIView):
    search_fields = ["name", "description"]
    filter_backends = (filters.SearchFilter,)
    queryset = prop_models.PointOfInterest.objects.all()
    serializer_class = prop_serializers.PointOfInterestSerializer
    # permission_classes = [IsAuthenticated,]

class POIRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PointOfInterest.objects.all()
    serializer_class = prop_serializers.PointOfInterestSerializer
    permission_classes = [IsAuthenticated,]

    def delete(self, request, **kwargs):
        property_id = request.query_params.get("property")
        poi_id = request.query_params.get("poi")
        print(property_id, poi_id)
        property_poi_instance = prop_models.PropertyPOI.objects.filter(property=property_id, point_of_interest=poi_id)
            
        if property_poi_instance.exists():
            try:
                property_poi_instance.delete()
                return Response(data="Deleted!", status=status.HTTP_204_NO_CONTENT)
            except:
                print("Something wrong when deleting property point of interest!")
                return Response(data="Something wrong when deleting property point of interest!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Property point of interest is not found!")
            return Response(data="Property point of interest is not found!", status=status.HTTP_404_NOT_FOUND)

#===================PROPERTY AMENITY================================================================================
class PropertyAmenityCreateView(generics.CreateAPIView):
     queryset = prop_models.Property.objects.all()
     serializer_class = prop_serializers.PropertySerializer
     permission_classes = [IsAuthenticated,]

     def post(self, request, **kwargs):
        #  print(request.data)

        property_id = request.data.get("property")
        amenities = request.data.get("amenity")

        try:
            property_instance = prop_models.Property.objects.get(pk=property_id)
        except ObjectDoesNotExist:
            print(f"Property {property_id} is not found!")
            return Response(data=f"Property {property_id} is not found!", status=status.HTTP_404_NOT_FOUND)

        for amenity_id in amenities:
            try:
                amenity_instance = prop_models.Amenity.objects.get(pk=amenity_id)
                prop_models.PropertyAmenity.objects.create(property=property_instance, amenity=amenity_instance)
            except ObjectDoesNotExist:
                print(f"Amenity {amenity_id} is not found!")
                # return Response(data=f"Amenity {amenity_id} is not found!", status=status.HTTP_404_NOT_FOUND)
        
        print(f"Amenities created for property {property_id}")
        return Response(data=f"Amenities created for property {property_id}", status=status.HTTP_201_CREATED)


class PropertyAmenityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Amenity.objects.all()
    serializer_class = prop_serializers.AmenitySerializer
    permission_classes = [IsAuthenticated,]

    def delete(self, request, **kwargs):
        property_id = request.query_params.get("property")
        amenity_id = request.query_params.get("amenity")
        print(property_id, amenity_id)
        property_amenity_instance = prop_models.PropertyAmenity.objects.filter(property=property_id, amenity=amenity_id)
            
        if property_amenity_instance.exists():
            try:
                property_amenity_instance.delete()
                return Response(data="Deleted!", status=status.HTTP_204_NO_CONTENT)
            except:
                print("Something wrong when deleting property amenity!")
                return Response(data="Something wrong when deleting property amenity!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Property amenity is not found!")
            return Response(data="Property amenity is not found!", status=status.HTTP_404_NOT_FOUND)

#===================RULE================================================================================
class RuleListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.Rule.objects.all()
    serializer_class = prop_serializers.RuleSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, **kwargs):
        # print(request.data)

        property_id = request.data.pop("property")
        rule = request.data.pop("rule")

        # print(rule)

        try:
            property_instance = prop_models.Property.objects.get(pk=property_id)
        except ObjectDoesNotExist:
            print(f"Property {property_id} is not found!")
            return Response(data=f"Property {property_id} is not found!", status=status.HTTP_404_NOT_FOUND)

        rule_serializer = self.get_serializer(data=rule)

        if rule_serializer.is_valid():
            try:
                rule_serializer.save(property=property_instance)
                return Response(data=rule_serializer.data, status=status.HTTP_201_CREATED)
            except:
                print("Something wrong when creating property rule!")
                return Response(data="Something wrong when creating property rule!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            print("Rule data is not valid!")
            return Response(data="Rule data is not valid!", status=status.HTTP_400_BAD_REQUEST)


class RuleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Rule.objects.all()
    serializer_class = prop_serializers.RuleSerializer
    permission_classes = [IsAuthenticated,]

#===================LISTING DISCOUNT BY CATEGORY====================================================================
class ListingDiscountByCategoryListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.ListingDiscountByCategory.objects.all()
    serializer_class = prop_serializers.ListingDiscountByCategorySerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request, **kwargs):

        category_key = request.query_params.get("property_category")
        print("YOOOO!!! ",category_key)

        try:
            category_instance = prop_models.PropertyCategory.objects.get(cat_key=category_key)
        except ObjectDoesNotExist:
            return Response(data="Property Category is not found!", status=status.HTTP_404_NOT_FOUND)

        property_discounts = prop_models.ListingDiscountByCategory.objects.filter(property_category=category_instance.id)

        if property_discounts.exists():
            return Response(data=self.get_serializer(property_discounts, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(data=[], status=status.HTTP_404_NOT_FOUND)


#===================LISTING PRICE BY CATEGORY====================================================================
class ListingPriceByCategoryListCreateView(generics.ListCreateAPIView):
    queryset = prop_models.ListingPriceByCategory.objects.all()
    serializer_class = prop_serializers.ListingPriceByCategorySerializer
    # permission_classes = [IsAuthenticated,]

    def get(self, request, **kwargs):

        category_key = request.query_params.get("property_category")

        try:
            category_instance = prop_models.PropertyCategory.objects.get(cat_key=category_key)
        except ObjectDoesNotExist:
            return Response(data="Property Category is not found!", status=status.HTTP_404_NOT_FOUND)

        property_prices = prop_models.ListingPriceByCategory.objects.filter(property_category=category_instance.id)

        if property_prices.exists():
            return Response(data=self.get_serializer(property_prices, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(data=[], status=status.HTTP_404_NOT_FOUND)


#=========================================================================================================
class ApartmentUnitRetrievePublicView(generics.RetrieveAPIView):
    queryset = prop_models.ApartmentUnit.objects.all()
    serializer_class = prop_serializers.ApartmentUnitSerializer


#=========================================================================================================
class CommercialPropertyUnitRetrievePublicView(generics.RetrieveAPIView):
    queryset = prop_models.CommercialPropertyUnit.objects.all()
    serializer_class = prop_serializers.CommercialPropertyUnitSerializer


#=========================================================================================================
class AllPurposePropertyUnitRetrievePublicView(generics.RetrieveAPIView):
    queryset = prop_models.AllPurposePropertyUnit.objects.all()
    serializer_class = prop_serializers.AllPurposePropertyUnitSerializer