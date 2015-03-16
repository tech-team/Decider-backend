import json
import urlparse
from decider_backend.settings import HOST_SCHEMA, HOST_ADDRESS, HOST_PORT

TOKEN_URL = urlparse.urlunparse((HOST_SCHEMA, HOST_ADDRESS + ':' + HOST_PORT, '/o/token/', '', '', ''))


def build_ok_response(data):
    return json.dumps({
        'status': 200,
        'msg': 'ok',
        'data': {
            'access_token': data.get('access_token'),
            'expires': data.get('expires_in'),
            'refresh_token': data.get('refresh_token')
        }
    })


def build_402_response(error_text):
    return json.dumps({
        'status': 402,
        'msg': 'incorrect data',
        'data': {
            'error_text': error_text
        }
    })


def build_403_response(error_text):
    return json.dumps({
        'status': 403,
        'msg': 'insufficient data',
        'data': {
            'error_text': error_text
        }
    })


def build_501_response(error_text):
    return json.dumps({
        'status': 501,
        'msg': 'internal error',
        'data': {
            'error_text': error_text
        }
    })