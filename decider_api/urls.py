from django.conf.urls import url, patterns, include
from decider_api.views import auth_views
from decider_api.views.user_data_views import UserDataEndpoint, UserEditEndpoint

urlpatterns = patterns('',
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url(r'^login/?$', auth_views.login, name="login"),
    url(r'^registration/?$', auth_views.registration, name="registration"),

    url(r'^user/(?P<user_id>[0-9]+)/?$', UserDataEndpoint.as_view()),
    url(r'^edit/?$', UserEditEndpoint.as_view()),

    url(r'^logout/?$', auth_views.logout_view, name="logout_view"),
)
