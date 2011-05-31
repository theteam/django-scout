from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('scout.views',
    url(r'^$', 'index', name="scout_index"),
)
