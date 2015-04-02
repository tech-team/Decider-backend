from django.http import JsonResponse
from decider_app.views.utils.response_codes import CODE_OK, CODE_CREATED


def build_error_response(status, code, msg, errors=None):

    resp_dict = {
        "status": "error",
        "code": code,
        "msg": msg,
        "errors": errors if errors else []
    }

    return JsonResponse(resp_dict, status=status)


def build_response(status, code=CODE_OK, msg="ok", data=None, extra_fields=None):

    resp_dict = {
        "status": "ok",
        "code": code,
        "msg": msg
    }
    if data is not None:
        resp_dict["data"] = data
    if extra_fields is not None:
        for field in extra_fields:
            resp_dict[field] = extra_fields[field]

    return JsonResponse(resp_dict, status=status)


# TODO: get rid of these responses
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


