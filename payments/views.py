from rest_framework import generics
from payments import models as pay_models
from payments import serializers as pay_serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status



class PaymentApprovalModeListView(generics.ListAPIView):
    queryset = pay_models.PaymentApprovalMode.objects.all()
    serializer_class = pay_serializers.PaymentApprovalModeSerializer
    # permission_classes = [IsAuthenticated,]

class PaymentMethodListView(generics.ListAPIView):
    queryset = pay_models.PaymentMethod.objects.all()
    serializer_class = pay_serializers.PaymentMethodSerializer
    # permission_classes = [IsAuthenticated,]

class SupportedCardSchemeListView(generics.ListAPIView):
    queryset = pay_models.SupportedCardScheme.objects.all()
    serializer_class = pay_serializers.SupportedCardSchemeSerializer
    # permission_classes = [IsAuthenticated,]

#=============COUPON======================================================
class CouponRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = pay_models.Coupon.objects.all()
    serializer_class = pay_serializers.CouponSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = "code"

    def get(self, request, **kwargs):
        coupon_code = request.query_params.get("code")
        # print("coupon_code: ", coupon_code)

        try:
            coupon_instance = pay_models.Coupon.objects.get(code=coupon_code)
        except ObjectDoesNotExist:
            return Response(data="Coupon does not exist!", status=status.HTTP_404_NOT_FOUND)

        return Response(data=self.get_serializer(coupon_instance).data, status=status.HTTP_200_OK)

    