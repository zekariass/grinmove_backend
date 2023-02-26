from django.contrib import admin
from subscriptions import models as sub_models

admin.site.register(sub_models.SubscriptionPlan)
admin.site.register(sub_models.Subscription)
admin.site.register(sub_models.SubscriptionHistory)
admin.site.register(sub_models.SubscriptionPayment)
admin.site.register(sub_models.SubscriptionDiscount)