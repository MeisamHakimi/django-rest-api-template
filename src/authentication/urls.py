from django.urls import path
from rest_framework_simplejwt import views as jwt_views
# from .views import (
# )

app_name = "auth"

urlpatterns = [
    # Token
    path("token/refresh", jwt_views.TokenRefreshView.as_view(), name="token-refresh"),
    
]
