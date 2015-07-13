from decider_api.utils import vk_helper
from decider_api.utils.helper import BACKENDS


def get_additional_data(strategy, details, user=None, *args, **kwargs):
    if user:
        backend = strategy.session.get('oauth_backend')
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
