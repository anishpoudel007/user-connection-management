from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Connection(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    user_1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="connection_from"
    )
    user_2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="connection_to"
    )
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_1", "user_2"], name="unique_connection_pair"
            )
        ]

    def __str__(self):
        return f"{self.user_1} <=> {self.user_2}"
