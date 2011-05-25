from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

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

    objects = models.Manager()
    active = ActiveManager()
    inactive = InactiveManager()

    class Meta:
        abstract = True

###
# Actual Models
###

class Client(TimestampModel, ActiveModel):
    """
    Models a "client", basically provides
    a method to group projects.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="client-images/", max_length=255, 
                              blank=True, null=True)

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
    expected_status_code = models.SmallIntegerField(choices=HTTP_STATUS_CODES)
    display_order = models.SmallIntegerField(blank=True, null=True, 
                help_text="Used to define order of display.")

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return u"Test: %s" % self.url


class StatusChange(models.Model):
    """
    This is effectively our logging table; we only log
    errors as the rest can be considered to be expected
    returns. An error counts as any status code response
    which was not expected or no response at all.
    """
    EXPECTED = 'OK'
    UNEXPECTED = 'ERR'
    STATUS_CHOICES = (
        (EXPECTED, _('Expected')),        
        (UNEXPECTED, _('Unexpected')),        
    )

    test = models.ForeignKey('scout.StatusTest', related_name='status_changes')
    # Don't need date updated so we keep things lean here 
    # by not subclassing the Timestamp abstract model.
    returned_status = models.PositiveSmallIntegerField(choices=HTTP_STATUS_CODES)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __unicode__(self):
        return u"[%s] <%s> %s" % (self.date_added, self.get_status_display,
                                  self.test)

