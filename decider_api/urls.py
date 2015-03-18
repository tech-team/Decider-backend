from django.conf.urls import url, patterns
from decider_api.views import auth_views
from decider_api.views.user_data_views import UserDataEndpoint, UserEditEndpoint

urlpatterns = patterns('',
    url(r'^login/?$', auth_views.submit_login, name="submit_login"),
    url(r'^registration/?$', auth_views.submit_registration, name="submit_registration"),

    url(r'^user/(?P<user_id>[0-9]+)/?$', UserDataEndpoint.as_view()),
    url(r'^edit/?$', UserEditEndpoint.as_view()),

    url(r'^logout/?$', auth_views.logout_view, name="logout_view"),
)
