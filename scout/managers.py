from django.db import models


class ActiveManager(models.Manager):

    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(is_active=True)

class InactiveManager(models.Manager):

    def get_query_set(self):
        return super(InactiveManager, self).get_query_set().filter(is_active=False)
