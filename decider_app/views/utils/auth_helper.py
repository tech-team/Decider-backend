from decider_backend.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET


def build_token_request_data(email, password):
    return {
        'grant_type': 'password',
        'client_id': OAUTH_CLIENT_ID,
        'client_secret': OAUTH_CLIENT_SECRET,
        'username': email,
        'password': password
    }