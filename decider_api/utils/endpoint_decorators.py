import httplib
import json
from django.utils import timezone
from decider_app.views.utils.response_builder import build_error_response
from decider_app.views.utils.response_codes import CODE_REQUIRED_PARAMS_MISSING, CODE_INVALID_DATA, \
    CODE_REGISTRATION_UNFINISHED


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


def track_activity(func):
    def wrapped(request, *args, **kwargs):
        if hasattr(request, 'request') and hasattr(request.request, 'resource_owner'):
            from push_service.models import NotificationHistory
            user = request.request.resource_owner
            user.update_last_active()
            NotificationHistory.objects.filter(user_id=user.id).delete()
        return func(request, *args, **kwargs)
    return wrapped


def require_registration(func):
    def wrapped(request, *args, **kwargs):
        if request.request.resource_owner.is_authenticated() and request.request.resource_owner.registration_finished():
            return func(request, *args, **kwargs)
        else:
            return build_error_response(httplib.BAD_REQUEST, CODE_REGISTRATION_UNFINISHED,
                                        "Registration unfinished")
    return wrapped
