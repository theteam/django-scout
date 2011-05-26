from django.contrib import admin

from scout.models import Client, Project, StatusTest

class ClientAdmin(admin.ModelAdmin):
    date_heirarchy = 'date_added'
    list_display = ['name', 'slug', 'description', 'image']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class StatusTestAdminInline(admin.TabularInline):
    model = StatusTest
    extra = 3


class ProjectAdmin(admin.ModelAdmin):
    date_heirarchy = 'date_added'
    inlines = [StatusTestAdminInline]
    list_display = ['name', 'client', 'description']
    list_filter = ['client']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
