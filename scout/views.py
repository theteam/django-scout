from django.views.generic import ListView

from scout.models import Project

class WallView(ListView):

    model = Project
    template_name = 'scout/wall.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.active.all().order_by('-working')
