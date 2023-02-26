from rest_framework import serializers
from payments import models as pay_models

class PaymentApprovalModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.PaymentApprovalMode
        fields = "__all__"

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.PaymentMethod
        fields = "__all__"


class SupportedCardSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.SupportedCardScheme
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.Payment
        fields = "__all__"

#=============BANK PAYMENT=====================================
class BankPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.BankPayment
        fields = "__all__"

class BankPaymentCreatBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.BankPayment
        exclude = ("payment",)

class BankRecieptCreateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.BankReciept
        exclude = ("bank_payment",)

#================COUPON========================================
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = pay_models.Coupon
        fields = ("id","code","current_value","initial_value","redeemed_on","expire_on","is_active")