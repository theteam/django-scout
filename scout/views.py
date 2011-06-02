from django.views.generic import ListView

from scout.models import Project

class WallView(ListView):

    model = Project
    template_name = 'scout/wall.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.active.all().order_by('-working')

    def get_context_data(self, **kwargs):
        context = super(WallView, self).get_context_data(**kwargs)
        try:
            last_update = Project.active.all()\
                            .order_by('-date_updated')[0].date_updated
        except IndexError:
            last_update = None
        context['last_update'] = last_update
        return context
