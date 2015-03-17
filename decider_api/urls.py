from django.conf.urls import url, patterns
from decider_api.views import auth_views
from decider_api.views.user_data_views import UserDataEndpoint

urlpatterns = patterns('',
    url(r'^login/', auth_views.submit_login, name="submit_login"),
    url(r'^registration/', auth_views.submit_registration, name="submit_registration"),

    url(r'^user/', UserDataEndpoint.as_view()),

    url(r'^logout/', auth_views.logout_view, name="logout_view"),
)
