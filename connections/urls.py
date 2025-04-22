from django.urls import path

from connections.views import UserConnectionRequestUpdateView, UserConnectionRequestView

urlpatterns = [
    path(
        "",
        UserConnectionRequestView.as_view(),
        name="user-connection-request",
    ),
    path(
        "<int:connection_id>/",
        UserConnectionRequestUpdateView.as_view(),
        name="user-connection-request-update",
    ),
]
