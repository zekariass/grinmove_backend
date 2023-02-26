from django.contrib import admin
from payments import models as pymnt_models

admin.site.register(pymnt_models.PaymentApprovalMode)
admin.site.register(pymnt_models.PaymentMethod)
admin.site.register(pymnt_models.PaymentMethodDiscount)
admin.site.register(pymnt_models.Payment)
# admin.site.register(pymnt_models.PaymentByMethod)
admin.site.register(pymnt_models.BankPayment)
admin.site.register(pymnt_models.BankReciept)
admin.site.register(pymnt_models.MobilePayment)
admin.site.register(pymnt_models.MobilePayReciept)
admin.site.register(pymnt_models.SupportedCardScheme)
admin.site.register(pymnt_models.CreditCardPayment)
admin.site.register(pymnt_models.CashPayment)
admin.site.register(pymnt_models.Coupon)
admin.site.register(pymnt_models.CouponPayment)
# admin.site.register(pymnt_models.AppliedCoupon)