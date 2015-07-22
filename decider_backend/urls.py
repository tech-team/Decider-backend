from django.conf.urls import patterns, include, url
from django.contrib import admin
from decider_api.views.share_views import get_image_view
from decider_backend.settings import DEBUG, MEDIA_ROOT

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'decider_backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('decider_app.urls', namespace="decider_app")),
    url(r'^api/v1/', include('decider_api.urls', namespace="api")),
    url(r'^api/v1/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^push/', include('push_service.urls', namespace='push')),

    url(r'^question/(?P<question_id>[0-9]+)/?$', get_image_view, name='get_image'),
)


if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT,
        }),
    )