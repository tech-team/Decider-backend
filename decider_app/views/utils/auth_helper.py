import json
import urllib
import urllib2
import urlparse
from django.core.urlresolvers import reverse
from decider_api.log_manager import logger
from decider_backend.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, HOST_SCHEMA, HOST_ADDRESS, HOST_PORT


def grant_type_switch(case):
    return {
        "password": build_token_request_data,
        "refresh_token": build_refresh_token_request_data
    }.get(case)


def get_token_url():
    return urlparse.urlunparse((HOST_SCHEMA, HOST_ADDRESS + ':' + HOST_PORT, str(reverse('oauth2_provider:token')), '', '', ''))


def build_token_request_data(data):
    return {
        'grant_type': 'password',
        'client_id': OAUTH_CLIENT_ID,
        'client_secret': OAUTH_CLIENT_SECRET,
        'username': data.get('email'),
        'password': data.get('password')
    }


def build_refresh_token_request_data(data):
    return {
        'grant_type': 'refresh_token',
        'client_id': OAUTH_CLIENT_ID,
        'client_secret': OAUTH_CLIENT_SECRET,
        'refresh_token': data.get('token')
    }


def get_token_data(grant_type, data):
    try:
        post_data = urllib.urlencode(grant_type_switch(grant_type)(data))
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
