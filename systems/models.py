from asyncio import constants
from django.db import models
from django.utils import timezone
import os
from django.conf import settings

"""Users can give ratings of their user experience about the system by number rating"""
class SystemRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="system_ratings")
    rating = models.IntegerField(verbose_name="System rating value", default=0)
    rated_on = models.DateTimeField(default=timezone.now, editable=False)

"""Users can write any feedback about the system. Feedback is a comment about their user experience of the system. 
    It allows to improve the system with additional features or modify the existing one"""
class SystemFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="system_feedbacks")
    feedback = models.TextField(verbose_name="System feedback")
    rated_on = models.DateTimeField(default=timezone.now, editable=False)


def get_system_asset_path(instance, filename):
    now = timezone.now()
    basename, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond//1000
    return f"systems/assets/{instance.owner.name}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


"""System assets may be owned by a specific page or module"""
class SystemAssetOwner(models.Model):
    SYSTEM_ASSET_OWNER_NAMES = [
        ("APARTMENT_PICTURE", "Apartment Picture"),
        ("VILLA_PICTURE", "Villa Picture"),
        ("CONDOMINIUM_PICTURE", "Condominium Picture"),
        ("TRADITIONAL_HOUSE_PICTURE", "Traditional House Picture"),
        ("SHARE_HOUSE_PICTURE", "Share House Picture"),
        ("COMMERCIAL_PROPERTY_PICTURE", "Commercial Property Picture"),
        ("OFFICE_PICTURE", "Office Picture"),
        ("HALL_PICTURE", "Hall Picture"),
        ("LAND_PICTURE", "Land Picture"),
        ("ALL_PURPOSE_PROPERTY_PICTURE", "All Purpose Property Picture"),
       ("LANDING_PAGE_SLIDER", "Landing Page Slider"),
    ]
    # asset = models.ManyToManyField(SystemAsset, verbose_name="system asset")
    name = models.CharField(verbose_name="name of owner of asset, (i.e. page, component)", choices=SYSTEM_ASSET_OWNER_NAMES, unique=True, max_length=250)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

"""The system may be configurable with a variety of assets, such as pictures for logo, slider, etc"""
class SystemAsset(models.Model):
    owner = models.ForeignKey(SystemAssetOwner, on_delete=models.CASCADE, related_name="assets")
    name = models.CharField(verbose_name="system asset name", max_length=50, blank=True, null=True)
    asset = models.FileField(verbose_name="asset file path", upload_to=get_system_asset_path)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Owner: %s, path: %s" % (self.owner.name, self.name)


"""There might be a variety of parameters we may store so that the system can use them for doing 
    some functionality with it during the listing, such as promotional parameters"""
class ListingParameter(models.Model):

    PARAMETERS = [
        ("NEW_AGENT_PROMOTION", "New Agent Promotion"),
       ("HOLIDAY_PROMOTION", "Holiday Promotion"),
    ]

    APPLIED_TO_OPTIONS = [
        ("SUBSCRIPTION", "Subscription"),
       ("PAY_PER_LISTING", "Pay-per-listing"),
       ("BOTH", "Subscription and Pay-per-listing"),
    ]

    VALUE_OPTIONS = [
        ("DAYS", "Days"),
       ("LISTING_COUNT", "Listing Count"),
    ]

    name = models.CharField(verbose_name="listing parameter name", choices=PARAMETERS, default=PARAMETERS[0][0], max_length=100)
    # value = models.CharField(verbose_name="Listing parameter value", max_length=100, default="")
    value_type = models.CharField(verbose_name="Listing parameter value Type", max_length=100, choices=VALUE_OPTIONS, default=VALUE_OPTIONS[0][0])
    applied_to = models.CharField(verbose_name="Which payment type to apply to", choices=APPLIED_TO_OPTIONS, max_length=50, default=APPLIED_TO_OPTIONS[0][0])
    description = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "value_type", "applied_to"], name="Listing_parameter_unique_constraint")
        ]

    def __str__(self):
        return f"{self.name}, {self.applied_to}, {self.value_type} "


"""System parameters are parameters used by the system for different purposes. Parameters are values that the system 
    use to function well, such as folder names, password length, password expiry age, etc"""
class SystemParameter(models.Model):
    name = models.CharField(verbose_name="system parameter name", unique=True, blank=False, null=False, max_length=100)
    value = models.CharField(verbose_name="system parameter value", max_length=100, default="")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(verbose_name="Currency name", max_length=20, default="Birr")
    numeric_code = models.CharField(verbose_name="Numeric code of the currency", max_length=5, default=230)
    symbol = models.CharField(verbose_name="Symbol of the currency", max_length=10, default="Br")
    added_on = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name
