from django.conf.urls import patterns, url
from push_service.views import PushAuthEndpoint, PushUnauthEndpoint, PushSubEndpoint, PushUnsubEndpoint

urlpatterns = patterns('',
    url(r'^auth/?$', PushAuthEndpoint.as_view(), name="auth"),
    url(r'^unauth/?$', PushUnauthEndpoint.as_view(), name="unauth"),

    url(r'^sub/?$', PushSubEndpoint.as_view(), name="sub"),
    url(r'^unsub/?$', PushUnsubEndpoint.as_view(), name="unsub"),
)
