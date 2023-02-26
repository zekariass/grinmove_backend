from django.contrib import admin
from commons import models as cmn_models


admin.site.register(cmn_models.Country)
admin.site.register(cmn_models.Region)
admin.site.register(cmn_models.City)
admin.site.register(cmn_models.Address)
admin.site.register(cmn_models.Periodicity)