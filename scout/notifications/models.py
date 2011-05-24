from django.db import models


class NotificationProfile(models.Model):
    """
    This provides a profile coupled to a django.auth User
    which allows us to set various notifcation options and values.
    """
    user = models.OneToOneField('auth.User', related_name='notification_profile')
    notification_email = models.EmailField(blank=True, max_length=255)
    mobile_number = models.CharField(blank=True, max_length=20)

    @property
    def email(self):
        """
        Returns notication_email if set, else the normal auth.User
        email field; this allows a user to keep their notification 
        email seperate from their registered email. Caches the email
        on the instance once calculated.
        """
        if self._email:
            return self._email
        else:
            if self.notification_email:
                self._email = self.notification_email
            else:
                self._email = self.user.email
            return self._email
