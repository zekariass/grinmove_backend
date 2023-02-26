from django.urls import path
from payments import views

urlpatterns = [
    path("paymentapprovalmode/list/", views.PaymentApprovalModeListView.as_view(), name="paymentapprovalmode-list"),
    path("paymentmethod/list/", views.PaymentMethodListView.as_view(), name="paymentmethod-list"),
    path("supportedcardscheme/list/", views.SupportedCardSchemeListView.as_view(), name="supportedcardscheme-list"),

    #===============COUPON=========================================
    # path("coupon/<slug:code>/detail/", views.CouponRetrieveUpdateDestroyView.as_view(), name="coupon-detail"),
    path("coupon/detail/", views.CouponRetrieveUpdateDestroyView.as_view(), name="coupon-detail"),

]