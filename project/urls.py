from django.urls import path, include
from rest_framework import routers

from connections.views import UserConnectionRequestUpdateView, UserConnectionRequestView
from user.views import (
    TestView,
    UserLoginView,
    UserRegisterView,
    UserSearchView,
    UserViewSet,
)


router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/auth/register", UserRegisterView.as_view(), name="user-register"),
    path("api/auth/login", UserLoginView.as_view(), name="user-login"),
    path("api/test-view", TestView.as_view(), name="test-view"),
    path("api/search-users", UserSearchView.as_view(), name="user-search-view"),
    path(
        "api/connection-request",
        UserConnectionRequestView.as_view(),
        name="user-connection-request",
    ),
    path(
        "api/connection-request/<int:connection_id>",
        UserConnectionRequestUpdateView.as_view(),
        name="user-connection-request-update",
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
