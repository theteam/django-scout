from django.db import models
from django.template.defaultfilters import slugify

from scout.choices import HTTP_STATUS_CODES
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


class Client(TimestampModel, ActiveModel):
    """
    Models a "client", basically provides
    a method to group projects.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Client, self).save(*args, **kwargs)


class Project(TimestampModel, ActiveModel):
    """
    Models a project, something which tests
    can be attached to.
    """
    client = models.ForeignKey('scout.Client', related_name='projects')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)


class StatusTest(TimestampModel, ActiveModel):
    """
    Represents one test which is linked to a project;
    this allows us to ping more than one URL per
    project but also allows us to attach notification
    options to a specfic instance of a test allowing
    them to be more granular.
    """

    project = models.ForeignKey('scout.Project', related_name='tests')
    url = models.URLField(max_length=255, verify_exists=False) 
    expected_status =  models.PositiveSmallIntegerField(choices=HTTP_STATUS_CODES)

    def __unicode__(self):
        return u"Test: %s" % self.url
