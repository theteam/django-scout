from django.db import models

from scout.managers import ActiveManager, InactiveManager

###
# Abstract Base classes
###

class TimestampModel(models.Model):
    """
    A short mixin abstract class for adding 
    update and creation timestamp fields.
    """
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class ActiveModel(models.Model):
    """
    A mixin abstract class to provide functionality
    for marking specific rows as active or inactive and
    creating the relevant managers to allow for simple
    use via the ORM.
    """
    is_active = models.BooleanField(default=True)

    objects = models.Manager
    active = ActiveManager()
    inactive = InactiveManager()

    class Meta:
        abstract = True


class Client(models.Model):
    """
    Models a "client", basically provides
    a method to group projects.
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Project(models.Model):
    """
    Models a project, something which tests
    can be attached to.
    """
    name = models.CharField(max_length=255)
