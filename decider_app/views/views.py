from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods


@login_required(login_url="/login/")
def index_view(request):
    return render(request, "index.html")


@require_http_methods(['GET'])
def vk_login_view(request):
    return render(request, 'vk_login.html')


@require_http_methods(['GET'])
def login_view(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'login.html', c)


@require_http_methods(['GET'])
def registration_view(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'registration.html', c)