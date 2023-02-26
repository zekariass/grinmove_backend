from agents import models as agent_models
from django.core.exceptions import ObjectDoesNotExist
from listings import models as list_models

class ListingQuerysetMixin():
    def get_queryset(self):
        user = self.request.user
        try:
            currentAgentAdmin = agent_models.AgentAdmin.objects.get(admin=user)
        except ObjectDoesNotExist:
            return None
        
        listings = list_models.MainListing.objects.filter(agent=currentAgentAdmin.agent)
        return listings
