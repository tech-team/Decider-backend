# coding=utf-8
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods

import json
import requests
from decider_app.models import User
from decider_app.views.utils.auth_helper import build_token_request_data
from decider_app.views.utils.response_builder import TOKEN_URL, build_ok_response, build_403_response, \
    build_402_response, build_501_response


@require_http_methods(['POST'])
def submit_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email and password:
        user = authenticate(email=email, password=password)
        if not user:
            error_text = 'Invalid email/password'
            return build_402_response(error_text)
        else:
            post_data = build_token_request_data(email, password)
            token_data = json.loads(requests.post(TOKEN_URL, data=post_data).content)
            data = {
                'access_token': token_data.get('access_token'),
                'expires': token_data.get('expires_in'),
                'refresh_token': token_data.get('refresh_token')
            }
            return build_ok_response(data)
    else:
        error_text = 'Some fields are not filled'
        return build_403_response(error_text)


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
                return build_402_response(error_text)
        except User.DoesNotExist:
            user = User.objects.create(email=email, username=username)
            user.set_password(request.POST.get("password"))
            user.save()

            post_data = build_token_request_data(email, password)
            token_data = json.loads(requests.post(TOKEN_URL, data=post_data).content)

            if not token_data.get('error'):
                data = {
                    'access_token': token_data.get('access_token'),
                    'expires': token_data.get('expires_in'),
                    'refresh_token': token_data.get('refresh_token')
                }
                return build_ok_response(data)
            else:
                error_text = 'Failed to save user'
                return build_501_response(error_text)
    else:
        error_text = 'Some fields are not filled'
        return build_403_response(error_text)


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/login/')
