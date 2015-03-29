from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'decider_backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('decider_app.urls', namespace="decider_app")),
    url(r'^api/v1/', include('decider_api.urls', namespace="api")),
    url(r'^api/v1/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)