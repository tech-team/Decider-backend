# coding=utf-8
import httplib
import urllib
import urllib2
import uuid
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from decider_api.utils.endpoint_decorators import require_params
from decider_api.utils.helper import get_user_data, BACKENDS

from decider_app.models import User, SocialSite
from decider_app.views.utils.auth_helper import get_token_data
from decider_app.views.utils.response_builder import build_response, build_error_response
from decider_app.views.utils.response_codes import CODE_OK, CODE_INVALID_CREDENTIALS, CODE_LOGIN_FAILED, \
    CODE_INSUFFICIENT_CREDENTIALS, CODE_UNKNOWN_SOCIAL, CODE_REQUIRED_PARAMS_MISSING, CODE_INVALID_TOKEN, CODE_CREATED


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
            return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_CREDENTIALS, 'Invalid credentials')
        else:
            data = get_token_data(
                'password',
                {
                    'email': user.email,
                    'password': password
                }
            )
            if not data:
                return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_LOGIN_FAILED, "Login failed")
            else:
                data.update({'user': get_user_data(user)})
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
            return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_CREDENTIALS,
                                        "Invalid credentials")

        data = get_token_data(
            'password',
            {
                'email': user.email,
                'password': password
            }
        )
        if not data:
            return build_error_response(httplib.INTERNAL_SERVER_ERROR, CODE_LOGIN_FAILED, "Registration failed")
        else:
            data.update({'user': get_user_data(user)})
            return build_response(httplib.OK, CODE_OK, "Registration successful", data)

    else:
        return build_error_response(httplib.BAD_REQUEST, CODE_INSUFFICIENT_CREDENTIALS,
                                    'Some fields are not filled')


@require_http_methods(['POST'])
def refresh_token_view(request):
    refresh_token = request.POST.get('refresh_token')
    if not refresh_token:
        return build_error_response(httplib.BAD_REQUEST, CODE_REQUIRED_PARAMS_MISSING,
                                    "Required params are missing", ['refresh_token'])

    data = get_token_data(
        'refresh_token',
        {
            'token': refresh_token
        }
    )

    if not data:
        return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_TOKEN,
                                    "Invalid refresh token")

    return build_response(httplib.CREATED, CODE_CREATED, "Here is your fresh token", data)


def social_login(request, provider):
    if provider in BACKENDS:
        logout(request)
        request.session['oauth_backend'] = BACKENDS[provider]
        return redirect(reverse('api:social:begin', kwargs={'backend': BACKENDS[provider]}))
    else:
        return render(request, 'social_login.html', {'text': 'Backend not supported'})

def social_complete(request):
    if request.user.is_authenticated():
        if 'access_token' in request.GET:
            return render(request, 'social_login.html', {'text': 'Login successful'})
        else:
            data = request.session.get('access_token')
            if data:
                del request.session['access_token']

                response = redirect('api:social_complete')
                response['Location'] += '?access_token=' + data.get('access_token') + \
                                        '&expires=' + str(data.get('expires')) + \
                                        '&refresh_token=' + data.get('refresh_token') + \
                                        '&user_id=' + request.user.social_id
                return response
            else:
                return render(request, 'social_login.html', {'text': 'You need to login again'})
    else:
        return render(request, 'social_login.html', {'text': 'Something went wrong'})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('/login/')
