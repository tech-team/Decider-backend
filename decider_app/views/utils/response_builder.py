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



