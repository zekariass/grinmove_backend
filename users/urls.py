from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.MyHomeUserListCreateView.as_view(), name='user-signup'),
    path('list/', views.MyHomeUserListCreateView.as_view(), name='user-list'),
    path('detail/', views.MyHomeUserDetailUpdateView.as_view(), name='user-detail'),
    path('<int:pk>/update/', views.MyHomeUserDetailUpdateView.as_view(), name='user-update')
]