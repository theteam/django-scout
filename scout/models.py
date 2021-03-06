from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from scout.choices import HTTP_STATUS_CODES
from scout.managers import (ClientActiveManager, ProjectActiveManager, 
                            StatusTestActiveManager)

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

    objects = models.Manager()
    active = ClientActiveManager()

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
    # This is a denormalized cached field to store the 
    # current status of the project (whether it's child
    # tests are passing or not)
    working = models.BooleanField(default=True)

    objects = models.Manager()
    active = ProjectActiveManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def last_log(self):
        """Returns the latest StatusChange for any test
        underneath this project. Caches state.
        """
        if hasattr(self, '_last_log'):
            return self._last_log
        else:   
            try:
                status_log = StatusChange.objects.filter(test__project=self)\
                                .order_by('-date_added')[0]
            except IndexError:
                status_log = None
        self._last_log = status_log
        return self._last_log

class StatusTest(TimestampModel, ActiveModel):
    """Represents one test which is linked to a project;
    this allows us to ping more than one URL per project 
    but also allows us to attach notification options to
    a specfic instance of a test allowing them to be
    more granular.
    """

    project = models.ForeignKey('scout.Project', related_name='tests')
    url = models.URLField(max_length=255, verify_exists=False) 
    expected_status = models.SmallIntegerField(choices=HTTP_STATUS_CODES)
    display_order = models.SmallIntegerField(blank=True, null=True, 
                help_text="Used to define order of display.")

    objects = models.Manager()
    active = StatusTestActiveManager()

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return u"Test: %s" % self.url

    def last_log(self):
        """Returns the latest StatusChange for this test,
        if available - else None. Caches state.
        """
        if hasattr(self, '_last_log'):
            return self._last_log
        else:   
            try:
                status_log = self.status_changes.all().order_by('-date_added')[0]
            except IndexError:
                status_log = None
        self._last_log = status_log
        return self._last_log


class StatusChange(models.Model):
    """This is effectively our logging table; we only log
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

    test = models.ForeignKey('scout.StatusTest', 
                             related_name='status_changes')
    # We log the expected status here rather than relying on what the 
    # StatusTest's version is currently set to as that is not guaranteed 
    # to be the same.
    expected_status = models.SmallIntegerField(choices=HTTP_STATUS_CODES)
    # As we might not even get a response, the returned_status field is
    # nullable so that we have some of showing that.
    returned_status = models.PositiveSmallIntegerField(
                        choices=HTTP_STATUS_CODES, null=True, blank=True)
    result = models.CharField(max_length=3, choices=STATUS_CHOICES)
    # Don't need date updated so we keep things lean here 
    # by not subclassing the Timestamp abstract model.
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __unicode__(self):
        return u"Status Log %s" % (self.pk)

    def is_error(self):
        """Returns True if this log should be considered as an
        unwanted occurance; allows us to do this in a centralised 
        place so we don't have to constantly check with conditionals 
        everywhere.
        """
        if self.result != self.EXPECTED:
            return True
        return False

