import urlparse
from django.core.urlresolvers import reverse
from decider_backend.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET, HOST_SCHEMA, HOST_ADDRESS, HOST_PORT


def get_token_url():
    return urlparse.urlunparse((HOST_SCHEMA, HOST_ADDRESS + ':' + HOST_PORT, str(reverse('oauth2_provider:token')), '', '', ''))


def build_token_request_data(email, password):
    return {
        'grant_type': 'password',
        'client_id': OAUTH_CLIENT_ID,
        'client_secret': OAUTH_CLIENT_SECRET,
        'username': email,
        'password': password
    }