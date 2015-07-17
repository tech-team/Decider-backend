from django.contrib.auth import logout
from decider_api.utils import vk_helper
from decider_api.utils.helper import BACKENDS
from decider_app.views.utils.auth_helper import get_token_data


def logout_internal(backend, details, response, *args, **kwargs):
    logout(backend.strategy.request)
    logout(kwargs.get('strategy').request)
    return


def get_additional_data(strategy, details, user=None, *args, **kwargs):
    if user and kwargs.get('is_new'):

        backend = strategy.session.get('oauth_backend')
        if backend:
            del strategy.session['oauth_backend']

        if kwargs.get('social'):
            access_token = kwargs.get('social').access_token
        else:
            access_token = user.social_auth.objects.get(user_id=user.id, provider=backend)

        provider = None
        for k, v in BACKENDS.iteritems():
            if v == backend:
                provider = k

        if provider == 'vk':
            vk_helper.get_additional_data(user, access_token)

    else:
        return


def get_access_token(strategy, details, user=None, *args, **kwargs):
    if user:
        data = get_token_data(
            'password',
            {
                'email': user.email,
                'password': user.get_dummy_password()
            }
        )
        if data:
            strategy.session['access_token'] = data
    else:
        return
