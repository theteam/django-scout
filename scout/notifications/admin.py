from django.contrib import admin

from scout.notifications.models import NotificationProfile


class NotificationProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_email', 'mobile_number']

admin.site.register(NotificationProfile, NotificationProfileAdmin)
