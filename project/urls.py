from django.urls import path, include
from rest_framework import routers

from user.views import UserLoginView, UserRegisterView, UserViewSet


router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/register", UserRegisterView.as_view(), name="user-register"),
    path("api/auth/login", UserLoginView.as_view(), name="user-login"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
