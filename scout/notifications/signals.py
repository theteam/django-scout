from scout.notifications.models import NotificationProfile


def create_notification_profile(sender, instance, created, using, **kwargs):
    """Attaches a new notification profile
    to a newly created django.auth User.
    """
    if created:
        data = {'user': instance}
        profile = NotificationProfile.objects.create(**data)
