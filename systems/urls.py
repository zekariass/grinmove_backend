from django.urls import path
from systems import views

urlpatterns = [
    path("systemparameters/", views.SystemParameterListView.as_view(), name="system-parameters" ),
    path("listingparameters/", views.ListingParameterListView.as_view(), name="listing-parameters" ),
    path("currency/list/", views.CurrencyListView.as_view(), name="currency-list" ),

    #SYSTEM ASSETS
    path("asset/list/", views.SystemAssetListCreateView.as_view(), name="system-asset-list" ),
]