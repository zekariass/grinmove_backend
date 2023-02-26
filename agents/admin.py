from django.contrib import admin
from agents import models as agnt_models

admin.site.register(agnt_models.AgentLogo)
admin.site.register(agnt_models.Agent)
admin.site.register(agnt_models.AgentAdmin)
admin.site.register(agnt_models.AgentMessagePreference)
admin.site.register(agnt_models.Message)
