from locale import currency
from django.db import models
from django.utils import timezone
from commons import models as cmn_models
from agents import models as agnt_models
from payments import models as pay_models
from systems import models as sys_models


"""When subscribing to a system service, the user may choose from various subscription plans"""
class SubscriptionPlan(models.Model):
    periodicity = models.ForeignKey(cmn_models.Periodicity, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name="price plan", default=0.00)
    currency = models.ForeignKey(sys_models.Currency, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    class Meta:
        constraints =  [
            models.UniqueConstraint(fields = ['periodicity','price'], name = 'unique_subscription_plan')
        ]

    def __str__(self):
        return f"{self.currency.symbol} {self.price} {self.periodicity.period}"


"""A user may want to subscribe to system services for a period. The subscription allows the user 
    to get many services for a period with a single payment."""
class Subscription(models.Model):
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    agent = models.OneToOneField(agnt_models.Agent, on_delete=models.CASCADE, related_name="subscription")
    subscription_payment = models.OneToOneField(pay_models.Payment, on_delete=models.CASCADE)
    started_on = models.DateTimeField(default=timezone.now, editable=False)
    expired_on = models.DateTimeField(editable=True, null=False, blank=False)


"""It is important to retain the subscriptions of a user for future reporting purposes. 
    Subscription must have a single subscription for a specific user. Hence another 
        record is added to the subscription history table"""
class SubscriptionHistory(models.Model):
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    agent = models.OneToOneField(agnt_models.Agent, on_delete=models.CASCADE, related_name="subscription_history")
    subscription_payment = models.OneToOneField(pay_models.Payment, on_delete=models.CASCADE)
    started_on = models.DateTimeField(default=timezone.now, editable=False)
    expired_on = models.DateTimeField(editable=True, null=False, blank=False)
    
    @property
    def subscription_state (self):
        if self.expired_on > self.started_on:
            return "EXPIRED"
        else:
            return "ACTIVE"


"""If the user is already subscribed for a set of services, then this user will not be 
    asked for additional payment for using a service. But a new record will be created 
    by the system to relate subscription and payment for a service through subscription"""
class SubscriptionPayment(models.Model) :
    parent_payment = models.OneToOneField(pay_models.Payment, on_delete=models.CASCADE, related_name="parent_payment_record")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    paid_on = models.DateTimeField(default=timezone.now, editable=False)


"""A discount may apply to a specific subscription plan for promotional purposes"""
class SubscriptionDiscount(models.Model):
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    listing_param = models.ForeignKey(sys_models.ListingParameter, on_delete=models.CASCADE)
    discount_percentage = models.FloatField(verbose_name="discount in percent", default=0.00)
    discount_fixed = models.FloatField(verbose_name="fixed discount amount", default=0.00)
    description = models.TextField(blank=True, null=True)
    started_on = models.DateTimeField(default=timezone.now, editable=False)
    expired_on = models.DateTimeField(editable=True)

    def __str__(self):
        return "descount in percent: %d, discount in fixed amount: %d" % (self.discount_percentage, self.discount_fixed)