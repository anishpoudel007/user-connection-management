from django.contrib.auth import get_user_model
from django.db import models
from connections.models import Connection

User = get_user_model()


class Notification(models.Model):
    class Type(models.TextChoices):
        connection_request = "connection_request", "Connection Request"
        connection_accepted = "connection_accepted", "Connection Accepted"
        connection_rejected = "connection_rejected", "Connection Rejected"

    type = models.CharField(max_length=30, choices=Type.choices)
    message = models.TextField()
    connection = models.ForeignKey(
        Connection, on_delete=models.CASCADE, related_name="connections"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipients"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="senders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
