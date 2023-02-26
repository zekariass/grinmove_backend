from django.contrib import admin
from systems import models

admin.site.register(models.SystemRating)
admin.site.register(models.SystemFeedback)
admin.site.register(models.ListingParameter)
admin.site.register(models.SystemAsset)
admin.site.register(models.SystemAssetOwner)
admin.site.register(models.SystemParameter)
admin.site.register(models.Currency)