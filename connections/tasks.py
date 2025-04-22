from celery import shared_task
from django.contrib.auth import get_user_model

from connections.models import Connection
from notification.models import Notification


User = get_user_model()


@shared_task
def send_connection_notification(connection_id, sender_id, status):
    try:
        connection = Connection.objects.get(id=connection_id)
        sender = User.objects.get(id=sender_id)

        if status == Connection.Status.ACCEPTED:
            notif_type = Notification.Type.connection_accepted
            recipient = connection.user_1
            message = f"{connection.user_2.username} accepted your connection request."
        elif status == Connection.Status.REJECTED:
            notif_type = Notification.Type.connection_rejected
            recipient = connection.user_1
            message = f"{connection.user_2.username} rejected your connection request."
        else:
            return

        Notification.objects.create(
            recipient=recipient,
            sender=sender,
            type=notif_type,
            message=message,
            connection=connection,
        )
    except (Connection.DoesNotExist, User.DoesNotExist):
        pass
