from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from listings import models as list_models
from listings import serializers as list_serializers
from listings.paginations import PublicListingPagination
from agents import models as agent_models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from listings.paginations import FeaturedListingPagination
from payments import serializers as pay_serializers
from payments import models as pay_models
from properties import models as prop_models
from properties import serializers as prop_serializers
from django.http.request import QueryDict
from django.db.models import Q

from myhome.strings import *
from rest_framework.parsers import MultiPartParser, FormParser


class ListingModeListView(generics.ListAPIView):
    queryset = list_models.ListingMode.objects.all()
    serializer_class = list_serializers.ListingModeSerializer
    # permission_classes = [IsAuthenticated,]


class ListingTypeListView(generics.ListAPIView):
    queryset = list_models.ListingType.objects.all()
    serializer_class = list_serializers.ListingTypeSerializer
    # permission_classes = [IsAuthenticated,]


class ListingStateListView(generics.ListAPIView):
    queryset = list_models.ListingState.objects.all()
    serializer_class = list_serializers.ListingStateSerializer
    # permission_classes = [IsAuthenticated,]


class AgentNumberOfListingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, **kwargs):
        user = self.request.user
        try:
            currentAgentAdmin = agent_models.AgentAdmin.objects.get(admin=user)
        except ObjectDoesNotExist:
            return None
        
        agent_listing_count = list_models.MainListing.objects.filter(agent=currentAgentAdmin.agent).count()

        return Response(data=agent_listing_count, status=status.HTTP_200_OK)


class ListingListCreateView(generics.ListCreateAPIView):
    queryset = list_models.MainListing.objects.all()
    serializer_class = list_serializers.MainListingSerializer
    permission_classes = [IsAuthenticated,]
    parser_clasess = [MultiPartParser, FormParser]

    def post(self, request, **kwargs):
        
        print(request.data)
        pm_key = request.data.get("payment[pm_key]")

        #==================COUPON================================================================
        coupon_payment_instance = None

        use_coupon = request.data.get("payment[coupon][use_coupon_payment]")
        listing_price = float(request.data.get("payment[listing_price]"))
        
        if use_coupon:
            coupon_code = request.data.get("payment[coupon][coupon_code]")
            try:
                coupon_instance = pay_models.Coupon.objects.get(code=coupon_code)
            except ObjectDoesNotExist:
                print(f"Coupon {coupon_code} not found!")
                return Response(data=f"Coupon {coupon_code} not found!", status=status.HTTP_404_NOT_FOUND)
            paid_amount = None
            try:
                if coupon_instance.current_value >= listing_price:
                    
                    paid_amount = listing_price
                else:
                    paid_amount = coupon_instance.current_value
                coupon_payment_instance = pay_models.CouponPayment.objects.create(coupon=coupon_instance, paid_amount=paid_amount)
                print("YOOOOOOOOO!!!!!: ",coupon_instance.current_value - paid_amount)
                pay_models.Coupon.objects.filter(code=coupon_code).update(current_value=coupon_instance.current_value - paid_amount)
                print("COUPON SAVED!!!!!!!!!")

            except:
                print(f"Something went wrong during saving coupon payment!")
                return Response(data=f"Something went wrong during saving coupon payment!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       
       
        #==================PAYMENT================================================================

        payment = {}

        payment["payment_method"] = request.data.get("payment[payment_method]")
        payment["total_price"] = float(listing_price)
        if coupon_payment_instance:
            payment["coupon_payment"] = coupon_payment_instance.id
        if pm_key == PM_CASH_PAYMENT or pm_key == PM_BANK_TRANSFER or pm_key == PM_MOBILE_PAYMENT:
             payment["is_approved"] = False
        else:
             payment["is_approved"] = True
        payment["narrative"] = request.data.get("payment[narrative]")

        payment_querydict = QueryDict("", mutable=True)
        payment_querydict.update(payment)

        payment_serializer = pay_serializers.PaymentSerializer(data=payment_querydict)
        if payment_serializer.is_valid():
            payment_instance = payment_serializer.save()
            print("PAYMENT SAVED!!!!!!!!!")
        else:
            print("Payment data is not valid!")
            return Response(data="Payment data is not valid!", status=status.HTTP_400_BAD_REQUEST)
    
        sub_payment_data = {}

        if pm_key == PM_BANK_TRANSFER:
            sub_payment_data["bank_name"] = request.data.get("payment[bank_transfer][bank_name]")
            sub_payment_data["bank_branch_name"] = request.data.get("payment[bank_transfer][bank_branch_name]")
            sub_payment_data["transaction_ref_number"] = request.data.get("payment[bank_transfer][transaction_ref_number]")
            sub_payment_data["payment_date"] = request.data.get("payment[bank_transfer][payment_date]")
            sub_payment_data["bank_full_address"] = request.data.get("payment[bank_transfer][bank_full_address]")


            bank_transfer_queridict = QueryDict("", mutable=True)
            bank_transfer_queridict.update(sub_payment_data)
            bank_transfer_serializer = pay_serializers.BankPaymentCreatBasicSerializer(data=bank_transfer_queridict)
            if bank_transfer_serializer.is_valid():
                # print("BANK: YAYYYYYY! BANK IS VALID")
                bank_transfer_instance = bank_transfer_serializer.save(payment=payment_instance)
                print("BANK TRANSFER SAVED!!!!!!!!!")

            else:
                print("Bank Payment data is not valid!")
                return Response(data="Bank Payment data is not valid!", status=status.HTTP_400_BAD_REQUEST)


        if pm_key == PM_BANK_TRANSFER or pm_key == PM_MOBILE_PAYMENT:
            reciepts = request.data.getlist("reciept")

            
            for reciept in reciepts:
                sub_payment = {"reciept": reciept}
                sub_payment_querydict = QueryDict("", mutable=True)
                sub_payment_querydict.update(sub_payment)

                sub_payment_serializer = None
                if pm_key == PM_BANK_TRANSFER:
                    sub_payment_serializer = pay_serializers.BankRecieptCreateBasicSerializer(data=sub_payment_querydict)
                    
                else:
                    print("Bank Reciept is not valid!")
                    return Response(data="Bank Reciept is not valid!", status=status.HTTP_400_BAD_REQUEST)



                if sub_payment_serializer.is_valid():
                    sub_payment_serializer.save(bank_payment=bank_transfer_instance)
                    print("Bank Reciept Saved!")
                else:
                    print("Sub-payment data is not valid!")
                    return Response(data="Sub-payment data is not valid!", status=status.HTTP_400_BAD_REQUEST)

        
        #==================MAIN LISTING==========================================================

        main_listing = {}

        main_listing["listing_type"] = request.data.get("main_listing[listing_type]")
        main_listing["property_price"] = request.data.get("main_listing[property_price]")
        main_listing["listing_currency"] = request.data.get("main_listing[listing_currency]")
        main_listing["listing_term"] = request.data.get("main_listing[listing_term]")
        main_listing["description"] = request.data.get("main_listing[description]")
        main_listing["deposit_in_months"] = request.data.get("main_listing[deposit_in_months]")
        main_listing["property"] = request.data.get("main_listing[property]")
        main_listing["sub_property"] = request.data.get("main_listing[sub_property]")
        main_listing["agent"] = request.data.get("main_listing[agent]")

        if pm_key == PM_CASH_PAYMENT or pm_key == PM_BANK_TRANSFER or pm_key == PM_MOBILE_PAYMENT:
             main_listing["listing_state"] = "INACTIVE"
             main_listing["is_approved"] = False
        else:
             main_listing["listing_state"] = "ACTIVE"
             main_listing["is_approved"] = True

        if pm_key == PM_SUBSCRIPTION:
            main_listing["listing_mode"] = "SUBSCRIPTION"
        else:
            main_listing["listing_mode"] = "PAY_PER_LISTING"
        

        main_listing_querydict = QueryDict("", mutable=True)
        main_listing_querydict.update(main_listing)
        main_listing_serializer = self.get_serializer(data=main_listing_querydict)

        if main_listing_serializer.is_valid():
            # print("MAIN LISTING: YAYYYYYY! MAIN LISTING IS VALID")
            main_listing_instance = main_listing_serializer.save(payment=payment_instance)
            print("MAIN LISTING SAVED!!!")
        else:
            print("Main listing has invalid data!")
            return Response(data="Main listing has ivalid data!", status=status.HTTP_400_BAD_REQUEST)

        #=================SUB LISTING============================================================
        cat_key = request.data.get("main_listing[cat_key]")
        sub_property_id = request.data.get("main_listing[sub_property]")

        try:
            if cat_key == VILLA_KEY:
                villa_instance = prop_models.Villa.objects.get(id=sub_property_id)
                list_models.VillaListing.objects.create(villa=villa_instance, main_listing=main_listing_instance)
                print("VILLA LISTING SAVED!!!!!!!!!")
            elif cat_key == CONDOMINIUM_KEY:
                condominium_instance = prop_models.Condominium.objects.get(id=sub_property_id)
                list_models.CondominiumListing.objects.create(condominium=condominium_instance, main_listing=main_listing_instance)
                print("CONDOMINIUM LISTING SAVED!!!!!!!!!")
            elif cat_key == TRADITIONAL_HOUSE_KEY:
                traditional_house_instance = prop_models.TraditionalHouse.objects.get(id=sub_property_id)
                list_models.TraditionalHouseListing.objects.create(traditional_house=traditional_house_instance, main_listing=main_listing_instance)
                print("TRADITIONAL HOUSE LISTING SAVED!!!!!!!!!")
            elif cat_key == SHARE_HOUSE_KEY:
                share_house_instance = prop_models.ShareHouse.objects.get(id=sub_property_id)
                list_models.ShareHouseListing.objects.create(Share_house=share_house_instance, main_listing=main_listing_instance)
                print("SHARE HOUSE LISTING SAVED!!!!!!!!!")
            elif cat_key == OFFICE_KEY:
                office_instance = prop_models.Office.objects.get(id=sub_property_id)
                list_models.OfficeListing.objects.create(office=office_instance, main_listing=main_listing_instance)
                print("OFFICE LISTING SAVED!!!!!!!!!")
            elif cat_key == LAND_KEY:
                land_instance = prop_models.Land.objects.get(id=sub_property_id)
                list_models.LandListing.objects.create(land=land_instance, main_listing=main_listing_instance)
                print("LAND LISTING SAVED!!!!!!!!!")
            elif cat_key == HALL_KEY:
                hall_instance = prop_models.Hall.objects.get(id=sub_property_id)
                list_models.HallListing.objects.create(hall=hall_instance, main_listing=main_listing_instance)
                print("Hall LISTING SAVED!!!!!!!!!")
            elif cat_key == COMMERCIAL_PROPERTY_KEY:
                unit_id = request.data.get("main_listing[unit]")
                commercial_property_instance = prop_models.CommercialProperty.objects.get(id=sub_property_id)
                unit_instance = prop_models.CommercialPropertyUnit.objects.get(id=unit_id)
                list_models.CommercialPropertyUnitListing.objects.create(commercial_property=commercial_property_instance, commercial_property_unit=unit_instance, main_listing=main_listing_instance)
                print("COMMERCIAL PROPERTY LISTING SAVED!!!!!!!!!")
            elif cat_key == APARTMENT_KEY:
                unit_id = request.data.get("main_listing[unit]")
                # apartment_instance = prop_models.CommercialProperty.objects.get(id=sub_property_id)
                unit_instance = prop_models.ApartmentUnit.objects.get(id=unit_id)
                list_models.ApartmentUnitListing.objects.create(apartment_unit=unit_instance, main_listing=main_listing_instance)
                print("APARTMENT LISTING SAVED!!!!!!!!!")
            elif cat_key == ALL_PURPOSE_PROPERTY_KEY:
                unit_id = request.data.get("main_listing[unit]")
                unit_instance = prop_models.AllPurposePropertyUnit.objects.get(id=unit_id)
                list_models.AllPurposePropertyUnitListing.objects.create(all_purpose_property_unit=unit_instance, main_listing=main_listing_instance)
                print("ALL PURPOSE PROPERTY LISTING SAVED!!!!!!!!!")
        except:
            print("Something went wrong when creating sub_property listing!")
            return Response(data="Something went wrong when creating sub_property listing!", status=status.HTTP_404_NOT_FOUND)

        # if cat_key == VILLA_KEY:
        #     print("VILLA LISTING SAVED!!!!!!!!!")
        #     list_models.VillaListing.objects.create(villa=villa_instance, main_listing=main_listing_instance)
        # elif cat_key == CONDOMINIUM_KEY:
        #     print("CONDOMINIUM LISTING SAVED!!!!!!!!!")
        #     list_models.CondominiumListing.objects.create(condominium=villa_instance, main_listing=main_listing_instance)
       


        
        # print("LISTING DATA: ", request.data)
        
        
        # for file in reciept:
        #     print("FILE DATA: ", file)

        return Response(data=main_listing_serializer.data, status=status.HTTP_201_CREATED)

class MainListingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = list_models.MainListing.objects.all()
    serializer_class = list_serializers.MainListingSerializer
    permission_classes = [IsAuthenticated,]
    #================================================================================================
    #============GET LISTING BY AGENT, PROPERTY, UNIT================================================

class ListingListByProperty(generics.ListAPIView):
    # queryset = list_models.MainListing.objects.all()
    serializer_class = list_serializers.MainListingSerializer
    permission_classes = [IsAuthenticated,]

    # def get(self, request, **kwargs):
    #     user = request.user
    #     propertyId = request.query_params.get("property")
    #     print("propertyId: ",propertyId)
    #     try:
    #         currentAgentAdmin = agent_models.AgentAdmin.objects.get(admin=user)
    #     except ObjectDoesNotExist:
    #         return None
        
    #     listings = list_models.MainListing.objects.filter(agent=currentAgentAdmin.agent, property=propertyId)
    #     if listings.exists():
    #         return Response(data=self.get_serializer(listings, many=True).data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(data="No listing for this Property", status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        user = self.request.user
        propertyId = self.request.query_params.get("property")
        try:
            currentAgentAdmin = agent_models.AgentAdmin.objects.get(admin=user)
        except ObjectDoesNotExist:
            print("AGENT ADMIN DOES NOT EXIST!")
            return None
        
        listings = list_models.MainListing.objects.filter(agent=currentAgentAdmin.agent, property=propertyId)
        return listings

class ListingListByPropertyUnit(generics.ListAPIView):
    serializer_class = list_serializers.CommercialPropertyUnitListingSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        property_unit_id = self.request.query_params.get("unit")
        cat_key = self.request.query_params.get("cat_key")

        if cat_key == COMMERCIAL_PROPERTY_KEY:
            listings = list_models.CommercialPropertyUnitListing.objects.filter(commercial_property_unit=property_unit_id)
            print(self.serializer_class)
        elif cat_key == APARTMENT_KEY:
            self.serializer_class = list_serializers.ApartmentUnitListingSerializer
            listings = list_models.ApartmentUnitListing.objects.filter(apartment_unit=property_unit_id)
            print(self.serializer_class)
        elif cat_key == ALL_PURPOSE_PROPERTY_KEY:
            self.serializer_class = list_serializers.AllPurposePropertyListingSerializer
            listings = list_models.AllPurposePropertyUnitListing.objects.filter(all_purpose_property_unit=property_unit_id)
            print(self.serializer_class)
        return listings

class ListingListByAgent(generics.ListAPIView):
    # queryset = list_models.MainListing.objects.all()
    serializer_class = list_serializers.MainListingSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        try:
            currentAgentAdmin = agent_models.AgentAdmin.objects.get(admin=user)
        except ObjectDoesNotExist:
            return None
        
        listings = list_models.MainListing.objects.filter(agent=currentAgentAdmin.agent)
        return listings


class PublicListingListView(generics.ListAPIView):
    # queryset = list_models.MainListing.objects.all()
    serializer_class = list_serializers.MainListingPublicSerializer
    pagination_class = PublicListingPagination
    # permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        # user = self.request.user
        query_params = self.request.query_params
        
        #GET QUERY PARAMS
        for_sale = query_params["for_sale"]
        for_rent = query_params["for_rent"]
        property_category = int(query_params["property_category"])
        location = (query_params["location"]).strip()
        min_price = float(query_params["min_price"])
        max_price = float(query_params["max_price"])
        number_of_bed_rooms = float(query_params["number_of_bed_rooms"])
        order_by = query_params["sort_by"]

        if max_price==-1:
            max_price = 999999999999

        # print("max_price============>: ",max_price)
        
        #NEW VARIABLES TO HOLD MODIFIED SEARCH PARAMS
        search_listing_types = []
        search_property_categories = None
        
        #IF FOR SALE PROPERTIES ARE NEEDED, ADD TO SEARCH PARAM
        if for_sale == "true":
            search_listing_types.append("SALE")

        #IF FOR RENT PROPERTIES ARE NEEDED, ADD TO SEARCH PARAM
        if for_rent == "true":
            search_listing_types.append("RENT")
        
        #IF NOTHING IS PROVIDED AS LISTING TYPE IN QUERY PARAMS, ADD BOTH TYPES AS SEARCH PARAMS
        if for_sale == "false" and for_rent == "false":
            search_listing_types.append("RENT")
            search_listing_types.append("SALE")
        
        #GET LISTING TYPES BASED ON NEEDED LISTING TYPES
        listing_types = list_models.ListingType.objects.filter(type__in=search_listing_types)

        #IF PROPERY CATEGORY IS NOT PROVIDED IN QUERY PARAMS (-1), ADD ALL CATEGORIES IN THE SEARCH PARAMS
        if property_category == -1:
            search_property_categories = prop_models.PropertyCategory.objects.all()
        else:
            search_property_categories = prop_models.PropertyCategory.objects.filter(pk=property_category)
            

        if order_by == "-1":
            order_by = "-listed_on"

        #PREPARE Q QUERY OBJECT FOR LOCATION IN THE ADDRESS TABLE
        location_search_object = Q()
        if location == "-1":
             location_search_object = Q()
        else:
            location_search_object = Q(property__address__city__name__icontains=location) | \
                                    Q(property__address__region__name__icontains=location) | \
                                    Q(property__address__country__name__icontains=location) | \
                                    Q(property__address__street__icontains=location) | \
                                    Q(property__address__post_code__icontains=location) | \
                                    Q(property__address__building_name_or_number__icontains=location)


        if number_of_bed_rooms == -1:
            number_of_bed_rooms_search_object = Q()
        else:
            if(search_property_categories[0].cat_key==VILLA_KEY):
                number_of_bed_rooms_search_object = Q(property__villa__number_of_bed_rooms__gte=number_of_bed_rooms)
            elif(search_property_categories[0].cat_key==TRADITIONAL_HOUSE_KEY):
                number_of_bed_rooms_search_object = Q(property__traditional_house__number_of_bed_rooms__gte=number_of_bed_rooms)
            elif(search_property_categories[0].cat_key==CONDOMINIUM_KEY):
                number_of_bed_rooms_search_object = Q(property__condominium__number_of_bed_rooms__gte=number_of_bed_rooms)
            elif(search_property_categories[0].cat_key==SHARE_HOUSE_KEY):
                number_of_bed_rooms_search_object = Q(property__share_house__number_of_bed_rooms_to_share__gte=number_of_bed_rooms)
            elif(search_property_categories[0].cat_key==APARTMENT_KEY):
                number_of_bed_rooms_search_object = Q(apartment_unit_listing__apartment_unit__number_of_bed_rooms__gte=number_of_bed_rooms)
            else:
                number_of_bed_rooms_search_object = Q()
                                                 

        #FILTER MAIN LISTING TABLE BASED ON THE QUERY PARAMETERS
        listings = list_models.MainListing.objects.filter(location_search_object,
                                                        number_of_bed_rooms_search_object,
                                                        listing_type__in=listing_types, 
                                                        property__property_category__in=search_property_categories,
                                                        property_price__gte=min_price,
                                                        listing_state = LISTING_STATE_ACTIVE,
                                                        is_expired=False,
                                                        is_approved=True,
                                                        ).filter(property_price__lte=max_price).order_by(order_by)
        # print("LISTINGS: ",listings)
        return listings


class PublicListingRetrieveView(generics.RetrieveAPIView):
    queryset = list_models.MainListing.objects.all()
    serializer_class = list_serializers.PublicListingDtailSerializer
    # pagination_class = PublicListingPagination
    # permission_classes = [IsAuthenticated,]


# class RetrieveApartmentUnitView(generics.RetrieveAPIView):
#     queryset = list_models.MainListing.objects.all()
#     serializer_class = list_serializers.PublicListingDtailSerializer


class SavedListingCreateView(generics.CreateAPIView):
    queryset = list_models.SavedListing.objects.all()
    serializer_class = list_serializers.SavedListingSerialier
    permission_classes = [IsAuthenticated,]

    def post(self, request, format=None):
        user = request.user
        if user.is_anonymous:
            return Response(data="You must signed in!", status=status.HTTP_401_UNAUTHORIZED)
        else:
            save_listing_serializer = list_serializers.SavedListingSerialier(data=request.data)
            if save_listing_serializer.is_valid():
                save_listing_serializer.save(user=user)
                return Response(data=save_listing_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data="Data is not valid!", status=status.HTTP_400_BAD_REQUEST)

class SavedListingDestroyView(generics.DestroyAPIView):
    queryset = list_models.SavedListing.objects.all()
    serializer_class = list_serializers.SavedListingSerialier
    permission_classes = [IsAuthenticated,]

    def delete(self, request, pk, format=None):
        user = request.user
        if user.is_anonymous:
            return Response(data="You must signed in!", status=status.HTTP_401_UNAUTHORIZED)
        else:
            list_models.SavedListing.objects.get(user=user.id, main_listing=pk).delete()
            return Response(data=None, status=status.HTTP_200_OK)

class SavedListingListView(generics.ListAPIView):
    queryset = list_models.SavedListing.objects.all()
    serializer_class = list_serializers.SavedListingListSerialier
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Response(data="You must signed in!", status=status.HTTP_401_UNAUTHORIZED)
        else:
            saved_listing_for_user = list_models.SavedListing.objects.filter(user=user.id).order_by("-saved_on")
            return saved_listing_for_user

class GetActiveFeaturePriceView(generics.RetrieveAPIView):
    queryset = list_models.FeaturePrice.objects.all()
    serializer_class = list_serializers.FeaturePriceSerialier
    permission_classes = [IsAuthenticated,]

    def get(self, request, format=None):
        active_feature_price_list = list_models.FeaturePrice.objects.filter(price_state=FEATURE_PRICE_ACTIVE)
        if active_feature_price_list.exists():
            active_feature_price = active_feature_price_list.order_by("-added_on")[0]

            return Response(data=list_serializers.FeaturePriceSerialier(active_feature_price).data, status=status.HTTP_200_OK)
        else:
            return Response(data="No active feature price", status=status.HTTP_404_NOT_FOUND)


class FeaturedListingCreateView(generics.CreateAPIView):
    queryset = list_models.FeaturedListing.objects.all()
    serializer_class = list_serializers.FeaturedListingSerialier
    permission_classes = [IsAuthenticated,]

    def post(self, request, format=None):

        print(request.data)

        active_feature_price_list = list_models.FeaturePrice.objects.filter(price_state=FEATURE_PRICE_ACTIVE)
        if active_feature_price_list.exists():
            active_feature_price = active_feature_price_list.order_by("-added_on")[0]
            # return Response(data="No active feature price", status=status.HTTP_404_NOT_FOUND)

            pm_key = request.data.get("payment[pm_key]")

            #==================COUPON================================================================
            coupon_payment_instance = None

            use_coupon = request.data.get("payment[coupon][use_coupon_payment]")
            feature_price = active_feature_price.price

            print("USE COUPOOOOOOOOOOOOOOOOOON: ", use_coupon)
            
            if use_coupon:
                coupon_code = request.data.get("payment[coupon][coupon_code]")
                try:
                    coupon_instance = pay_models.Coupon.objects.get(code=coupon_code)
                except ObjectDoesNotExist:
                    print(f"Coupon {coupon_code} not found!")
                    return Response(data=f"Coupon {coupon_code} not found!", status=status.HTTP_404_NOT_FOUND)
                paid_amount = None
                try:
                    if coupon_instance.current_value >= feature_price:
                        paid_amount = feature_price
                    else:
                        paid_amount = coupon_instance.current_value
                    coupon_payment_instance = pay_models.CouponPayment.objects.create(coupon=coupon_instance, paid_amount=paid_amount)
                    print("YOOOOOOOOO!!!!!: ",coupon_instance.current_value - paid_amount)
                    pay_models.Coupon.objects.filter(code=coupon_code).update(current_value=coupon_instance.current_value - paid_amount)
                    print("COUPON SAVED!!!!!!!!!")

                except:
                    print(f"Something went wrong during saving coupon payment!")
                    return Response(data=f"Something went wrong during saving coupon payment!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

            #==================PAYMENT================================================================

            payment = {}

            payment["payment_method"] = request.data.get("payment[payment_method]")
            payment["total_price"] = active_feature_price.price
            if coupon_payment_instance:
                payment["coupon_payment"] = coupon_payment_instance.id
            if pm_key == PM_CASH_PAYMENT or pm_key == PM_BANK_TRANSFER or pm_key == PM_MOBILE_PAYMENT:
                payment["is_approved"] = False
            else:
                payment["is_approved"] = True
            payment["narrative"] = request.data.get("payment[narrative]")

            payment_querydict = QueryDict("", mutable=True)
            payment_querydict.update(payment)

            payment_serializer = pay_serializers.PaymentSerializer(data=payment_querydict)
            if payment_serializer.is_valid():
                payment_instance = payment_serializer.save()
                print("PAYMENT SAVED!!!!!!!!!")
            else:
                print("Payment data is not valid!")
                return Response(data="Payment data is not valid!", status=status.HTTP_400_BAD_REQUEST)
        
            sub_payment_data = {}

            if pm_key == PM_BANK_TRANSFER:
                sub_payment_data["bank_name"] = request.data.get("payment[bank_transfer][bank_name]")
                sub_payment_data["bank_branch_name"] = request.data.get("payment[bank_transfer][bank_branch_name]")
                sub_payment_data["transaction_ref_number"] = request.data.get("payment[bank_transfer][transaction_ref_number]")
                sub_payment_data["payment_date"] = request.data.get("payment[bank_transfer][payment_date]")
                sub_payment_data["bank_full_address"] = request.data.get("payment[bank_transfer][bank_full_address]")


                bank_transfer_queridict = QueryDict("", mutable=True)
                bank_transfer_queridict.update(sub_payment_data)
                bank_transfer_serializer = pay_serializers.BankPaymentCreatBasicSerializer(data=bank_transfer_queridict)
                if bank_transfer_serializer.is_valid():
                    # print("BANK: YAYYYYYY! BANK IS VALID")
                    bank_transfer_instance = bank_transfer_serializer.save(payment=payment_instance)
                    print("BANK TRANSFER SAVED!!!!!!!!!")

                else:
                    print("Bank Payment data is not valid!")
                    return Response(data="Bank Payment data is not valid!", status=status.HTTP_400_BAD_REQUEST)


            if pm_key == PM_BANK_TRANSFER or pm_key == PM_MOBILE_PAYMENT:
                reciepts = request.data.getlist("reciept")

                
                for reciept in reciepts:
                    sub_payment = {"reciept": reciept}
                    sub_payment_querydict = QueryDict("", mutable=True)
                    sub_payment_querydict.update(sub_payment)

                    sub_payment_serializer = None
                    if pm_key == PM_BANK_TRANSFER:
                        sub_payment_serializer = pay_serializers.BankRecieptCreateBasicSerializer(data=sub_payment_querydict)
                        
                    else:
                        print("Bank Reciept is not valid!")
                        return Response(data="Bank Reciept is not valid!", status=status.HTTP_400_BAD_REQUEST)



                    if sub_payment_serializer.is_valid():
                        sub_payment_serializer.save(bank_payment=bank_transfer_instance)
                        print("Bank Reciept Saved!")
                    else:
                        print("Sub-payment data is not valid!")
                        return Response(data="Sub-payment data is not valid!", status=status.HTTP_400_BAD_REQUEST)

            
            main_listing = request.data.get("main_listing")
            print("=============>main_listing<====================: ", main_listing)
            featured_listing_dict = {"main_listing": main_listing}
            featured_listing_query_dict = QueryDict("", mutable=True)
            featured_listing_query_dict.update(featured_listing_dict)

            featured_listing_serializer = list_serializers.FeaturedListingSerialier(data=featured_listing_query_dict)

            if featured_listing_serializer.is_valid():
                featured_listing_instance = featured_listing_serializer.save(feature_price=active_feature_price,
                                                                             payment=payment_instance, 
                                                                             featured_listing_state=FEATURE_PRICE_ACTIVE)
                print("FEATURE LISTING SAVED!")
            
                return Response(data=f"Listing {main_listing} is featured!", status=status.HTTP_201_CREATED)
            else:
                print("INVALID FEATURE DATA!")
                return Response(data="Feature listing data is not valid!", status=status.HTTP_201_CREATED)
        return Response(data="No active feature price", status=status.HTTP_404_NOT_FOUND)


class FeaturedListingListView(generics.ListAPIView):
    queryset = list_models.FeaturedListing.objects.all()
    serializer_class = list_serializers.FeaturedListingWithMainListingDetailSerialier
    pagination_class = FeaturedListingPagination

    def get_queryset(self):
        location = self.request.query_params.get("location")
        print("location=========>: ",location)
        active_and_approved_featured_listings = list_models.FeaturedListing.objects.filter(
                                                    main_listing__property__address__city__name__icontains=location,
                                                    featured_listing_state=FEATURED_LISTING_ACTIVE, is_approved=True) \
                                                    .order_by("-featured_on")
        return active_and_approved_featured_listings


class ListingPropertyImagesListView(generics.ListAPIView):
    queryset = prop_models.PropertyImage.objects.all()
    serializer_class = prop_serializers.PropertyImageSerializer
    # pagination_class = FeaturedListingPagination

    def get(self, request, pk=None, format=None):
        # print("++++++======>PK======>++++++: ", pk)
        try:
            listing_instance = list_models.MainListing.objects.get(id=pk)
        except:
            return Response(data="Listing not found!", status=status.HTTP_404_NOT_FOUND)

        image_list = prop_models.PropertyImage.objects.filter(property=listing_instance.property.id)

        # print("HEYYYYYYYYYYYYYYYYY====================>: ",image_list)

        return Response(prop_serializers.PropertyImageSerializer(image_list, many=True, context={"request": request}).data, status=status.HTTP_200_OK)


class ListingPropertyVideoListView(generics.ListAPIView):
    queryset = prop_models.PropertyImage.objects.all()
    serializer_class = prop_serializers.PropertyVideoSerializer
    # pagination_class = FeaturedListingPagination

    def get(self, request, pk=None, format=None):
        # print("++++++======>PK======>++++++: ", pk)
        try:
            listing_instance = list_models.MainListing.objects.get(id=pk)
        except:
            return Response(data="Listing not found!", status=status.HTTP_404_NOT_FOUND)

        video_list = prop_models.PropertyVideo.objects.filter(property=listing_instance.property.id)

        # print("HEYYYYYYYYYYYYYYYYY====================>: ",video_list)

        return Response(prop_serializers.PropertyVideoSerializer(video_list, many=True, context={"request": request}).data, status=status.HTTP_200_OK)