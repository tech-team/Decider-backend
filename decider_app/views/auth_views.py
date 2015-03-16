# coding=utf-8
import urlparse
import urllib
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import json
import requests
from decider_app.models import User
from decider_app.views.utils.auth_helper import build_token_request_data
from decider_app.views.utils.response_builder import TOKEN_URL, build_ok_response, build_403_response, \
    build_402_response, build_501_response
from decider_backend.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, HOST_ADDRESS, HOST_SCHEMA, HOST_PORT


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


@require_http_methods(['POST'])
def submit_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email and password:
        user = authenticate(email=email, password=password)
        if not user:
            error_text = 'Invalid email/password'
            return HttpResponse(build_402_response(error_text), content_type="application/json")
        else:
            post_data = build_token_request_data(email, password)
            token_data = json.loads(requests.post(TOKEN_URL, data=post_data).content)

            return HttpResponse(build_ok_response(token_data), content_type="application/json")
    else:
        error_text = 'Some fields are not filled'
        return HttpResponse(build_403_response(error_text), content_type="application/json")


@require_http_methods(['POST'])
def submit_registration(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if username and email and password:
        try:
            user = User.objects.get(email=email)
            if user:
                error_text = "That email is taken"
                return HttpResponse(build_402_response(error_text), content_type="application/json")
        except User.DoesNotExist:
            user = User.objects.create(email=email, username=username)
            user.set_password(request.POST.get("password"))
            user.save()

            post_data = build_token_request_data(email, password)
            token_data = json.loads(requests.post(TOKEN_URL, data=post_data).content)

            if not token_data.get('error'):
                return HttpResponse(build_ok_response(token_data), content_type="application/json")
            else:
                error_text = 'Failed to save user'
                return HttpResponse(build_501_response(error_text), content_type="application/json")
    else:
        error_text = 'Some fields are not filled'
        return HttpResponse(build_403_response(error_text), content_type="application/json")


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/login/')
