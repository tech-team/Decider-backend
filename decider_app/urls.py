from django.conf.urls import patterns, url

from decider_app.views import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name="index_view"),

    url(r'^login/$', views.login_view, name="login_view"),
    url(r'^vk_login/$', views.vk_login_view, name="vk_login_view"),
    url(r'^registration/$', views.registration_view, name="registration_view"),
)
