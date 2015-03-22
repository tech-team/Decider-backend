from django.http import JsonResponse


def build_ok_response(data):
    return JsonResponse({
        'status': 200,
        'msg': 'ok',
        'data': data
    })


def build_402_response(error_text):
    return JsonResponse({
        'status': 402,
        'msg': 'incorrect data',
        'data': {
            'error_text': error_text
        }
    })


def build_403_response(error_text):
    return JsonResponse({
        'status': 403,
        'msg': 'insufficient data',
        'data': {
            'error_text': error_text
        }
    })


def build_404_response(error_text, msg=None, http_code=404):
    return JsonResponse({
        'status': 404,
        'msg': msg if msg else 'user not found',
        'data': {
            'error_text': error_text
        }
    }, status=http_code)


def build_501_response(error_text):
    return JsonResponse({
        'status': 501,
        'msg': 'internal error',
        'data': {
            'error_text': error_text
        }
    })


