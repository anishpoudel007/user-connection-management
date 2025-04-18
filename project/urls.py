from django.urls import path, include
from user.models import User
from user.serializer import UserViewSet
from rest_framework import routers

from user.views import UserRegister


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register("users", UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/register", UserRegister.as_view(), name="user-register"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
