import httplib
import json
from decider_app.views.utils.response_builder import build_error_response
from decider_app.views.utils.response_codes import CODE_REQUIRED_PARAMS_MISSING, CODE_INVALID_DATA


def require_params(*params):
    def decorator(func):
        def wrapped(request, *args, **kwargs):
            errors = []
            for param in params[0]:
                if getattr(args[0], args[0].method).get(param) is None:
                    errors.append(param)

            if errors:
                return build_error_response(httplib.BAD_REQUEST, CODE_REQUIRED_PARAMS_MISSING,
                                            "Required params are missing", errors)
            else:
                return func(request, *args, **kwargs)
        return wrapped
    return decorator


def require_post_data(*params):
    def decorator(func):
        def wrapped(request, *args, **kwargs):
            try:
                data = json.loads(args[0].POST.get("data"))
            except ValueError:
                return build_error_response(httplib.BAD_REQUEST, CODE_INVALID_DATA,
                                            "Some fields are invalid", ['data'])
            except TypeError:
                return build_error_response(httplib.BAD_REQUEST, CODE_REQUIRED_PARAMS_MISSING,
                                            "Required params are missing", ['data'])

            errors = []
            for param in params[0]:
                if data.get(param) is None:
                    errors.append(param)

            if errors:
                return build_error_response(httplib.BAD_REQUEST, CODE_REQUIRED_PARAMS_MISSING,
                                            "Required params are missing", errors)
            else:
                return func(request, *args, **kwargs)
        return wrapped
    return decorator