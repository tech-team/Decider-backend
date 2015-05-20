# coding=utf-8
import httplib
import urllib
import urllib2
import uuid
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

import json
from decider_app.models import User, SocialSite
from decider_app.views.utils.auth_helper import build_token_request_data, get_token_url
from decider_app.views.utils.response_builder import build_response, build_error_response
from decider_api.log_manager import logger
from decider_app.views.utils.response_codes import CODE_OK, CODE_INVALID_CREDENTIALS, CODE_LOGIN_FAILED, \
    CODE_INSUFFICIENT_CREDENTIALS, CODE_UNKNOWN_SOCIAL


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
def login_view(request):
    email = request.POST.get('email')

    social_name = request.POST.get('social_name')
    social_id = request.POST.get('social_id')

    password = request.POST.get('password')
    if password and (email or social_name and social_id):
        if email:
            user = authenticate(email=email, password=password)
        else:
            social_name = str(social_name)
            social_id = str(social_id)
            try:
                social_site = SocialSite.objects.get(name=social_name)
            except SocialSite.DoesNotExist:
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_SOCIAL,
                                            'Unknown social site')

            user = authenticate(social_id=social_id, social_site=social_site,
                                password=password)

        if not user:
            return build_error_response(httplib.FORBIDDEN, CODE_INVALID_CREDENTIALS, 'Invalid credentials')
        else:
            data = get_token_data(user.email, password)
            if not data:
                return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_LOGIN_FAILED, "Login failed")
            else:
                data.update({'uid': user.uid})
                return build_response(httplib.OK, CODE_OK, "Login successful", data)
    else:
        return build_error_response(httplib.BAD_REQUEST, CODE_INSUFFICIENT_CREDENTIALS, 'Some fields are not filled')


@require_http_methods(['POST'])
def registration_view(request):
    email = request.POST.get('email')

    social_name = request.POST.get('social_name')
    social_id = request.POST.get('social_id')

    password = request.POST.get('password')
    if password and (email or social_name and social_id):
        if email:
            try:
                User.objects.get(email=email)

            except User.DoesNotExist:
                user = User(email=email, uid=uuid.uuid4().hex)
                user.set_password(password)
                user.save()

            user = authenticate(email=email, password=password)
        else:
            social_name = str(social_name)
            social_id = str(social_id)
            try:
                social_site = SocialSite.objects.get(name=social_name)
            except SocialSite.DoesNotExist:
                return build_error_response(httplib.NOT_FOUND, CODE_UNKNOWN_SOCIAL,
                                            'Unknown social site')

            try:
                User.objects.get(social_id=social_id, social_site=social_site)

            except User.DoesNotExist:
                user = User(social_id=social_id, social_site=social_site,
                            uid=uuid.uuid4().hex)
                user.email = user.uid
                user.set_password(password)
                user.save()

            user = authenticate(social_id=social_id, social_site=social_site,
                                password=password)
        if not user:
            return build_error_response(httplib.FORBIDDEN, CODE_INVALID_CREDENTIALS,
                                        "Invalid credentials")

        data = get_token_data(user.email, password)
        if not data:
            return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_LOGIN_FAILED, "Registration failed")
        else:
            data.update({'uid': user.uid})
            return build_response(httplib.OK, CODE_OK, "Registration successful", data)

    else:
        return build_error_response(httplib.BAD_REQUEST, CODE_INSUFFICIENT_CREDENTIALS,
                                    'Some fields are not filled')


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/login/')
