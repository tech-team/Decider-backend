# coding=utf-8
import httplib
import urllib
import urllib2
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

import json
import requests
from decider_app.models import User
from decider_app.views.utils.auth_helper import build_token_request_data, get_token_url
from decider_app.views.utils.response_builder import build_response, build_error_response
from decider_api.log_manager import logger
from decider_app.views.utils.response_codes import CODE_OK, CODE_INVALID_LOGIN, CODE_LOGIN_FAILED, \
    CODE_INSUFFICIENT_LOGIN, CODE_EMAIL_TAKEN, CODE_CREATED, CODE_REGISTRATION_FAILED


def get_token_data(email, password):
    try:
        post_data = urllib.urlencode(build_token_request_data(email, password))
        token_response = urllib2.urlopen(urllib2.Request(get_token_url(), data=post_data))
        token_data = json.loads(token_response.read())
        if not token_data:
            return False

        data = {
            'access_token': token_data.get('access_token'),
            'expires': token_data.get('expires_in'),
            'refresh_token': token_data.get('refresh_token')
        }
        return data
    except Exception as e:
        logger.exception(e)
        return False

@require_http_methods(['POST'])
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email and password:
        user = authenticate(email=email, password=password)
        if not user:
            return build_error_response(httplib.FORBIDDEN, CODE_INVALID_LOGIN, 'Invalid email/password')
        else:
            data = get_token_data(email, password)
            if not data:
                return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_LOGIN_FAILED, "Login failed")
            else:
                return build_response(httplib.OK, CODE_OK, "Login successful", data)
    else:
        return build_error_response(httplib.BAD_REQUEST, CODE_INSUFFICIENT_LOGIN, 'Some fields are not filled')


@require_http_methods(['POST'])
def registration(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email and password:
        try:
            user = User.objects.get(email=email)
            if user:
                return build_error_response(httplib.FORBIDDEN, CODE_EMAIL_TAKEN, "Email is taken")
        except User.DoesNotExist:
            user = User.objects.create(email=email)
            user.set_password(request.POST.get("password"))
            user.save()

            data = get_token_data(email, password)
            if not data:
                return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_REGISTRATION_FAILED, "Registration failed")
            else:
                return build_response(httplib.CREATED, CODE_CREATED, "Registration successful", data)
    else:
        return build_error_response(httplib.BAD_REQUEST, CODE_INSUFFICIENT_LOGIN, 'Some fields are not filled')


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/login/')
