from django.urls import path

from auth.apis.views.auth_login_views import LoginAPIView, RefreshTokenAPIView

urlpatterns = [
    path("token/", LoginAPIView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", RefreshTokenAPIView.as_view(), name="token_refresh"),
]
