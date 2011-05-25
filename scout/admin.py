from django.contrib import admin

from scout.models import Client, Project, StatusTest

class ClientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, ClientAdmin)
