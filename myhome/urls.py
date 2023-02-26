"""myhome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users import urls as user_urls
from agents import urls as agent_urls
from commons import urls as cmn_urls
from properties import urls as prop_urls
from systems import urls as sys_urls
from listings import urls as list_urls
from payments import urls as pay_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(user_urls)),
    path('agent/', include(agent_urls)),
    path('common/', include(cmn_urls)),
    path('property/', include(prop_urls)),
    path('system/', include(sys_urls)),
    path('listing/', include(list_urls)),
    path('payment/', include(pay_urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
