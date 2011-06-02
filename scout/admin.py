from django.contrib import admin

from scout.models import Client, Project, StatusTest, StatusChange

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
    list_display = ['name', 'client', 'description', 'working']
    list_filter = ['client']
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['working']
    search_fields = ['name']


class StatusChangeAdmin(admin.ModelAdmin):
    list_display = ['test', 'expected_status', 'returned_status', 'result']


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(StatusChange, StatusChangeAdmin)
