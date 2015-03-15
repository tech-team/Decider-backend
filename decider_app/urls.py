from django.conf.urls import patterns, url
from decider_app.views import views, auth_views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name="index_view"),

    url(r'^login/$', auth_views.login_view, name="login_view"),
    url(r'^submit_login/$', auth_views.submit_login, name="submit_login"),
    url(r'^registration/$', auth_views.registration_view, name="registration_view"),
    url(r'^submit_registration/$', auth_views.submit_registration, name="submit_registration"),

    url(r'^logout/$', auth_views.logout_view, name="logout_view"),
)
