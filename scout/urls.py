from django.conf.urls.defaults import patterns, url

from scout.views import WallView

urlpatterns = patterns('scout.views',
    url(r'^$', WallView.as_view(), name="scout_index"),
)
