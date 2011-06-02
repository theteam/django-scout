from django.db import models


class ClientActiveManager(models.Manager):

    def get_query_set(self):
        """Retrieves all clients that are active.
        """
        return super(ClientActiveManager, self).get_query_set().\
                filter(is_active=True)


class ProjectActiveManager(models.Manager):

    def get_query_set(self):
        """Retrieves all projects that are active and have active
        parent clients.
        """
        return super(ProjectActiveManager, self).get_query_set().\
                filter(is_active=True,
                       client__is_active=True)


class StatusTestActiveManager(models.Manager):

    def get_query_set(self):
        """Retrieves all test that are active and have active parent projects
        AND active parent clients.
        """
        return super(StatusTestActiveManager, self).get_query_set()\
                .filter(is_active=True,
                        project__is_active=True,
                        project__client__is_active=True)
